"""
Exception hierarchy for V2.0 processing pipeline.

All custom exceptions inherit from DataverseBaseError for easy catching.
Specific exceptions provide context for error handling and logging.
"""


class DataverseBaseError(Exception):
    """Base exception for all V2.0 errors"""
    pass


# ============================================================================
# Data Extraction Errors
# ============================================================================

class DataExtractionError(DataverseBaseError):
    """Base class for extraction errors (XML/CSV parsing)"""
    
    def __init__(self, message: str, file_path: str = None):
        self.file_path = file_path
        super().__init__(f"{message} (file: {file_path})" if file_path else message)


class XmlParsingError(DataExtractionError):
    """Raised when XML parsing fails"""
    pass


class CsvParsingError(DataExtractionError):
    """Raised when CSV parsing fails"""
    pass


# ============================================================================
# Data Validation Errors
# ============================================================================

class DataValidationError(DataverseBaseError):
    """Base class for validation errors"""
    
    def __init__(self, message: str, field: str = None, value=None):
        self.field = field
        self.value = value
        detail = f" (field: {field}, value: {value})" if field else ""
        super().__init__(f"{message}{detail}")


class SchemaValidationError(DataValidationError):
    """Raised when data doesn't match expected schema"""
    pass


class BusinessRuleError(DataValidationError):
    """Raised when business rule validation fails"""
    pass


class MatchingError(DataverseBaseError):
    """Raised when license-usage matching fails"""
    pass


# ============================================================================
# Configuration Errors
# ============================================================================

class ConfigurationError(DataverseBaseError):
    """Base class for configuration errors"""
    pass


class MissingConfigError(ConfigurationError):
    """Raised when required configuration is missing"""
    
    def __init__(self, key: str, config_file: str = None):
        self.key = key
        self.config_file = config_file
        message = f"Missing required configuration: {key}"
        if config_file:
            message += f" in {config_file}"
        super().__init__(message)


class InvalidConfigError(ConfigurationError):
    """Raised when configuration is invalid"""
    pass


# ============================================================================
# Processing Errors
# ============================================================================

class ProcessingError(DataverseBaseError):
    """Base class for processing/transformation errors"""
    pass


class DeduplicationError(ProcessingError):
    """Raised during deduplication process"""
    pass


class CostCalculationError(ProcessingError):
    """Raised during cost calculation"""
    pass


class TransferDetectionError(ProcessingError):
    """Raised during transfer candidate detection"""
    pass


# ============================================================================
# Export Errors
# ============================================================================

class ExportError(DataverseBaseError):
    """Base class for export errors"""
    pass


class ExcelExportError(ExportError):
    """Raised during Excel file generation"""
    pass


class JsonExportError(ExportError):
    """Raised during JSON export"""
    pass


# ============================================================================
# Utility Functions
# ============================================================================

def format_error_context(error: Exception, context: dict = None) -> dict:
    """
    Format exception with context for logging.
    
    Args:
        error: The exception to format
        context: Additional context dictionary
    
    Returns:
        Dictionary with error details for structured logging
    """
    error_info = {
        'type': error.__class__.__name__,
        'message': str(error),
        'base_type': error.__class__.__bases__[0].__name__
    }
    
    # Add specific attributes if present
    if hasattr(error, 'file_path'):
        error_info['file_path'] = error.file_path
    if hasattr(error, 'field'):
        error_info['field'] = error.field
    if hasattr(error, 'value'):
        error_info['value'] = error.value
    if hasattr(error, 'key'):
        error_info['key'] = error.key
    if hasattr(error, 'config_file'):
        error_info['config_file'] = error.config_file
    
    if context:
        error_info['context'] = context
    
    return error_info
