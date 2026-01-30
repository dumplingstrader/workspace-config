"""
Transfer Detector - Identify license transfer candidates.

This module identifies systems with significant excess capacity that could
potentially transfer licenses to systems with shortages.

Transfer Candidate Criteria (from transfer_rules.yaml):
1. Absolute excess: e.g., ≥500 unused points
2. Percentage excess: e.g., ≤75% utilization (≥25% excess)
3. Minimum value: e.g., excess worth ≥$1,000

A system qualifies if it meets ANY ONE criterion for a license type.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from pathlib import Path

from v2.core.config import Config
from v2.models.transfer import TransferCandidate


@dataclass
class TransferDetectionResult:
    """
    Result of transfer candidate detection.
    
    Attributes:
        candidates: List of TransferCandidate instances
        total_excess_value: Sum of all excess values
        high_priority_count: Number of HIGH priority candidates
        systems_analyzed: Number of systems checked
        stats: Detection statistics by license type
    
    Examples:
        >>> result = detector.detect(enriched_licenses)
        >>> print(f"Found {len(result.candidates)} candidates")
        >>> print(f"Total excess value: ${result.total_excess_value:,.2f}")
    """
    candidates: List[TransferCandidate]
    total_excess_value: float
    high_priority_count: int
    systems_analyzed: int
    stats: Dict[str, int]


class TransferDetector:
    """
    Detect license transfer candidates using configured rules.
    
    Identifies systems with excess licenses that could be transferred
    to other systems based on criteria in transfer_rules.yaml.
    
    Detection Logic:
    - For each license type in each system:
      1. Calculate excess = licensed - used
      2. Check if meets any criterion (absolute, percentage, value)
      3. If yes, create TransferCandidate with priority
    
    Priority Levels:
    - HIGH: excess_value >= $10,000
    - MEDIUM: excess_value >= $1,000
    - LOW: excess_value < $1,000
    
    Examples:
        >>> detector = TransferDetector(config)
        >>> result = detector.detect(enriched_licenses)
        >>> for candidate in result.candidates:
        ...     print(f"{candidate.msid}: {candidate.license_type} "
        ...           f"- {candidate.excess_quantity} excess")
    """
    
    def __init__(self, config: Config):
        """
        Initialize transfer detector with configuration.
        
        Args:
            config: Config instance with transfer_rules.yaml loaded
        
        Raises:
            KeyError: If transfer_rules not in config
        """
        self.config = config
        
        if not hasattr(config, 'transfer_rules'):
            raise KeyError("Config must contain transfer_rules")
        
        self.rules = config.transfer_rules
        self.criteria = self.rules.get('criteria', {})
    
    def detect(
        self,
        enriched_licenses: List[Dict],
        usage_data: Optional[List[Dict]] = None
    ) -> TransferDetectionResult:
        """
        Detect transfer candidates from enriched license data.
        
        Args:
            enriched_licenses: List of license dicts with usage and costs
            usage_data: Optional list of usage dicts (can extract from enriched)
        
        Returns:
            TransferDetectionResult with candidates and statistics
        
        Algorithm:
        1. For each license record:
           a. Extract license type quantities
           b. Extract usage quantities
           c. Calculate excess for each type
           d. Check criteria for each type
           e. Create TransferCandidate if qualified
        2. Calculate aggregate statistics
        3. Sort candidates by priority and excess value
        
        Examples:
            >>> enriched = [
            ...     {
            ...         'msid': 'M0614',
            ...         'licensed': {'PROCESSPOINTS': 4750},
            ...         'usage': {'PROCESSPOINTS': 108},
            ...         'costs': {'PROCESSPOINTS': 213750.00}
            ...     }
            ... ]
            >>> result = detector.detect(enriched)
            >>> assert len(result.candidates) > 0
        """
        candidates = []
        systems_analyzed = 0
        license_type_stats = {}
        
        for license_record in enriched_licenses:
            systems_analyzed += 1
            
            # Extract data
            msid = license_record.get('msid', '')
            system_number = license_record.get('system_number', '')
            cluster = license_record.get('cluster', '')
            licensed = license_record.get('licensed', {})
            
            # Get usage data
            usage_dict = self._extract_usage(license_record, usage_data)
            
            # Get cost data
            costs = license_record.get('costs', {})
            
            # Check each license type
            for license_type, licensed_qty in licensed.items():
                used_qty = usage_dict.get(license_type, 0)
                excess_qty = licensed_qty - used_qty
                
                # Skip if no excess
                if excess_qty <= 0:
                    continue
                
                # Get unit price
                unit_price = self._get_unit_price(license_type, costs)
                
                # Calculate excess value
                excess_value = excess_qty * unit_price if unit_price else 0.0
                
                # Check if meets criteria
                if self._meets_criteria(license_type, licensed_qty, used_qty, excess_qty, excess_value):
                    # Determine priority
                    priority = self._calculate_priority(excess_value)
                    
                    # Create candidate
                    candidate = TransferCandidate(
                        msid=msid,
                        system_number=system_number,
                        cluster=cluster,
                        license_type=license_type,
                        licensed_quantity=licensed_qty,
                        used_quantity=used_qty,
                        excess_quantity=excess_qty,
                        excess_value=round(excess_value, 2),
                        unit_price=unit_price,
                        priority=priority
                    )
                    candidates.append(candidate)
                    
                    # Update stats
                    license_type_stats[license_type] = license_type_stats.get(license_type, 0) + 1
        
        # Calculate aggregate stats
        total_excess_value = sum(c.excess_value for c in candidates)
        high_priority_count = sum(1 for c in candidates if c.priority == 'HIGH')
        
        # Sort by priority and value
        candidates.sort(key=lambda c: (
            {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2}[c.priority],
            -c.excess_value
        ))
        
        return TransferDetectionResult(
            candidates=candidates,
            total_excess_value=total_excess_value,
            high_priority_count=high_priority_count,
            systems_analyzed=systems_analyzed,
            stats=license_type_stats
        )
    
    def _extract_usage(
        self,
        license_record: Dict,
        usage_data: Optional[List[Dict]]
    ) -> Dict[str, int]:
        """
        Extract usage quantities for all license types.
        
        Args:
            license_record: License record with possible usage data
            usage_data: Optional external usage data
        
        Returns:
            Dict mapping license_type -> used_quantity
        """
        # Try to get usage from license record first
        if 'usage' in license_record:
            return license_record['usage']
        
        # Try to extract from matched usage data
        if usage_data and license_record.get('msid'):
            msid = license_record['msid']
            for usage in usage_data:
                if usage.get('msid') == msid:
                    # Build usage dict from usage record
                    return {usage.get('license_type', ''): usage.get('used_quantity', 0)}
        
        # No usage data available
        return {}
    
    def _get_unit_price(self, license_type: str, costs: Dict) -> float:
        """
        Get unit price for license type from costs.
        
        Args:
            license_type: Type of license
            costs: Dict of license_type -> cost_data
        
        Returns:
            Unit price or 0.0 if not found
        """
        if license_type in costs:
            cost_data = costs[license_type]
            if isinstance(cost_data, dict):
                return cost_data.get('unit_cost', 0.0)
        return 0.0
    
    def _meets_criteria(
        self,
        license_type: str,
        licensed_qty: int,
        used_qty: int,
        excess_qty: int,
        excess_value: float
    ) -> bool:
        """
        Check if license type meets ANY transfer criterion.
        
        Args:
            license_type: Type of license
            licensed_qty: Licensed quantity
            used_qty: Used quantity
            excess_qty: Excess quantity (licensed - used)
            excess_value: Dollar value of excess
        
        Returns:
            True if meets at least one enabled criterion
        """
        # Get criteria for this license type
        type_criteria = self.criteria.get(license_type, [])
        
        if not type_criteria:
            # No specific criteria - use defaults
            # Default: absolute ≥500, percentage ≥25%, value ≥$1000
            return (
                excess_qty >= 500 or
                (licensed_qty > 0 and (excess_qty / licensed_qty) >= 0.25) or
                excess_value >= 1000.0
            )
        
        # Check each criterion
        for criterion in type_criteria:
            if not criterion.get('enabled', False):
                continue
            
            criterion_type = criterion.get('type')
            threshold = criterion.get('threshold', 0)
            
            if criterion_type == 'absolute':
                # Check absolute excess
                if excess_qty >= threshold:
                    return True
            
            elif criterion_type == 'percentage':
                # Check percentage excess (threshold is % excess, e.g., 25 = ≥25% excess)
                if licensed_qty > 0:
                    utilization = (used_qty / licensed_qty) * 100
                    excess_percent = 100 - utilization
                    if excess_percent >= threshold:
                        return True
            
            elif criterion_type == 'value':
                # Check minimum value
                if excess_value >= threshold:
                    return True
        
        return False
    
    def _calculate_priority(self, excess_value: float) -> str:
        """
        Calculate priority level based on excess value.
        
        Args:
            excess_value: Dollar value of excess
        
        Returns:
            'HIGH', 'MEDIUM', or 'LOW'
        
        Priority Thresholds:
        - HIGH: >= $10,000
        - MEDIUM: >= $1,000
        - LOW: < $1,000
        """
        if excess_value >= 10000.0:
            return 'HIGH'
        elif excess_value >= 1000.0:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def get_candidates_by_priority(
        self,
        result: TransferDetectionResult,
        priority: str
    ) -> List[TransferCandidate]:
        """
        Filter candidates by priority level.
        
        Args:
            result: TransferDetectionResult from detect()
            priority: 'HIGH', 'MEDIUM', or 'LOW'
        
        Returns:
            List of candidates matching priority
        
        Examples:
            >>> high_priority = detector.get_candidates_by_priority(result, 'HIGH')
            >>> print(f"Found {len(high_priority)} high priority candidates")
        """
        return [c for c in result.candidates if c.priority == priority]
    
    def get_candidates_by_cluster(
        self,
        result: TransferDetectionResult,
        cluster: str
    ) -> List[TransferCandidate]:
        """
        Filter candidates by cluster/site.
        
        Args:
            result: TransferDetectionResult from detect()
            cluster: Cluster name
        
        Returns:
            List of candidates from cluster
        """
        return [c for c in result.candidates if c.cluster == cluster]
    
    def get_candidates_by_license_type(
        self,
        result: TransferDetectionResult,
        license_type: str
    ) -> List[TransferCandidate]:
        """
        Filter candidates by license type.
        
        Args:
            result: TransferDetectionResult from detect()
            license_type: Type of license
        
        Returns:
            List of candidates for license type
        """
        return [c for c in result.candidates if c.license_type == license_type]
    
    def generate_transfer_report(self, result: TransferDetectionResult) -> str:
        """
        Generate human-readable transfer candidate report.
        
        Args:
            result: TransferDetectionResult from detect()
        
        Returns:
            Multi-line string report
        
        Example Output:
            Transfer Candidate Report
            ==================================================
            Total Candidates: 12
            Total Excess Value: $425,890.50
            High Priority: 3
            
            HIGH PRIORITY CANDIDATES:
            M0614 (Carson/60806): PROCESSPOINTS
              Licensed: 4,750 | Used: 108 | Excess: 4,642
              Excess Value: $208,890.00 | Utilization: 2.3%
        """
        lines = [
            "Transfer Candidate Report",
            "=" * 60,
            f"Total Candidates: {len(result.candidates)}",
            f"Total Excess Value: ${result.total_excess_value:,.2f}",
            f"High Priority: {result.high_priority_count}",
            f"Systems Analyzed: {result.systems_analyzed}",
            ""
        ]
        
        # Group by priority
        for priority in ['HIGH', 'MEDIUM', 'LOW']:
            priority_candidates = self.get_candidates_by_priority(result, priority)
            if not priority_candidates:
                continue
            
            lines.append(f"{priority} PRIORITY CANDIDATES:")
            for candidate in priority_candidates:
                lines.append(f"{candidate.msid} ({candidate.cluster}/{candidate.system_number}): {candidate.license_type}")
                lines.append(f"  Licensed: {candidate.licensed_quantity:,} | "
                           f"Used: {candidate.used_quantity:,} | "
                           f"Excess: {candidate.excess_quantity:,}")
                lines.append(f"  Excess Value: ${candidate.excess_value:,.2f} | "
                           f"Utilization: {candidate.utilization_percentage():.1f}%")
                lines.append("")
        
        # License type summary
        if result.stats:
            lines.append("License Type Summary:")
            for license_type, count in sorted(result.stats.items()):
                lines.append(f"- {license_type}: {count} candidates")
        
        return "\n".join(lines)
