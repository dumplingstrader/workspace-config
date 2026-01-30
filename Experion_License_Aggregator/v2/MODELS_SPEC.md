# Data Models Specification

**Module**: `v2/models/`  
**Purpose**: Type-safe data structures with built-in validation  
**Testing**: 100% coverage required (critical data layer)

---

## Overview

All data models use Python dataclasses with:
- **Type hints** for all fields
- **Validation** in `__post_init__`
- **Immutability** where appropriate (frozen=True)
- **Serialization** methods (to_dict, from_dict)
- **Rich comparison** for testing

---

## License Data Model

### `models/license.py`

```python
"""
License data model representing a single Experion system license.
Immutable after creation to prevent accidental modification.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Optional, Tuple
from enum import Enum

class LicenseType(Enum):
    """Supported license types from Experion XML"""
    PROCESSPOINTS = "PROCESSPOINTS"
    SCADAPOINTS = "SCADAPOINTS"
    STATIONS = "STATIONS"
    MULTISTATIONS = "MULTISTATIONS"
    DIRECTSTATIONS = "DIRECTSTATIONS"
    CONSOLE_STATIONS = "CONSOLE_STATIONS"  # CSV equivalent
    DUAL = "DUAL"
    DAS = "DAS"
    API = "API"
    SQL = "SQL"
    # ... add all 70+ types

class ValidationError(Exception):
    """Raised when data model validation fails"""
    pass

@dataclass(frozen=True)
class LicenseData:
    """
    Immutable license record from XML file.
    
    Attributes:
        msid: System identifier (e.g., 'M0614')
        system_number: 5-6 digit license number (e.g., '60806')
        cluster: Site location ('Carson', 'Wilmington')
        release: Experion version (e.g., 'R520')
        product: System type ('PKS', 'HS', 'EAS')
        license_date: Date license was issued
        customer: Customer name (should contain 'Marathon' or 'MPC')
        file_version: Version number from filename suffix
        file_path: Original XML file path for tracing
        licensed: Dictionary of licensed quantities by type
    """
    
    # Identity fields
    msid: str
    system_number: str
    cluster: str
    
    # Metadata fields
    release: str
    product: str = 'PKS'  # Default to PKS
    license_date: Optional[datetime] = None
    customer: Optional[str] = None
    file_version: int = 0
    file_path: Optional[str] = None
    
    # License quantities (immutable dict)
    licensed: Dict[str, int] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate data integrity at construction time"""
        
        # Critical validation: MSID must exist and not be 'Unknown'
        if not self.msid or self.msid == 'Unknown':
            raise ValidationError(
                f"Invalid MSID: '{self.msid}' in file {self.file_path}"
            )
        
        # System number must be numeric
        if not self.system_number.isdigit():
            raise ValidationError(
                f"System number must be numeric: '{self.system_number}' "
                f"for {self.msid}"
            )
        
        # Cluster must be recognized
        if not self.cluster:
            raise ValidationError(
                f"Cluster required for {self.msid}/{self.system_number}"
            )
        
        # Version should be positive
        if self.file_version < 0:
            raise ValidationError(
                f"File version cannot be negative: {self.file_version}"
            )
    
    @property
    def unique_key(self) -> Tuple[str, str, str]:
        """
        Canonical identifier for deduplication.
        Returns: (cluster, msid, system_number)
        """
        return (self.cluster, self.msid, self.system_number)
    
    @property
    def display_name(self) -> str:
        """Human-readable system name"""
        return f"{self.msid}/{self.system_number} ({self.cluster})"
    
    def get_licensed_quantity(self, license_type: str) -> int:
        """
        Safely get licensed quantity for a type.
        Returns 0 if type not found.
        """
        return self.licensed.get(license_type, 0)
    
    def has_license_type(self, license_type: str) -> bool:
        """Check if system has a specific license type"""
        return license_type in self.licensed and self.licensed[license_type] > 0
    
    def to_dict(self) -> Dict:
        """Serialize to dictionary for JSON export"""
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
        """Deserialize from dictionary"""
        if data.get('license_date'):
            data['license_date'] = datetime.fromisoformat(data['license_date'])
        return cls(**data)
```

### **Test Requirements**

