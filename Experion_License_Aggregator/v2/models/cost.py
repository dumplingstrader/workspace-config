"""
Cost calculation model - Represents computed cost for a license type.

This module defines CostCalculation for tracking pricing and total costs.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class CostCalculation:
    """
    Immutable cost calculation result.
    
    Represents the cost calculation for a single license type on a system.
    
    Attributes:
        msid: System identifier
        system_number: License number
        license_type: Type of license
        licensed_quantity: Number of licenses
        unit_price: Price per license
        total_cost: Total cost (quantity * price)
        price_source: Where price came from ('MPC 2026', 'Honeywell', etc.)
        cluster: Optional site location
    
    Examples:
        >>> cost = CostCalculation(
        ...     msid='M0614',
        ...     system_number='60806',
        ...     license_type='PROCESSPOINTS',
        ...     licensed_quantity=4750,
        ...     unit_price=45.00,
        ...     total_cost=213750.00,
        ...     price_source='MPC 2026 Confirmed'
        ... )
        >>> cost.total_cost
        213750.0
    """
    
    # Identity
    msid: str
    system_number: str
    license_type: str
    
    # Calculation fields
    licensed_quantity: int
    unit_price: float
    total_cost: float
    price_source: str
    
    # Optional
    cluster: Optional[str] = None
    
    def calculate_total(self) -> float:
        """
        Calculate total cost from quantity and unit price.
        
        Returns:
            Quantity multiplied by unit price
        
        Note:
            This method recalculates from components, useful for verification.
        """
        return self.licensed_quantity * self.unit_price
    
    @property
    def is_confirmed_price(self) -> bool:
        """Check if price is from confirmed MPC 2026 pricing"""
        return 'MPC 2026' in self.price_source
    
    @property
    def is_placeholder(self) -> bool:
        """Check if price is placeholder ($100 default)"""
        return 'Placeholder' in self.price_source
    
    def to_dict(self) -> dict:
        """Serialize to dictionary"""
        return {
            'msid': self.msid,
            'system_number': self.system_number,
            'license_type': self.license_type,
            'licensed_quantity': self.licensed_quantity,
            'unit_price': self.unit_price,
            'total_cost': self.total_cost,
            'price_source': self.price_source,
            'cluster': self.cluster
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'CostCalculation':
        """Deserialize from dictionary"""
        return cls(**data)
