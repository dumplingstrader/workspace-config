"""
Usage data model - Represents actual license usage from CSV files.

This module defines UsageData for tracking how many licenses are
actively in use on each system.
"""

from dataclasses import dataclass
from typing import Optional
from v2.models.license import ValidationError


@dataclass(frozen=True)
class UsageData:
    """
    Immutable usage record from CSV file.
    
    Represents actual license consumption for a single license type
    on a specific system.
    
    Attributes:
        msid: System identifier (must match LicenseData.msid)
        license_type: Type of license being used (e.g., 'PROCESSPOINTS')
        used_quantity: Number of licenses actively in use
        cluster: Optional site location for verification
        file_path: Source CSV file for error tracing
    
    Examples:
        >>> usage = UsageData(
        ...     msid='M0614',
        ...     license_type='PROCESSPOINTS',
        ...     used_quantity=108
        ... )
        >>> usage.msid
        'M0614'
    """
    
    # Required fields
    msid: str
    license_type: str
    used_quantity: int
    
    # Optional fields
    cluster: Optional[str] = None
    system_name: Optional[str] = None  # System name from CSV filename (ESVT0, HCU, etc.)
    file_path: Optional[str] = None
    
    def __post_init__(self):
        """
        Validate usage data at construction time.
        
        Raises:
            ValidationError: If validation fails
        
        Validation Rules:
        1. MSID must not be empty
        2. License type must not be empty
        3. Used quantity must be non-negative
        """
        
        # MSID required for matching
        if not self.msid:
            raise ValidationError(
                f"MSID required for usage data from {self.file_path}"
            )
        
        # License type required
        if not self.license_type:
            raise ValidationError(
                f"License type required for usage from {self.msid}"
            )
        
        # Quantity must be non-negative
        if self.used_quantity < 0:
            raise ValidationError(
                f"Used quantity cannot be negative: {self.used_quantity} "
                f"for {self.msid}/{self.license_type}"
            )
    
    @property
    def match_key(self) -> tuple:
        """
        Key for matching usage to license data.
        
        Returns:
            Tuple of (msid, license_type)
        """
        return (self.msid, self.license_type)
    
    def to_dict(self) -> dict:
        """Serialize to dictionary for JSON export"""
        return {
            'msid': self.msid,
            'license_type': self.license_type,
            'used_quantity': self.used_quantity,
            'cluster': self.cluster,
            'file_path': self.file_path
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'UsageData':
        """Deserialize from dictionary"""
        return cls(**data)
