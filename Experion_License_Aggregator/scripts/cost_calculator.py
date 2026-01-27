"""
License Cost Calculator
Calculates estimated costs based on cost catalog.
"""

import json
from pathlib import Path
from typing import Dict, List


class CostCalculator:
    """Calculate license costs from cost catalog."""
    
    def __init__(self, catalog_path: str, placeholder_cost: float = 100.0):
        """
        Initialize cost calculator.
        
        Args:
            catalog_path: Path to cost_catalog.json
            placeholder_cost: Default cost for unknown items
        """
        self.placeholder_cost = placeholder_cost
        self.catalog = self._load_catalog(catalog_path)
    
    def _load_catalog(self, catalog_path: str) -> Dict:
        """Load cost catalog from JSON file."""
        try:
            with open(catalog_path, 'r') as f:
                catalog = json.load(f)
            # Remove metadata fields
            catalog.pop('_comment', None)
            catalog.pop('_format', None)
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
        
        Args:
            option_name: License option name (e.g., 'PROCESSPOINTS')
            quantity: Licensed quantity
            
        Returns:
            Dictionary with cost breakdown
        """
        if option_name not in self.catalog:
            return {
                'option': option_name,
                'quantity': quantity,
                'unit_cost': self.placeholder_cost,
                'per': 1,
                'units': quantity,
                'total_cost': quantity * self.placeholder_cost,
                'is_placeholder': True
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
        
        for lic in licenses:
            # Check process points
            licensed_process = lic.get('PROCESSPOINTS', 0)
            # Note: Actual usage would come from utilization_input.csv
            # For now, flag any system with significant capacity
            
            if licensed_process >= excess_points_absolute:
                candidates.append({
                    'cluster': lic.get('cluster'),
                    'msid': lic.get('msid'),
                    'system_number': lic.get('system_number'),
                    'licensed_process_points': licensed_process,
                    'excess_points': licensed_process,  # Placeholder
                    'excess_percent': 100,  # Placeholder
                    'cost_value': self.calculate_item_cost('PROCESSPOINTS', licensed_process)['total_cost']
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
