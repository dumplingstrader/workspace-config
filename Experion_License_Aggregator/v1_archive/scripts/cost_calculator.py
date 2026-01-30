"""
License Cost Calculator
Calculates estimated costs based on cost catalog with MPC 2026 override support.
"""

import json
from pathlib import Path
from typing import Dict, List


class CostCalculator:
    """Calculate license costs from cost catalog with pricing override support."""
    
    def __init__(self, catalog_path: str, placeholder_cost: float = 100.0, 
                 override_catalog_path: str = None):
        """
        Initialize cost calculator with pricing override support.
        
        Priority order:
        1. MPC 2026 override catalog (if provided)
        2. Base Honeywell 2021-2022 catalog
        3. Placeholder cost
        
        Args:
            catalog_path: Path to cost_catalog.json (Honeywell baseline)
            placeholder_cost: Default cost for unknown items
            override_catalog_path: Path to cost_catalog_mpc_2026.json (optional)
        """
        self.placeholder_cost = placeholder_cost
        self.catalog = self._load_catalog(catalog_path)
        self.override_catalog = {}
        
        # Load MPC 2026 overrides if provided
        if override_catalog_path and Path(override_catalog_path).exists():
            self.override_catalog = self._load_catalog(override_catalog_path)
            print(f"✓ Loaded {len(self.override_catalog)} MPC 2026 pricing overrides")
    
    def _load_catalog(self, catalog_path: str) -> Dict:
        """Load cost catalog from JSON file."""
        try:
            with open(catalog_path, 'r') as f:
                catalog = json.load(f)
            # Remove metadata fields
            for key in ['_comment', '_format', '_usage', '_last_updated', '_instructions']:
                catalog.pop(key, None)
            return catalog
        except FileNotFoundError:
            print(f"Warning: Cost catalog not found at {catalog_path}")
            return {}
        except json.JSONDecodeError as e:
            print(f"Error parsing cost catalog: {e}")
            return {}
    
    def calculate_item_cost(self, option_name: str, quantity: int) -> Dict:
        """
        Calculate cost for a single license option.
        Uses MPC 2026 pricing if available, otherwise falls back to baseline.
        
        Args:
            option_name: License option name (e.g., 'PROCESSPOINTS')
            quantity: Licensed quantity
            
        Returns:
            Dictionary with cost breakdown and pricing source
        """
        # Check override catalog first (MPC 2026 pricing)
        if option_name in self.override_catalog:
            item = self.override_catalog[option_name]
            pricing_source = item.get('source', 'MPC 2026 Override')
        elif option_name in self.catalog:
            item = self.catalog[option_name]
            pricing_source = 'Honeywell 2021-2022 Baseline'
        else:
            # Use placeholder for unknown items
            return {
                'option': option_name,
                'quantity': quantity,
                'unit_cost': self.placeholder_cost,
                'per': 1,
                'units': quantity,
                'total_cost': quantity * self.placeholder_cost,
                'is_placeholder': True,
                'pricing_source': 'Placeholder (Unknown Item)'
            }
        
        # Extract pricing info
        unit_cost = item.get('unit_cost', self.placeholder_cost)
        per = item.get('per', 1)
        category = item.get('category', 'Unknown')
        description = item.get('description', '')
        is_placeholder = item.get('is_placeholder', False)
        
        # Calculate units (round up)
        units = (quantity + per - 1) // per if per > 0 else quantity
        total_cost = units * unit_cost
        
        return {
            'option': option_name,
            'quantity': quantity,
            'unit_cost': unit_cost,
            'per': per,
            'units': units,
            'total_cost': total_cost,
            'category': category,
            'description': description,
            'is_placeholder': is_placeholder,
            'pricing_source': pricing_source
        }
        
        item = self.catalog[option_name]
        unit_cost = item.get('unit_cost', self.placeholder_cost)
        per = item.get('per', 1)
        
        # Calculate number of units (round up)
        units = (quantity + per - 1) // per if per > 0 else 0
        total_cost = units * unit_cost
        
        return {
            'option': option_name,
            'quantity': quantity,
            'unit_cost': unit_cost,
            'per': per,
            'units': units,
            'total_cost': total_cost,
            'category': item.get('category', 'Other'),
            'description': item.get('description', option_name),
            'is_placeholder': item.get('is_placeholder', False)
        }
    
    def calculate_system_cost(self, license_data: Dict) -> Dict:
        """
        Calculate total cost for a system.
        
        Args:
            license_data: Dictionary with license option quantities
            
        Returns:
            Dictionary with cost breakdown by category and total
        """
        costs_by_category = {}
        total_cost = 0
        line_items = []
        
        # Track all options from catalog
        for option_name in self.catalog.keys():
            quantity = license_data.get(option_name, 0)
            
            if quantity > 0:  # Only calculate cost for licensed options
                cost_detail = self.calculate_item_cost(option_name, quantity)
                line_items.append(cost_detail)
                
                category = cost_detail['category']
                if category not in costs_by_category:
                    costs_by_category[category] = 0
                costs_by_category[category] += cost_detail['total_cost']
                total_cost += cost_detail['total_cost']
        
        return {
            'system': f"{license_data.get('cluster', 'Unknown')} - {license_data.get('msid', 'Unknown')}",
            'msid': license_data.get('msid', 'Unknown'),
            'system_number': license_data.get('system_number', 'Unknown'),
            'line_items': line_items,
            'costs_by_category': costs_by_category,
            'total_cost': total_cost
        }
    
    def calculate_all_systems(self, licenses: List[Dict]) -> Dict:
        """
        Calculate costs for all systems.
        
        Args:
            licenses: List of license data dictionaries
            
        Returns:
            Summary with per-system and total costs
        """
        system_costs = []
        total_by_cluster = {}
        total_by_category = {}
        grand_total = 0
        
        for lic in licenses:
            cost_detail = self.calculate_system_cost(lic)
            system_costs.append(cost_detail)
            
            # Accumulate cluster totals
            cluster = lic.get('cluster', 'Unknown')
            if cluster not in total_by_cluster:
                total_by_cluster[cluster] = 0
            total_by_cluster[cluster] += cost_detail['total_cost']
            
            # Accumulate category totals
            for category, amount in cost_detail['costs_by_category'].items():
                if category not in total_by_category:
                    total_by_category[category] = 0
                total_by_category[category] += amount
            
            grand_total += cost_detail['total_cost']
        
        return {
            'system_costs': system_costs,
            'total_by_cluster': total_by_cluster,
            'total_by_category': total_by_category,
            'grand_total': grand_total,
            'system_count': len(licenses)
        }
    
    def identify_transfer_candidates(self, licenses: List[Dict],
                                     excess_points_absolute: int = 500,
                                     excess_points_percent: int = 25) -> List[Dict]:
        """
        Identify systems with excess capacity that could be transferred.
        
        Args:
            licenses: List of license data
            excess_points_absolute: Minimum excess points to qualify
            excess_points_percent: Minimum excess percentage to qualify
            
        Returns:
            List of transfer candidate systems
        """
        candidates = []
        
        # License types to check for excess capacity
        license_types = ['PROCESSPOINTS', 'SCADAPOINTS', 'STATIONS', 'MULTISTATIONS', 'DIRECTSTATIONS']
        
        for lic in licenses:
            excess_items = []
            total_excess_value = 0
            
            for license_type in license_types:
                licensed = lic.get(license_type, 0)
                used = lic.get(f'{license_type}_USED', 0)
                
                if licensed > 0:
                    excess = licensed - used
                    util_percent = (used / licensed * 100) if licensed > 0 else 0
                    excess_percent = 100 - util_percent
                    
                    # Qualify if significant excess (absolute OR percentage)
                    if (excess >= excess_points_absolute or excess_percent >= excess_points_percent) and excess > 0:
                        cost_result = self.calculate_item_cost(license_type, excess)
                        excess_value = cost_result['total_cost']
                        
                        excess_items.append({
                            'type': license_type,
                            'licensed': licensed,
                            'used': used,
                            'excess': excess,
                            'utilization_percent': util_percent,
                            'excess_percent': excess_percent,
                            'excess_value': excess_value
                        })
                        total_excess_value += excess_value
            
            # Only flag as candidate if has significant excess capacity
            if excess_items and total_excess_value > 1000:  # $1k minimum excess value
                candidates.append({
                    'cluster': lic.get('cluster'),
                    'msid': lic.get('msid'),
                    'system_number': lic.get('system_number'),
                    'excess_items': excess_items,
                    'total_excess_value': total_excess_value,
                    'has_utilization_data': any(lic.get(f'{lt}_USED', 0) > 0 for lt in license_types)
                })
        
        return candidates


if __name__ == '__main__':
    # Test cost calculations
    calc = CostCalculator('../config/cost_catalog.json')
    
    # Sample license
    test_license = {
        'cluster': 'Carson',
        'msid': 'M0614',
        'system_number': '60806',
        'PROCESSPOINTS': 5000,
        'SCADAPOINTS': 2000,
        'STATIONS': 10,
        'DUAL': 1,
        'DAS': 1
    }
    
    system_cost = calc.calculate_system_cost(test_license)
    print(f"System cost: ${system_cost['total_cost']:,.2f}")
    print("\nLine items:")
    for item in system_cost['line_items']:
        print(f"  {item['option']}: {item['quantity']} @ ${item['unit_cost']} per {item['per']} = ${item['total_cost']:,.2f}")
