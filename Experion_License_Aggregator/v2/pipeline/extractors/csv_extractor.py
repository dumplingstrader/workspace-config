"""
CSV Extractor Module

Parses Station Manager CSV exports to extract usage data.
Converts CSV structure to immutable UsageData objects.
"""

import csv
from pathlib import Path
from typing import Dict, List, Optional
import re

from v2.pipeline.extractors.base_extractor import BaseExtractor, ExtractionResult
from v2.models.usage import UsageData
from v2.core.exceptions import CsvParsingError, DataValidationError
from v2.core.constants import ValidationLevel


class CsvExtractor(BaseExtractor):
    """
    Extract UsageData from Station Manager CSV files.
    
    CSV Format:
    - Row 1: Category,License Option,Detail Type,<SYSTEM_NAME>
    - Row 2: Collate header,Collate date,License,<DATE>
    - Row 6: License certificate,System number,License,<SYSTEM_NUMBER>
    - Row 8: License certificate,MSID/ESID,License,<MSID>
    - Rows with "Used" in column 3 contain usage quantities
    
    Maps:
    - "Process point(s)" → PROCESSPOINTS
    - "Console station(s)" → CONSOLE_STATIONS (maps to DIRECTSTATIONS)
    - "SCADA point(s)" → SCADAPOINTS
    - "Flex station(s)" → STATIONS
    """
    
    # Mapping from CSV row names to license types
    CSV_TO_LICENSE_TYPE = {
        'Process point(s)': 'PROCESSPOINTS',
        'SCADA point(s)': 'SCADAPOINTS',
        'Console station(s)': 'CONSOLE_STATIONS',  # Note: Will map to DIRECTSTATIONS
        'Flex station(s)': 'STATIONS',
        'Multi window flex station(s)': 'MULTISTATIONS',
        'Distributed server(s)': 'MULTI_COUNT',
        'Analog IO Point(s)': 'CDA_IO_ANA',
        'Digital IO Point(s)': 'CDA_IO_DIG',
        'Operator touch panel(s)': 'OPER_TOUCH_PANEL',
        'Modbus': 'MODICON',
        'OPC client interface': 'OPCCLIENT',
        'Console extension station(s)': 'DIRECTCLIENTS',
        'Other point(s)': 'OTHER_POINTS',
        'Total point(s)': 'TOTAL_POINTS',
        'Equipment point(s)': 'EQUIPMENT_POINTS',
        'Composite Device point(s)': 'COMPOSITE_POINTS',
        'Collaboration station(s)': 'COLLABORATION_STATIONS',
        'Experion app client(s)': 'EXPERION_APP_CLIENTS',
        'Maximum active RCM instance(s)': 'MAX_RCM_INSTANCES',
    }
    
    def __init__(self, strict_mode: bool = False):
        """
        Initialize CSV extractor.
        
        Args:
            strict_mode: Treat warnings as errors
        """
        super().__init__(strict_mode)
    
    def can_handle(self, file_path: Path) -> bool:
        """Check if file is CSV."""
        return file_path.suffix.lower() == '.csv'
    
    def validate_structure(self, file_path: Path) -> bool:
        """
        Validate CSV structure before extraction.
        
        Args:
            file_path: CSV file path
            
        Returns:
            True if structure valid
            
        Raises:
            CsvParsingError: If CSV malformed or missing required columns
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                
                # Read first row to check structure
                header = next(reader, None)
                if not header:
                    raise CsvParsingError(
                        message="Empty CSV file",
                        file_path=str(file_path)
                    )
                
                # Check expected columns
                if len(header) < 4:
                    raise CsvParsingError(
                        message=f"Expected at least 4 columns, found {len(header)}",
                        file_path=str(file_path)
                    )
                
                # First 3 columns should be Category, License Option, Detail Type
                expected = ['Category', 'License Option', 'Detail Type']
                if header[:3] != expected:
                    raise CsvParsingError(
                        message=f"Expected columns {expected}, found {header[:3]}",
                        file_path=str(file_path)
                    )
                
                return True
                
        except (IOError, OSError) as e:
            raise CsvParsingError(
                message=f"Cannot read CSV file: {e}",
                file_path=str(file_path)
            )
    
    def extract_from_file(self, file_path: Path) -> ExtractionResult[List[UsageData]]:
        """
        Extract UsageData list from CSV file.
        
        Note: Returns a list because one CSV can contain multiple license types.
        
        Args:
            file_path: Path to CSV file
            
        Returns:
            ExtractionResult with List[UsageData] or errors
        """
        self.reset()
        
        if not file_path.exists():
            self._add_error(f"File not found: {file_path}")
            return self._create_failure_result(file_path)
        
        if not self.can_handle(file_path):
            self._add_error(f"Not a CSV file: {file_path}")
            return self._create_failure_result(file_path)
        
        try:
            # Validate structure
            self.validate_structure(file_path)
            
            # Parse CSV
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                rows = list(reader)
            
            # Extract metadata
            cluster = self._extract_cluster(file_path)
            system_name = self._extract_system_name(rows, file_path)
            msid = self._extract_msid(rows)
            system_number = self._extract_system_number(rows)
            
            # Extract usage data
            usage_list = self._extract_usage_data(rows, cluster, msid, system_number, system_name)
            
            if not usage_list:
                self._add_error("No usage data found in CSV")
                return self._create_failure_result(file_path)
            
            return self._create_success_result(usage_list, file_path)
            
        except CsvParsingError:
            raise  # Re-raise parsing errors
        except Exception as e:
            self._add_error(f"Unexpected error: {e}")
            return self._create_failure_result(file_path)
    
    def _extract_cluster(self, file_path: Path) -> str:
        """
        Extract cluster from file path or filename.
        
        Args:
            file_path: Full file path
            
        Returns:
            Cluster name
        """
        parts = file_path.parts
        for i, part in enumerate(parts):
            if part in ['Carson', 'Wilmington', 'Salt Lake City']:
                return part
            # Handle 'raw/Carson' structure
            if part == 'raw' and i + 1 < len(parts):
                next_part = parts[i + 1]
                if next_part in ['Carson', 'Wilmington', 'Salt Lake City']:
                    return next_part
        
        # Check if Usage folder is in path (common structure)
        if 'Usage' in parts:
            # Cluster often before Usage folder
            idx = parts.index('Usage')
            if idx > 0 and parts[idx - 1] in ['Carson', 'Wilmington', 'Salt Lake City']:
                return parts[idx - 1]
        
        self._add_warning(f"Could not determine cluster from path: {file_path}", ValidationLevel.WARNING)
        return 'Unknown'
    
    def _extract_system_name(self, rows: List[List[str]], file_path: Path) -> str:
        """
        Extract system name from CSV header (column 4 of row 1).
        
        Args:
            rows: CSV rows
            file_path: File path for fallback
            
        Returns:
            System name
        """
        if rows and len(rows[0]) >= 4:
            return rows[0][3]
        
        # Fallback to filename
        return file_path.stem
    
    def _extract_msid(self, rows: List[List[str]]) -> str:
        """
        Extract MSID from CSV data.
        
        Row 8: License certificate,MSID/ESID,License,<MSID>
        
        Args:
            rows: CSV rows
            
        Returns:
            MSID string
        """
        for row in rows:
            if len(row) >= 4:
                if row[0] == 'License certificate' and 'MSID' in row[1]:
                    msid = row[3].strip()
                    if msid:
                        return msid.upper()
        
        self._add_warning("Could not extract MSID from CSV", ValidationLevel.WARNING)
        return 'Unknown'
    
    def _extract_system_number(self, rows: List[List[str]]) -> str:
        """
        Extract system number from CSV data.
        
        Row 6: License certificate,System number,License,<SYSTEM_NUMBER>
        
        Args:
            rows: CSV rows
            
        Returns:
            System number as string
        """
        for row in rows:
            if len(row) >= 4:
                if row[0] == 'License certificate' and row[1] == 'System number':
                    system_number = row[3].strip()
                    if system_number:
                        return system_number
        
        self._add_warning("Could not extract system number from CSV", ValidationLevel.WARNING)
        return '00000'
    
    def _extract_usage_data(self, rows: List[List[str]], cluster: str, 
                           msid: str, system_number: str, system_name: str) -> List[UsageData]:
        """
        Extract all usage data rows from CSV.
        
        Args:
            rows: CSV rows
            cluster: Cluster name
            msid: MSID
            system_number: System number
            system_name: System name from CSV filename
            
        Returns:
            List of UsageData objects
        """
        usage_list = []
        
        for row in rows:
            if len(row) < 4:
                continue
            
            # Look for rows where column 3 is "Used"
            if row[2] == 'Used':
                license_option = row[1]  # e.g., "Process point(s)"
                used_value = row[3]
                
                # Map CSV name to license type
                license_type = self.CSV_TO_LICENSE_TYPE.get(license_option)
                
                if license_type:
                    try:
                        used_qty = int(used_value) if used_value else 0
                        
                        # Use system_name extracted from CSV filename
                        usage_data = UsageData(
                            cluster=cluster,
                            msid=msid,
                            license_type=license_type,
                            used_quantity=used_qty,
                            system_name=system_name
                        )
                        
                        usage_list.append(usage_data)
                        
                    except ValueError:
                        self._add_warning(
                            f"Invalid usage value for {license_option}: {used_value}",
                            ValidationLevel.WARNING
                        )
                    except DataValidationError as e:
                        self._add_warning(
                            f"Validation error for {license_option}: {e}",
                            ValidationLevel.WARNING
                        )
        
        return usage_list
