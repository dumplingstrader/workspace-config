"""
License data model - Immutable representation of an Experion system license.

This module defines the core LicenseData dataclass and related types.
All licenses are immutable (frozen=True) to prevent accidental modification
after validation.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Optional, Tuple
from enum import Enum


class LicenseType(Enum):
    """
    Supported license types from Experion XML and CSV files.
    
    Note: DIRECTSTATIONS (XML) and CONSOLE_STATIONS (CSV) are treated
    as synonyms during field mapping.
    """
    PROCESSPOINTS = "PROCESSPOINTS"
    SCADAPOINTS = "SCADAPOINTS"
    STATIONS = "STATIONS"
    MULTISTATIONS = "MULTISTATIONS"
    DIRECTSTATIONS = "DIRECTSTATIONS"
    CONSOLE_STATIONS = "CONSOLE_STATIONS"
    DUAL = "DUAL"
    DAS = "DAS"
    API = "API"
    SQL = "SQL"
    HISTORIAN = "HISTORIAN"
    REPORTING = "REPORTING"
    ADVANCED = "ADVANCED"
    BATCH = "BATCH"
    CONTROLLER = "CONTROLLER"


class ValidationError(Exception):
    """Raised when data model validation fails during construction"""
    pass


@dataclass(frozen=True)
class LicenseData:
    """
    Immutable license record extracted from XML file.
    
    Represents a single Experion system's license configuration.
    Validation occurs at construction time (__post_init__) to fail fast.
    
    Attributes:
        msid: System identifier (e.g., 'M0614', 'M0615')
        system_number: 5-6 digit license number (e.g., '60806')
        cluster: Site location ('Carson', 'Wilmington')
        release: Experion version (e.g., 'R520', 'R511.6')
        product: System type ('PKS', 'HS', 'EAS'), defaults to 'PKS'
        license_date: Date license was issued (optional)
        customer: Customer name (should contain 'Marathon' or 'MPC')
        file_version: Version number from filename suffix (_v40 → 40)
        file_path: Original XML file path for error tracing
        licensed: Dictionary mapping license type to quantity
    
    Examples:
        >>> license = LicenseData(
        ...     msid='M0614',
        ...     system_number='60806',
        ...     cluster='Carson',
        ...     release='R520',
        ...     licensed={'PROCESSPOINTS': 4750}
        ... )
        >>> license.unique_key
        ('Carson', 'M0614', '60806')
        >>> license.get_licensed_quantity('PROCESSPOINTS')
        4750
    """
    
    # Identity fields (required)
    msid: str
    system_number: str
    cluster: str
    release: str
    
    # Metadata fields (optional with defaults)
    product: str = 'PKS'
    license_date: Optional[datetime] = None
    customer: Optional[str] = None
    file_version: int = 0
    file_path: Optional[str] = None
    system_name: Optional[str] = None  # System name (ESVT0, HCU, ALKY, etc.) from folder
    
    # License quantities (mutable dict frozen via immutability)
    licensed: Dict[str, int] = field(default_factory=dict)
    
    def __post_init__(self):
        """
        Validate data integrity at construction time.
        
        Raises:
            ValidationError: If any validation rule fails
        
        Validation Rules:
        1. MSID must exist and not be 'Unknown' (common parsing failure)
        2. System number must be numeric
        3. Cluster must not be empty
        4. File version must be non-negative
        """
        
        # Critical: MSID must exist and be valid
        if not self.msid or self.msid == 'Unknown':
            raise ValidationError(
                f"Invalid MSID: '{self.msid}' in file {self.file_path}"
            )
        
        # System number must be numeric (enforces data type)
        if not self.system_number.isdigit():
            raise ValidationError(
                f"System number must be numeric: '{self.system_number}' "
                f"for {self.msid}"
            )
        
        # Cluster required for proper grouping
        if not self.cluster:
            raise ValidationError(
                f"Cluster required for {self.msid}/{self.system_number}"
            )
        
        # Version sanity check
        if self.file_version < 0:
            raise ValidationError(
                f"File version cannot be negative: {self.file_version}"
            )
    
    @property
    def unique_key(self) -> Tuple[str, str, str]:
        """
        Canonical identifier for deduplication.
        
        Returns:
            Tuple of (cluster, msid, system_number)
        
        Note:
            This key is used to detect duplicate systems across different
            file versions. The highest file_version wins during deduplication.
        """
        return (self.cluster, self.msid, self.system_number)
    
    @property
    def display_name(self) -> str:
        """
        Human-readable system name for reports.
        
        Returns:
            Formatted string like "M0614/60806 (Carson)"
        """
        return f"{self.msid}/{self.system_number} ({self.cluster})"
    
    def get_licensed_quantity(self, license_type: str) -> int:
        """
        Safely retrieve licensed quantity for a specific type.
        
        Args:
            license_type: License type name (e.g., 'PROCESSPOINTS')
        
        Returns:
            Quantity if exists, otherwise 0
        
        Example:
            >>> license.get_licensed_quantity('PROCESSPOINTS')
            4750
            >>> license.get_licensed_quantity('NONEXISTENT')
            0
        """
        return self.licensed.get(license_type, 0)
    
    def has_license_type(self, license_type: str) -> bool:
        """
        Check if system has a specific license type with quantity > 0.
        
        Args:
            license_type: License type name
        
        Returns:
            True if license type exists and quantity > 0
        
        Example:
            >>> license.has_license_type('PROCESSPOINTS')
            True
            >>> license.has_license_type('NONEXISTENT')
            False
        """
        return license_type in self.licensed and self.licensed[license_type] > 0
    
    def to_dict(self) -> Dict:
        """
        Serialize to dictionary for JSON export.
        
        Returns:
            Dictionary with all fields, datetime converted to ISO format
        
        Note:
            Use this for creating JSON checkpoints and reports.
        """
        return {
            'msid': self.msid,
            'system_number': self.system_number,
            'cluster': self.cluster,
            'release': self.release,
            'product': self.product,
            'license_date': self.license_date.isoformat() if self.license_date else None,
            'customer': self.customer,
            'file_version': self.file_version,
            'file_path': self.file_path,
            'licensed': self.licensed
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'LicenseData':
        """
        Deserialize from dictionary (inverse of to_dict).
        
        Args:
            data: Dictionary with license fields
        
        Returns:
            New LicenseData instance
        
        Note:
            Handles ISO datetime string conversion automatically.
        """
        # Convert ISO string back to datetime
        if data.get('license_date'):
            data['license_date'] = datetime.fromisoformat(data['license_date'])
        
        return cls(**data)
