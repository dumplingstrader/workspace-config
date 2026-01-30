"""
Core infrastructure package - Configuration, exceptions, and constants.

This package provides foundational components used throughout the V2.0 pipeline.
"""

from v2.core.config import Config
from v2.core.constants import (
    LicenseType,
    ValidationLevel,
    ProcessingStage,
    PriceSource,
    TransferPriority,
    ExcelSheetName,
)
from v2.core.exceptions import (
    DataverseBaseError,
    DataExtractionError,
    XmlParsingError,
    CsvParsingError,
    DataValidationError,
    SchemaValidationError,
    BusinessRuleError,
    MatchingError,
    ConfigurationError,
    MissingConfigError,
    InvalidConfigError,
    ProcessingError,
    DeduplicationError,
    CostCalculationError,
    TransferDetectionError,
    ExportError,
    ExcelExportError,
    JsonExportError,
    format_error_context,
)

__all__ = [
    # Configuration
    'Config',
    
    # Enums
    'LicenseType',
    'ValidationLevel',
    'ProcessingStage',
    'PriceSource',
    'TransferPriority',
    'ExcelSheetName',
    
    # Exceptions
    'DataverseBaseError',
    'DataExtractionError',
    'XmlParsingError',
    'CsvParsingError',
    'DataValidationError',
    'SchemaValidationError',
    'BusinessRuleError',
    'MatchingError',
    'ConfigurationError',
    'MissingConfigError',
    'InvalidConfigError',
    'ProcessingError',
    'DeduplicationError',
    'CostCalculationError',
    'TransferDetectionError',
    'ExportError',
    'ExcelExportError',
    'JsonExportError',
    'format_error_context',
]
