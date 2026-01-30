"""
Data models package - Type-safe structures for license data processing.

This package provides immutable dataclass models with built-in validation
for all stages of the ETL pipeline.

Models:
    LicenseData: Extracted license information from XML
    UsageData: Actual usage from CSV files
    CostCalculation: Computed costs with pricing source
    TransferCandidate: Systems with excess licenses

All models are immutable (frozen=True) and validate data at construction
time to fail fast.
"""

from v2.models.license import LicenseData, LicenseType, ValidationError
from v2.models.usage import UsageData
from v2.models.cost import CostCalculation
from v2.models.transfer import TransferCandidate

__all__ = [
    'LicenseData',
    'LicenseType',
    'UsageData',
    'CostCalculation',
    'TransferCandidate',
    'ValidationError',
]
