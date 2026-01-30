"""
JSON exporter for V2.0 pipeline.

Exports license, cost, and transfer data to structured JSON files.
"""

import json
from typing import List, Dict, Any, Union, Optional
from pathlib import Path
from datetime import datetime
from dataclasses import asdict, is_dataclass

from v2.pipeline.exporters.base_exporter import BaseExporter, ExportResult
from v2.models.license import LicenseData
from v2.models.usage import UsageData
from v2.models.cost import CostCalculation
from v2.models.transfer import TransferCandidate


class JsonExporter(BaseExporter):
    """
    Exports data to JSON format with custom serialization.
    
    Handles dataclass serialization, datetime formatting, and
    nested structure organization.
    
    Supports:
    - Single records
    - Lists of records
    - Nested dictionaries with metadata
    - Custom indentation and formatting
    
    Examples:
        >>> exporter = JsonExporter(output_dir=Path('output'))
        >>> result = exporter.export(licenses, 'licenses.json')
        >>> assert result.success
        >>> assert result.output_path.exists()
    """
    
    def __init__(
        self,
        output_dir: Optional[Path] = None,
        indent: int = 2,
        ensure_ascii: bool = False
    ):
        """
        Initialize JSON exporter.
        
        Args:
            output_dir: Directory for exported files
            indent: JSON indentation (0 = compact, 2+ = pretty)
            ensure_ascii: Whether to escape non-ASCII characters
        """
        super().__init__(output_dir)
        self.indent = indent
        self.ensure_ascii = ensure_ascii
    
    def export(
        self,
        data: Union[List[Any], Dict[str, Any], Any],
        filename: str,
        **options
    ) -> ExportResult:
        """
        Export data to JSON file.
        
        Args:
            data: Data to export (list of dataclasses, dict, or single item)
            filename: Output filename (without .json extension if not present)
            **options: Additional JSON options (indent, ensure_ascii)
            
        Returns:
            ExportResult with success status and file path
        """
        try:
            # Ensure filename has .json extension
            if not filename.endswith('.json'):
                filename = f"{filename}.json"
            
            output_path = self.output_dir / filename
            
            # Convert data to JSON-serializable format
            json_data = self._serialize_data(data)
            
            # Get JSON options
            indent = options.get('indent', self.indent)
            ensure_ascii = options.get('ensure_ascii', self.ensure_ascii)
            
            # Write JSON file
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(
                    json_data,
                    f,
                    indent=indent if indent > 0 else None,
                    ensure_ascii=ensure_ascii,
                    default=self._json_serializer
                )
            
            # Calculate record count
            record_count = self._count_records(json_data)
            
            return self._create_success_result(
                output_path=output_path,
                format='json',
                record_count=record_count,
                indent=indent,
                file_size=output_path.stat().st_size
            )
            
        except Exception as e:
            return self._create_error_result(
                format='json',
                error_message=f"JSON export failed: {str(e)}",
                filename=filename
            )
    
    def export_summary(
        self,
        licenses: List[LicenseData],
        costs: List[CostCalculation],
        transfers: List[TransferCandidate],
        filename: str = "summary.json",
        **metadata
    ) -> ExportResult:
        """
        Export comprehensive summary with all data types.
        
        Args:
            licenses: List of LicenseData
            costs: List of CostCalculation
            transfers: List of TransferCandidate
            filename: Output filename
            **metadata: Additional metadata to include
            
        Returns:
            ExportResult with success status
        """
        try:
            summary = {
                'export_metadata': {
                    'export_time': datetime.now().isoformat(),
                    'license_count': len(licenses),
                    'cost_count': len(costs),
                    'transfer_count': len(transfers),
                    **metadata
                },
                'licenses': [self._dataclass_to_dict(lic) for lic in licenses],
                'costs': [self._dataclass_to_dict(cost) for cost in costs],
                'transfers': [self._dataclass_to_dict(xfer) for xfer in transfers],
                'statistics': self._calculate_statistics(licenses, costs, transfers)
            }
            
            return self.export(summary, filename)
            
        except Exception as e:
            return self._create_error_result(
                format='json',
                error_message=f"Summary export failed: {str(e)}",
                filename=filename
            )
    
    def _serialize_data(self, data: Any) -> Any:
        """
        Convert data to JSON-serializable format.
        
        Args:
            data: Input data
            
        Returns:
            JSON-serializable version of data
        """
        if is_dataclass(data) and not isinstance(data, type):
            return self._dataclass_to_dict(data)
        elif isinstance(data, list):
            return [self._serialize_data(item) for item in data]
        elif isinstance(data, dict):
            return {key: self._serialize_data(value) for key, value in data.items()}
        else:
            return data
    
    def _dataclass_to_dict(self, obj: Any) -> Dict[str, Any]:
        """
        Convert dataclass to dictionary with custom handling.
        
        Args:
            obj: Dataclass instance
            
        Returns:
            Dictionary representation
        """
        if not is_dataclass(obj):
            return obj
        
        result = {}
        for key, value in asdict(obj).items():
            if isinstance(value, datetime):
                result[key] = value.isoformat()
            elif isinstance(value, Path):
                result[key] = str(value)
            elif isinstance(value, dict):
                result[key] = value
            elif is_dataclass(value):
                result[key] = self._dataclass_to_dict(value)
            else:
                result[key] = value
        
        return result
    
    def _json_serializer(self, obj: Any) -> Any:
        """
        Custom JSON serializer for non-standard types.
        
        Args:
            obj: Object to serialize
            
        Returns:
            Serializable version of object
        """
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, Path):
            return str(obj)
        elif hasattr(obj, '__dict__'):
            return obj.__dict__
        else:
            return str(obj)
    
    def _count_records(self, data: Any) -> int:
        """
        Count records in exported data.
        
        Args:
            data: JSON data structure
            
        Returns:
            Number of records
        """
        if isinstance(data, list):
            return len(data)
        elif isinstance(data, dict):
            # Look for common list keys
            for key in ['licenses', 'costs', 'transfers', 'data', 'records']:
                if key in data and isinstance(data[key], list):
                    return len(data[key])
            # Count total items in all lists
            total = 0
            for value in data.values():
                if isinstance(value, list):
                    total += len(value)
            # If no lists found but dict has content, count as 1 record
            if total == 0 and data:
                return 1
            return total
        else:
            return 1
    
    def _calculate_statistics(
        self,
        licenses: List[LicenseData],
        costs: List[CostCalculation],
        transfers: List[TransferCandidate]
    ) -> Dict[str, Any]:
        """
        Calculate summary statistics.
        
        Args:
            licenses: List of LicenseData
            costs: List of CostCalculation
            transfers: List of TransferCandidate
            
        Returns:
            Dictionary with statistics
        """
        stats = {
            'total_systems': len(licenses),
            'total_cost': sum(c.total_cost for c in costs),
            'total_transfers': len(transfers),
            'total_excess_value': sum(t.excess_value for t in transfers)
        }
        
        # Cluster breakdown
        clusters = {}
        for lic in licenses:
            cluster = lic.cluster or 'Unknown'
            clusters[cluster] = clusters.get(cluster, 0) + 1
        stats['clusters'] = clusters
        
        # Priority breakdown for transfers
        priorities = {}
        for xfer in transfers:
            priority = xfer.priority
            priorities[priority] = priorities.get(priority, 0) + 1
        stats['transfer_priorities'] = priorities
        
        return stats