```python
# tests/test_models.py

def test_license_data_creation():
    """Test valid license creation"""
    license = LicenseData(
        msid='M0614',
        system_number='60806',
        cluster='Carson',
        release='R520',
        file_version=40,
        licensed={'PROCESSPOINTS': 4750, 'SCADAPOINTS': 5750}
    )
    
    assert license.unique_key == ('Carson', 'M0614', '60806')
    assert license.display_name == 'M0614/60806 (Carson)'
    assert license.get_licensed_quantity('PROCESSPOINTS') == 4750
    assert license.has_license_type('SCADAPOINTS') == True

def test_license_validation_rejects_empty_msid():
    """Test validation catches empty MSID"""
    with pytest.raises(ValidationError, match="Invalid MSID"):
        LicenseData(
            msid='',
            system_number='60806',
            cluster='Carson',
            release='R520'
        )

def test_license_validation_rejects_unknown_msid():
    """Test validation catches 'Unknown' MSID"""
    with pytest.raises(ValidationError, match="Invalid MSID"):
        LicenseData(
            msid='Unknown',
            system_number='60806',
            cluster='Carson',
            release='R520'
        )

def test_license_validation_rejects_non_numeric_system_number():
    """Test validation catches invalid system number"""
    with pytest.raises(ValidationError, match="System number must be numeric"):
        LicenseData(
            msid='M0614',
            system_number='ABC123',
            cluster='Carson',
            release='R520'
        )

def test_license_serialization():
    """Test to_dict and from_dict roundtrip"""
    original = LicenseData(
        msid='M0614',
        system_number='60806',
        cluster='Carson',
        release='R520',
        license_date=datetime(2024, 1, 15),
        licensed={'PROCESSPOINTS': 4750}
    )
    
    data = original.to_dict()
    restored = LicenseData.from_dict(data)
    
    assert restored.unique_key == original.unique_key
    assert restored.license_date == original.license_date
```

---

## Usage Data Model

### `models/usage.py`

```python
"""
Usage data model from Station Manager CSV exports.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Optional, Tuple

@dataclass
class UsageData:
    """
    Actual utilization data from Experion Station Manager.
    
    Attributes:
        msid: System identifier (must match LicenseData)
        system_number: License number (must match LicenseData)
        cluster: Site location (must match LicenseData)
        as_of_date: Date usage was collected
        usage: Dictionary of actual usage by type
        source_file: CSV file path for tracing
    """
    
    # Identity (must match LicenseData for merging)
    msid: str
    system_number: str
    cluster: str
    
    # Usage data
    as_of_date: Optional[datetime] = None
    usage: Dict[str, int] = field(default_factory=dict)
    source_file: Optional[str] = None
    
    @property
    def unique_key(self) -> Tuple[str, str, str]:
        """Matching key for LicenseData.unique_key"""
        return (self.cluster, self.msid, self.system_number)
    
    def get_usage(self, license_type: str) -> int:
        """Safely get usage for a type. Returns 0 if not found."""
        return self.usage.get(license_type, 0)
    
    def to_dict(self) -> Dict:
        """Serialize to dictionary"""
        return {
            'msid': self.msid,
            'system_number': self.system_number,
            'cluster': self.cluster,
            'as_of_date': self.as_of_date.isoformat() if self.as_of_date else None,
            'usage': self.usage,
            'source_file': self.source_file
        }
```

---

## Enriched License Model

### `models/enriched_license.py`

```python
"""
Enriched license with usage, costs, and analysis.
"""

from dataclasses import dataclass
from typing import Optional
from .license import LicenseData
from .usage import UsageData
from .cost import CostCalculation

@dataclass
class EnrichedLicense:
    """
    License + usage + cost + analysis.
    Created by transformation pipeline.
    """
    
    license: LicenseData
    usage: Optional[UsageData] = None
    cost: Optional[CostCalculation] = None
    match_confidence: float = 0.0  # 0.0 to 1.0
    match_method: str = 'none'  # 'exact', 'fuzzy_msid', 'none'
    
    def get_utilization(self, license_type: str) -> Optional[float]:
        """
        Calculate utilization percentage for a license type.
        Returns None if no usage data available.
        """
        if not self.usage:
            return None
        
        licensed = self.license.get_licensed_quantity(license_type)
        if licensed == 0:
            return None
        
        used = self.usage.get_usage(license_type)
        return (used / licensed) * 100.0
    
    def get_excess(self, license_type: str) -> Optional[int]:
        """Get excess capacity (licensed - used)"""
        if not self.usage:
            return None
        
        licensed = self.license.get_licensed_quantity(license_type)
        used = self.usage.get_usage(license_type)
        return licensed - used
    
    @property
    def has_usage_data(self) -> bool:
        """Check if usage data is available"""
        return self.usage is not None and self.match_confidence > 0.0
```

