"""
Cost Calculator - Multi-source cost calculation with cascade strategy.

This module implements the pricing cascade strategy where multiple cost
catalogs are checked in priority order until a price is found.

Cascade Order:
1. MPC 2026 Confirmed (priority 1) - Most current pricing
2. Honeywell Baseline (priority 2) - Historical pricing
3. Placeholder (priority 3) - Default $100 for unknown types

Cost Formula: (quantity / per) * unit_cost
Example: 4750 PROCESSPOINTS at $45 per 50 = (4750 / 50) * 45 = $4,275
"""

from dataclasses import dataclass
from typing import Dict, Optional, List, Any
from pathlib import Path
import json

from v2.core.config import Config


@dataclass
class CostResult:
    """
    Result of cost calculation for a single license type.
    
    Attributes:
        license_type: Type of license (e.g., 'PROCESSPOINTS')
        quantity: Licensed quantity
        unit_cost: Cost per 'per' increment
        per: Quantity increment
        total_cost: Calculated total cost
        pricing_source: Which catalog provided the price
        calculation_details: Human-readable calculation explanation
    
    Examples:
        >>> result = CostResult(
        ...     license_type='PROCESSPOINTS',
        ...     quantity=4750,
        ...     unit_cost=45.00,
        ...     per=50,
        ...     total_cost=4275.00,
        ...     pricing_source='MPC 2026 Confirmed'
        ... )
    """
    license_type: str
    quantity: int
    unit_cost: float
    per: int
    total_cost: float
    pricing_source: str
    calculation_details: str = ""


@dataclass
class LicenseCostSummary:
    """
    Complete cost calculation for all license types in a system.
    
    Attributes:
        msid: System identifier
        cluster: Site location
        system_number: License number
        costs: List of CostResult for each license type
        total_cost: Sum of all license type costs
        missing_prices: List of license types with no pricing data
    
    Examples:
        >>> summary = calculator.calculate_license_cost(license_data)
        >>> print(f"Total: ${summary.total_cost:,.2f}")
    """
    msid: str
    cluster: str
    system_number: str
    costs: List[CostResult]
    total_cost: float
    missing_prices: List[str]


