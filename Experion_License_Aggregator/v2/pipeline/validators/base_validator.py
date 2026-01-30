"""
Base validator for V2.0 pipeline.

Provides abstract validation interface and result container.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional, Any
from datetime import datetime
from enum import Enum


class ValidationLevel(Enum):
    """Severity level for validation issues"""
    INFO = 1
    WARNING = 2
    ERROR = 3


@dataclass
class ValidationResult:
    """
    Result of validation operation.
    
    Contains validation outcome with categorized issues.
    
    Attributes:
        passed: Whether validation succeeded
        errors: List of error messages (block processing)
        warnings: List of warning messages (informational)
        info: List of info messages (context)
        validation_time: When validation occurred
        validator_name: Which validator produced this result
    """
    
    passed: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    info: List[str] = field(default_factory=list)
    validation_time: datetime = field(default_factory=datetime.now)
    validator_name: Optional[str] = None
    
    def __post_init__(self):
        """Validate result consistency"""
        # If there are errors, validation must have failed
        if self.errors and self.passed:
            raise ValueError("ValidationResult with errors cannot have passed=True")
        
        # If validation failed, there must be at least one error
        if not self.passed and not self.errors:
            raise ValueError("Failed ValidationResult must have at least one error")
    
    @property
    def has_warnings(self) -> bool:
        """Check if result has warnings"""
        return len(self.warnings) > 0
    
    @property
    def has_errors(self) -> bool:
        """Check if result has errors"""
        return len(self.errors) > 0
    
    @property
    def issue_count(self) -> int:
        """Total number of issues (errors + warnings)"""
        return len(self.errors) + len(self.warnings)
    
    def to_dict(self) -> dict:
        """Serialize to dictionary"""
        return {
            'passed': self.passed,
            'errors': self.errors,
            'warnings': self.warnings,
            'info': self.info,
            'validation_time': self.validation_time.isoformat(),
            'validator_name': self.validator_name,
            'has_warnings': self.has_warnings,
            'has_errors': self.has_errors,
            'issue_count': self.issue_count
        }


class BaseValidator(ABC):
    """
    Abstract base class for validators.
    
    All validators must implement validate() method.
    Provides helper methods for building validation results.
    """
    
    def __init__(self):
        """Initialize validator with empty state"""
        self._errors: List[str] = []
        self._warnings: List[str] = []
        self._info: List[str] = []
    
    @abstractmethod
    def validate(self, data: Any) -> ValidationResult:
        """
        Validate data and return result.
        
        Args:
            data: Data to validate (type depends on validator)
            
        Returns:
            ValidationResult with pass/fail and issues
        """
        pass
    
    def _add_error(self, message: str) -> None:
        """
        Add error message.
        
        Errors indicate validation failure and block processing.
        
        Args:
            message: Error description
        """
        self._errors.append(f"[ERROR] {message}")
    
    def _add_warning(self, message: str) -> None:
        """
        Add warning message.
        
        Warnings indicate potential issues but don't block processing.
        
        Args:
            message: Warning description
        """
        self._warnings.append(f"[WARNING] {message}")
    
    def _add_info(self, message: str) -> None:
        """
        Add info message.
        
        Info messages provide context about validation.
        
        Args:
            message: Info description
        """
        self._info.append(f"[INFO] {message}")
    
    def _create_result(self, passed: bool) -> ValidationResult:
        """
        Create validation result from accumulated issues.
        
        Args:
            passed: Whether validation succeeded
            
        Returns:
            ValidationResult with collected issues
        """
        result = ValidationResult(
            passed=passed,
            errors=self._errors.copy(),
            warnings=self._warnings.copy(),
            info=self._info.copy(),
            validator_name=self.__class__.__name__
        )
        return result
    
    def reset(self) -> None:
        """Clear accumulated validation issues"""
        self._errors.clear()
        self._warnings.clear()
        self._info.clear()
