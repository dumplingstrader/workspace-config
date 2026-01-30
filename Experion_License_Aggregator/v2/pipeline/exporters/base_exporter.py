"""
Base exporter for V2.0 pipeline.

Provides abstract export interface and result container.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from datetime import datetime
from pathlib import Path


@dataclass
class ExportResult:
    """
    Result of export operation.
    
    Contains export outcome with file paths and statistics.
    
    Attributes:
        success: Whether export succeeded
        output_path: Path to exported file
        format: Export format ('json', 'xlsx', etc.)
        record_count: Number of records exported
        errors: List of error messages
        warnings: List of warning messages
        export_time: When export occurred
        metadata: Additional export metadata
    """
    
    success: bool
    output_path: Optional[Path] = None
    format: str = ""
    record_count: int = 0
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    export_time: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate result consistency"""
        if self.success and self.errors:
            raise ValueError("ExportResult with errors cannot have success=True")
        
        if not self.success and not self.errors:
            raise ValueError("Failed ExportResult must have at least one error")
    
    @property
    def has_warnings(self) -> bool:
        """Check if result has warnings"""
        return len(self.warnings) > 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary"""
        return {
            'success': self.success,
            'output_path': str(self.output_path) if self.output_path else None,
            'format': self.format,
            'record_count': self.record_count,
            'errors': self.errors,
            'warnings': self.warnings,
            'export_time': self.export_time.isoformat(),
            'metadata': self.metadata
        }


class BaseExporter(ABC):
    """
    Abstract base class for exporters.
    
    All exporters must implement export() method.
    Provides helper methods for common export operations.
    """
    
    def __init__(self, output_dir: Optional[Path] = None):
        """
        Initialize exporter.
        
        Args:
            output_dir: Directory for exported files (None = current directory)
        """
        self.output_dir = output_dir or Path.cwd()
        self._ensure_output_dir()
    
    def _ensure_output_dir(self) -> None:
        """Create output directory if it doesn't exist"""
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    @abstractmethod
    def export(self, data: Any, filename: str, **options) -> ExportResult:
        """
        Export data to file.
        
        Args:
            data: Data to export
            filename: Output filename
            **options: Format-specific export options
            
        Returns:
            ExportResult with success status and file path
            
        Raises:
            NotImplementedError: Must be implemented by subclass
        """
        raise NotImplementedError("Subclasses must implement export()")
    
    def _create_success_result(
        self,
        output_path: Path,
        format: str,
        record_count: int,
        **metadata
    ) -> ExportResult:
        """
        Create successful export result.
        
        Args:
            output_path: Path to exported file
            format: Export format
            record_count: Number of records exported
            **metadata: Additional metadata
            
        Returns:
            ExportResult with success=True
        """
        return ExportResult(
            success=True,
            output_path=output_path,
            format=format,
            record_count=record_count,
            metadata=metadata
        )
    
    def _create_error_result(
        self,
        format: str,
        error_message: str,
        **metadata
    ) -> ExportResult:
        """
        Create failed export result.
        
        Args:
            format: Export format
            error_message: Error description
            **metadata: Additional metadata
            
        Returns:
            ExportResult with success=False
        """
        return ExportResult(
            success=False,
            format=format,
            errors=[error_message],
            metadata=metadata
        )