class CostCalculator:
    """
    Calculate license costs using multi-source pricing cascade.
    
    Implements priority-based pricing lookup across multiple catalogs.
    Falls back to placeholder pricing for unknown license types.
    
    The cost formula is: (quantity / per) * unit_cost
    - quantity: Licensed quantity from XML
    - per: Increment size from catalog (e.g., 50 points)
    - unit_cost: Price per increment from catalog
    
    Examples:
        >>> calculator = CostCalculator(config)
        >>> summary = calculator.calculate_license_cost(license_data)
        >>> for cost in summary.costs:
        ...     print(f"{cost.license_type}: ${cost.total_cost:,.2f}")
    """
    
    def __init__(self, config: Config):
        """
        Initialize cost calculator with configuration.
        
        Args:
            config: Config instance with cost_rules.yaml loaded
        
        Raises:
            KeyError: If cost_rules not in config
        """
        self.config = config
        
        if not hasattr(config, 'cost_rules'):
            raise KeyError("Config must contain cost_rules")
        
        self.rules = config.cost_rules
        self.pricing_strategy = self.rules.get('pricing_strategy', [])
        self.calculation_rules = self.rules.get('calculation', {})
        
        # Load all cost catalogs
        self.catalogs = self._load_catalogs()
    
    def _load_catalogs(self) -> Dict[str, Dict[str, Any]]:
        """
        Load all cost catalogs defined in pricing strategy.
        
        Returns:
            Dict mapping catalog name to catalog data
        """
        catalogs = {}
        config_dir = self.config.config_dir
        
        for strategy in self.pricing_strategy:
            source = strategy.get('source')
            if source:
                catalog_path = config_dir / source
                if catalog_path.exists():
                    with open(catalog_path, 'r') as f:
                        catalogs[strategy['name']] = json.load(f)
                else:
                    # Catalog file missing - use empty dict
                    catalogs[strategy['name']] = {}
        
        return catalogs
    
    def calculate_license_cost(
        self,
        licensed: Dict[str, int],
        msid: str = "",
        cluster: str = "",
        system_number: str = ""
    ) -> LicenseCostSummary:
        """
        Calculate total cost for all license types in a system.
        
        Args:
            licensed: Dict of license type -> quantity
            msid: System identifier (for reporting)
            cluster: Site location (for reporting)
            system_number: License number (for reporting)
        
        Returns:
            LicenseCostSummary with individual and total costs
        
        Examples:
            >>> licensed = {'PROCESSPOINTS': 4750, 'DIRECTSTATIONS': 8}
            >>> summary = calculator.calculate_license_cost(licensed, 'M0614')
            >>> print(summary.total_cost)
            4327.40
        """
        costs = []
        total = 0.0
        missing_prices = []
        
        for license_type, quantity in licensed.items():
            # Skip zero quantities if configured
            if quantity == 0 and not self.calculation_rules.get('include_zero_costs', False):
                continue
            
            # Get pricing for this license type
            cost_result = self._calculate_single_cost(license_type, quantity)
            
            if cost_result:
                costs.append(cost_result)
                total += cost_result.total_cost
            else:
                missing_prices.append(license_type)
        
        # Round total if configured
        if self.calculation_rules.get('round_to_cents', True):
            total = round(total, 2)
        
        return LicenseCostSummary(
            msid=msid,
            cluster=cluster,
            system_number=system_number,
            costs=costs,
            total_cost=total,
            missing_prices=missing_prices
        )
    
    def _calculate_single_cost(
        self,
        license_type: str,
        quantity: int
    ) -> Optional[CostResult]:
        """
        Calculate cost for single license type using cascade.
        
        Args:
            license_type: Type of license (e.g., 'PROCESSPOINTS')
            quantity: Licensed quantity
        
        Returns:
            CostResult if pricing found, None otherwise
        
        Algorithm:
        1. Try each catalog in priority order
        2. If found, calculate cost using formula
        3. If not found in any catalog, use placeholder
        """
        # Try each pricing source in priority order
        for strategy in sorted(self.pricing_strategy, key=lambda x: x.get('priority', 999)):
            catalog_name = strategy['name']
            
            # Check if this is placeholder strategy
            if 'value' in strategy:
                # Placeholder pricing
                unit_cost = strategy['value']
                per = 1
                total = self._apply_cost_formula(quantity, unit_cost, per)
                
                return CostResult(
                    license_type=license_type,
                    quantity=quantity,
                    unit_cost=unit_cost,
                    per=per,
                    total_cost=total,
                    pricing_source=catalog_name,
                    calculation_details=f"{quantity} × ${unit_cost:.2f} = ${total:.2f}"
                )
            
            # Check catalog for this license type
            catalog = self.catalogs.get(catalog_name, {})
            if license_type in catalog:
                pricing = catalog[license_type]
                unit_cost = pricing.get('unit_cost', 0.0)
                per = pricing.get('per', 1)
                
                total = self._apply_cost_formula(quantity, unit_cost, per)
                
                # Build calculation details
                if per == 1:
                    details = f"{quantity} × ${unit_cost:.2f} = ${total:.2f}"
                else:
                    details = f"({quantity} / {per}) × ${unit_cost:.2f} = ${total:.2f}"
                
                return CostResult(
                    license_type=license_type,
                    quantity=quantity,
                    unit_cost=unit_cost,
                    per=per,
                    total_cost=total,
                    pricing_source=catalog_name,
                    calculation_details=details
                )
        
        # No pricing found in any source
        return None
    
    def _apply_cost_formula(
        self,
        quantity: int,
        unit_cost: float,
        per: int
    ) -> float:
        """
        Apply cost calculation formula with rounding.
        
        Args:
            quantity: Licensed quantity
            unit_cost: Cost per 'per' increment
            per: Quantity increment
        
        Returns:
            Total cost (rounded if configured)
        
        Formula: (quantity / per) * unit_cost
        """
        total = (quantity / per) * unit_cost
        
        # Apply rounding
        if self.calculation_rules.get('round_to_cents', True):
            total = round(total, 2)
        
        # Apply minimum charge
        min_charge = self.calculation_rules.get('minimum_charge', 0.0)
        if total < min_charge:
            total = min_charge
        
        return total
    
    def get_pricing_source(self, license_type: str) -> Optional[str]:
        """
        Find which catalog provides pricing for a license type.
        
        Args:
            license_type: Type of license (e.g., 'PROCESSPOINTS')
        
        Returns:
            Catalog name if found, None otherwise
        
        Examples:
            >>> source = calculator.get_pricing_source('PROCESSPOINTS')
            >>> print(source)
            MPC 2026 Confirmed
        """
        for strategy in sorted(self.pricing_strategy, key=lambda x: x.get('priority', 999)):
            catalog_name = strategy['name']
            
            # Skip placeholder
            if 'value' in strategy:
                continue
            
            catalog = self.catalogs.get(catalog_name, {})
            if license_type in catalog:
                return catalog_name
        
        # Check for placeholder
        for strategy in self.pricing_strategy:
            if 'value' in strategy:
                return strategy['name']
        
        return None
    
    def get_all_available_license_types(self) -> List[str]:
        """
        Get list of all license types with pricing data.
        
        Returns:
            List of license type names across all catalogs
        
        Examples:
            >>> types = calculator.get_all_available_license_types()
            >>> print(types)
            ['PROCESSPOINTS', 'SCADAPOINTS', 'DIRECTSTATIONS', ...]
        """
        all_types = set()
        
        for catalog in self.catalogs.values():
            all_types.update(catalog.keys())
        
        return sorted(all_types)
    
    def generate_pricing_report(self, summary: LicenseCostSummary) -> str:
        """
        Generate human-readable pricing report.
        
        Args:
            summary: LicenseCostSummary from calculate_license_cost()
        
        Returns:
            Multi-line string report
        
        Example Output:
            Cost Breakdown for M0614 (Carson/60806)
            ========================================
            PROCESSPOINTS: 4,750 @ $45.00/50 = $4,275.00 (MPC 2026)
            DIRECTSTATIONS: 8 @ $6.55/1 = $52.40 (Honeywell Baseline)
            
            Total: $4,327.40
        """
        lines = [
            f"Cost Breakdown for {summary.msid} ({summary.cluster}/{summary.system_number})",
            "=" * 60
        ]
        
        for cost in summary.costs:
            line = (
                f"{cost.license_type}: {cost.quantity:,} "
                f"@ ${cost.unit_cost:.2f}/{cost.per} = "
                f"${cost.total_cost:,.2f} ({cost.pricing_source})"
            )
            lines.append(line)
        
        if summary.missing_prices:
            lines.append("")
            lines.append("Missing Pricing:")
            for license_type in summary.missing_prices:
                lines.append(f"- {license_type}")
        
        lines.append("")
        lines.append(f"Total: ${summary.total_cost:,.2f}")
        
        return "\n".join(lines)