---

## Cost Calculation Model

### `models/cost.py`

```python
"""
Cost calculation results with audit trail.
"""

from dataclasses import dataclass, field
from typing import Dict, List
from enum import Enum

class PricingSource(Enum):
    """Source of pricing data"""
    MPC_2026 = "MPC 2026 Confirmed"
    HONEYWELL_BASELINE = "Honeywell Baseline"
    PLACEHOLDER = "Placeholder"

@dataclass
class CostLineItem:
    """Single cost calculation for a license type"""
    license_type: str
    quantity: int
    unit_cost: float
    per: int  # Increment (e.g., 50 for PROCESSPOINTS)
    total_cost: float
    source: PricingSource
    
    def to_dict(self) -> Dict:
        return {
            'license_type': self.license_type,
            'quantity': self.quantity,
            'unit_cost': self.unit_cost,
            'per': self.per,
            'total_cost': self.total_cost,
            'source': self.source.value
        }

@dataclass
class CostCalculation:
    """
    Complete cost breakdown for a license.
    Includes audit trail of pricing sources.
    """
    
    total_cost: float
    breakdown: Dict[str, CostLineItem] = field(default_factory=dict)
    
    def add_line_item(self, item: CostLineItem):
        """Add a cost line item"""
        self.breakdown[item.license_type] = item
    
    def get_cost_by_source(self, source: PricingSource) -> float:
        """Sum costs from a specific pricing source"""
        return sum(
            item.total_cost 
            for item in self.breakdown.values() 
            if item.source == source
        )
    
    def to_dict(self) -> Dict:
        return {
            'total_cost': self.total_cost,
            'breakdown': {k: v.to_dict() for k, v in self.breakdown.items()}
        }
```

---

## Transfer Candidate Model

### `models/transfer.py`

```python
"""
Transfer candidate identification results.
"""

from dataclasses import dataclass

@dataclass
class TransferCandidate:
    """
    System with excess capacity available for transfer.
    """
    
    cluster: str
    system_name: str
    msid: str
    system_number: str
    license_type: str
    
    licensed: int
    used: int
    excess: int
    utilization_percent: float
    excess_value: float
    
    has_usage_data: bool
    
    def meets_absolute_threshold(self, threshold: int) -> bool:
        """Check if excess meets absolute threshold"""
        return self.excess >= threshold
    
    def meets_percent_threshold(self, threshold: float) -> bool:
        """Check if utilization is below threshold"""
        return self.utilization_percent <= (100 - threshold)
    
    def meets_value_threshold(self, threshold: float) -> bool:
        """Check if excess value meets minimum"""
        return self.excess_value >= threshold
    
    def to_dict(self) -> Dict:
        return {
            'cluster': self.cluster,
            'system_name': self.system_name,
            'msid': self.msid,
            'system_number': self.system_number,
            'license_type': self.license_type,
            'licensed': self.licensed,
            'used': self.used,
            'excess': self.excess,
            'utilization_percent': self.utilization_percent,
            'excess_value': self.excess_value,
            'has_usage_data': self.has_usage_data
        }
```

---

## Module Exports

### `models/__init__.py`

```python
"""
Data models for Experion License Aggregator V2.
All models include validation and serialization.
"""

from .license import LicenseData, LicenseType, ValidationError
from .usage import UsageData
from .enriched_license import EnrichedLicense
from .cost import CostCalculation, CostLineItem, PricingSource
from .transfer import TransferCandidate

__all__ = [
    'LicenseData',
    'LicenseType',
    'ValidationError',
    'UsageData',
    'EnrichedLicense',
    'CostCalculation',
    'CostLineItem',
    'PricingSource',
    'TransferCandidate'
]
```

---

## Agent Implementation Checklist

- [ ] Create all model files in `v2/models/`
- [ ] Add type hints to all fields
- [ ] Implement `__post_init__` validation
- [ ] Add docstrings (Google style)
- [ ] Create `to_dict()` and `from_dict()` methods
- [ ] Write unit tests for each model (100% coverage)
- [ ] Test validation catches all error cases
- [ ] Test serialization roundtrip
- [ ] Update `__init__.py` with exports
- [ ] Run `pytest tests/test_models.py --cov=v2/models`
