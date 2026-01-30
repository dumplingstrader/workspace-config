"""
Base Extractor Module

Defines abstract base class for data extractors with standardized interface.
All extractors (XML, CSV) inherit from this base to ensure consistent behavior.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Generic, TypeVar, List, Optional
from datetime import datetime

from v2.core.exceptions import DataExtractionError
from v2.core.constants import ProcessingStage, ValidationLevel


# Generic type for extraction result data
T = TypeVar('T')


@dataclass(frozen=True)
class ExtractionResult(Generic[T]):
    """
    Result of data extraction operation.
    
    Attributes:
        success: Whether extraction succeeded
        data: Extracted data object (LicenseData or UsageData)
        source_file: Path to source file
        warnings: Non-fatal validation warnings
        errors: Fatal errors (empty if success=True)
        extraction_time: Timestamp of extraction
        stage: Processing stage
    """
    success: bool
    data: Optional[T]
    source_file: Path
    warnings: List[str]
    errors: List[str]
    extraction_time: datetime
    stage: ProcessingStage = ProcessingStage.EXTRACTION
    
    def __post_init__(self):
        """Validate result consistency."""
        if self.success and self.data is None:
            raise ValueError("Successful extraction must have data")
        if not self.success and not self.errors:
            raise ValueError("Failed extraction must have errors")


class BaseExtractor(ABC):
    """
    Abstract base class for data extractors.
    
    Enforces consistent interface across all extractor implementations
    (XML parser, CSV parser, etc.).
    """
    
    def __init__(self, strict_mode: bool = False):
        """
        Initialize extractor.
        
        Args:
            strict_mode: If True, treat warnings as errors
        """
        self.strict_mode = strict_mode
        self.warnings: List[str] = []
        self.errors: List[str] = []
    
    @abstractmethod
    def extract_from_file(self, file_path: Path) -> ExtractionResult[T]:
        """
        Extract data from file.
        
        Args:
            file_path: Path to source file
            
        Returns:
            ExtractionResult with data or errors
            
        Raises:
            DataExtractionError: If file cannot be read or parsed
        """
        pass
    
    @abstractmethod
    def can_handle(self, file_path: Path) -> bool:
        """
        Check if extractor can handle this file type.
        
        Args:
            file_path: Path to check
            
        Returns:
            True if extractor supports this file format
        """
        pass
    
    @abstractmethod
    def validate_structure(self, file_path: Path) -> bool:
        """
        Validate file structure before extraction.
        
        Args:
            file_path: Path to validate
            
        Returns:
            True if file structure is valid
            
        Raises:
            DataExtractionError: If structure validation fails
        """
        pass
    
    def _add_warning(self, message: str, level: ValidationLevel = ValidationLevel.WARNING):
        """
        Add warning message.
        
        Args:
            message: Warning message
            level: Severity level
        """
        formatted = f"[{level.name}] {message}"
        self.warnings.append(formatted)
        
        if self.strict_mode and level == ValidationLevel.ERROR:
            raise DataExtractionError(formatted)
    
    def _add_error(self, message: str):
        """
        Add error message.
        
        Args:
            message: Error message
        """
        self.errors.append(f"[ERROR] {message}")
    
    def _create_success_result(self, data: T, source_file: Path) -> ExtractionResult[T]:
        """
        Create successful extraction result.
        
        Args:
            data: Extracted data
            source_file: Source file path
            
        Returns:
            ExtractionResult with success=True
        """
        return ExtractionResult(
            success=True,
            data=data,
            source_file=source_file,
            warnings=self.warnings.copy(),
            errors=[],
            extraction_time=datetime.now()
        )
    
    def _create_failure_result(self, source_file: Path) -> ExtractionResult[T]:
        """
        Create failed extraction result.
        
        Args:
            source_file: Source file path
            
        Returns:
            ExtractionResult with success=False
        """
        return ExtractionResult(
            success=False,
            data=None,
            source_file=source_file,
            warnings=self.warnings.copy(),
            errors=self.errors.copy(),
            extraction_time=datetime.now()
        )
    
    def reset(self):
        """Reset warning and error state for next extraction."""
        self.warnings.clear()
        self.errors.clear()
