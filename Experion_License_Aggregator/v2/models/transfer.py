"""
Transfer candidate model - Represents systems with excess licenses.

This module defines TransferCandidate for identifying licenses that
could be transferred to other systems.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class TransferCandidate:
    """
    Immutable transfer candidate record.
    
    Represents a system with excess licenses that could be transferred
    to other systems, along with the financial value of the excess.
    
    Attributes:
        msid: System identifier
        system_number: License number
        cluster: Site location
        license_type: Type of license with excess
        licensed_quantity: Total licensed amount
        used_quantity: Actually used amount
        excess_quantity: Unused amount (licensed - used)
        excess_value: Dollar value of excess (excess * unit_price)
        unit_price: Price per license
        priority: Priority level ('HIGH', 'MEDIUM', 'LOW')
        notes: Optional explanatory notes
    
    Examples:
        >>> transfer = TransferCandidate(
        ...     msid='M0614',
        ...     system_number='60806',
        ...     cluster='Carson',
        ...     license_type='PROCESSPOINTS',
        ...     licensed_quantity=4750,
        ...     used_quantity=108,
        ...     excess_quantity=4642,
        ...     excess_value=208890.00,
        ...     unit_price=45.00,
        ...     priority='HIGH'
        ... )
        >>> transfer.utilization_percentage()
        2.27
    """
    
    # Identity
    msid: str
    system_number: str
    cluster: str
    license_type: str
    
    # Quantities
    licensed_quantity: int
    used_quantity: int
    excess_quantity: int
    
    # Financial
    excess_value: float
    unit_price: float
    
    # Metadata
    priority: str  # HIGH, MEDIUM, LOW
    notes: Optional[str] = None
    
    def utilization_percentage(self) -> float:
        """
        Calculate utilization percentage.
        
        Returns:
            Percentage of licensed quantity actually used (0-100)
        
        Example:
            >>> transfer.utilization_percentage()
            2.27  # 108/4750 * 100
        """
        if self.licensed_quantity == 0:
            return 0.0
        
        return round((self.used_quantity / self.licensed_quantity) * 100, 2)
    
    @property
    def excess_percentage(self) -> float:
        """Calculate percentage that is excess (inverse of utilization)"""
        return round(100.0 - self.utilization_percentage(), 2)
    
    @property
    def is_high_value(self) -> bool:
        """Check if excess value is significant (>$50k)"""
        return self.excess_value > 50000
    
    def to_dict(self) -> dict:
        """Serialize to dictionary"""
        return {
            'msid': self.msid,
            'system_number': self.system_number,
            'cluster': self.cluster,
            'license_type': self.license_type,
            'licensed_quantity': self.licensed_quantity,
            'used_quantity': self.used_quantity,
            'excess_quantity': self.excess_quantity,
            'excess_value': self.excess_value,
            'unit_price': self.unit_price,
            'priority': self.priority,
            'notes': self.notes,
            'utilization_percentage': self.utilization_percentage(),
            'excess_percentage': self.excess_percentage
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'TransferCandidate':
        """Deserialize from dictionary"""
        # Remove computed fields if present
        data = {k: v for k, v in data.items() 
                if k not in ['utilization_percentage', 'excess_percentage']}
        return cls(**data)
