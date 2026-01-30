"""
XML Extractor Module

Parses Honeywell Experion license XML files to extract licensing information.
Converts XML structure to immutable LicenseData objects with validation.
"""

import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional
import re

from v2.pipeline.extractors.base_extractor import BaseExtractor, ExtractionResult
from v2.models.license import LicenseData
from v2.core.exceptions import XmlParsingError, DataValidationError
from v2.core.constants import ValidationLevel


class XmlExtractor(BaseExtractor):
    """
    Extract LicenseData from Experion XML license files.
    
    Handles:
    - XML structure parsing
    - License detail extraction
    - Option quantity extraction
    - File path metadata (cluster, MSID, system number, version)
    - Date parsing and validation
    """
    
    def __init__(self, strict_mode: bool = False):
        """
        Initialize XML extractor.
        
        Args:
            strict_mode: Treat warnings as errors
        """
        super().__init__(strict_mode)
    
    def can_handle(self, file_path: Path) -> bool:
        """Check if file is XML."""
        return file_path.suffix.lower() == '.xml'
    
    def validate_structure(self, file_path: Path) -> bool:
        """
        Validate XML structure before extraction.
        
        Args:
            file_path: XML file path
            
        Returns:
            True if structure valid
            
        Raises:
            XmlParsingError: If XML malformed or missing required elements
        """
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            # Check root element
            if root.tag != 'licensefile':
                raise XmlParsingError(
                    message="Root element must be 'licensefile'",
                    file_path=str(file_path)
                )
            
            # Check required children
            license = root.find('license')
            if license is None:
                raise XmlParsingError(
                    message="Missing <license> element",
                    file_path=str(file_path)
                )
            
            details = license.find('details')
            if details is None:
                raise XmlParsingError(
                    message="Missing <details> element",
                    file_path=str(file_path)
                )
            
            options = license.find('options')
            if options is None:
                raise XmlParsingError(
                    message="Missing <options> element",
                    file_path=str(file_path)
                )
            
            return True
            
        except ET.ParseError as e:
            raise XmlParsingError(
                message=f"XML parse error: {e}",
                file_path=str(file_path)
            )
    
    def extract_from_file(self, file_path: Path) -> ExtractionResult[LicenseData]:
        """
        Extract LicenseData from XML file.
        
        Args:
            file_path: Path to XML license file
            
        Returns:
            ExtractionResult with LicenseData or errors
        """
        self.reset()
        
        if not file_path.exists():
            self._add_error(f"File not found: {file_path}")
            return self._create_failure_result(file_path)
        
        if not self.can_handle(file_path):
            self._add_error(f"Not an XML file: {file_path}")
            return self._create_failure_result(file_path)
        
        try:
            # Validate structure
            self.validate_structure(file_path)
            
            # Parse XML
            tree = ET.parse(file_path)
            root = tree.getroot()
            license = root.find('license')
            
            # Extract metadata from path
            cluster = self._extract_cluster(file_path)
            system_name = self._extract_system_name(file_path)
            msid = self._extract_msid(file_path)
            system_number = self._extract_system_number(file_path)
            file_version = self._extract_version(file_path)
            
            # Extract license details
            details = self._extract_details(license)
            
            # Extract license options
            options = self._extract_options(license)
            
            # Build LicenseData
            license_data = LicenseData(
                msid=msid,
                system_number=system_number,
                cluster=cluster,
                system_name=system_name,
                release=details.get('release', ''),
                product=details.get('product', ''),
                customer=details.get('customer', ''),
                licensed=options,
                license_date=details.get('license_date'),
                file_version=file_version,
                file_path=str(file_path)
            )
            
            return self._create_success_result(license_data, file_path)
            
        except XmlParsingError:
            raise  # Re-raise parsing errors
        except Exception as e:
            self._add_error(f"Unexpected error: {e}")
            return self._create_failure_result(file_path)
    
    def _extract_cluster(self, file_path: Path) -> str:
        """
        Extract cluster name from file path.
        
        Args:
            file_path: Full file path
            
        Returns:
            Cluster name (Carson, Wilmington, Salt Lake City)
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
        
        self._add_warning(f"Could not determine cluster from path: {file_path}", ValidationLevel.WARNING)
        return 'Unknown'
    
    def _extract_system_name(self, file_path: Path) -> str:
        """
        Extract system name from folder path.
        
        Pattern: Folder name like "ESVT0 M0614 60806" -> ESVT0
                 or "RP&S M0922 50215" -> RP&S
        
        Args:
            file_path: Full file path
            
        Returns:
            System name (ESVT0, HCU, ALKY, RP&S, etc.) or 'Unknown'
        """
        folder_name = file_path.parent.name
        
        # Pattern: System name is first word/token before MSID
        # "ESVT0 M0614 60806" -> ESVT0
        # "RP&S M0922 50215" -> RP&S
        parts = folder_name.split()
        if len(parts) >= 2:
            # First part before MSID pattern
            for i, part in enumerate(parts):
                if re.match(r'^[Mm]\d+', part):  # Found MSID
                    if i > 0:
                        return parts[0]  # Return first part
        
        # If no pattern match, return Unknown
        return 'Unknown'
    
    def _extract_msid(self, file_path: Path) -> str:
        """
        Extract MSID from filename or parent folder.
        
        Patterns:
        - M0614_Experion... -> M0614
        - M13287-EX10_Experion... -> M13287-EX10
        - Folder: "ESVT0 M0614 60806" -> M0614
        
        Args:
            file_path: Full file path
            
        Returns:
            MSID string
        """
        filename = file_path.stem
        folder_name = file_path.parent.name
        
        # Try filename first
        match = re.match(r'^([Mm]\d+(?:-EX\d+)?)_', filename)
        if match:
            return match.group(1).upper()
        
        # Try folder name pattern: "ESVT0 M0614 60806"
        match = re.search(r'\b([Mm]\d+(?:-EX\d+)?)\b', folder_name)
        if match:
            return match.group(1).upper()
        
        self._add_warning(f"Could not extract MSID from: {file_path}", ValidationLevel.WARNING)
        return 'Unknown'
    
    def _extract_system_number(self, file_path: Path) -> str:
        """
        Extract system number from filename or folder.
        
        Patterns:
        - M0614_...x_60806_40.xml -> 60806
        - Folder: "ESVT0 M0614 60806" -> 60806
        
        Args:
            file_path: Full file path
            
        Returns:
            System number as string
        """
        filename = file_path.stem
        folder_name = file_path.parent.name
        
        # Try filename pattern: _x_60806_ or _60806_
        match = re.search(r'_x?_(\d{5,6})_', filename)
        if match:
            return match.group(1)
        
        # Try folder pattern: "MSID System" (e.g., "M0614 60806")
        match = re.search(r'\b(\d{5,6})\b', folder_name)
        if match:
            return match.group(1)
        
        self._add_warning(f"Could not extract system number from: {file_path}", ValidationLevel.WARNING)
        return '00000'
    
    def _extract_version(self, file_path: Path) -> int:
        """
        Extract file version number from filename.
        
        Pattern: _40.xml -> 40
        
        Args:
            file_path: Full file path
            
        Returns:
            Version number
        """
        filename = file_path.stem
        
        # Try standard pattern: _40.xml
        match = re.search(r'_(\d+)$', filename)
        if match:
            return int(match.group(1))
        
        self._add_warning(f"Could not extract version from: {file_path}", ValidationLevel.INFO)
        return 0
    
    def _extract_details(self, license_element: ET.Element) -> Dict:
        """
        Extract license detail elements.
        
        Args:
            license_element: <license> XML element
            
        Returns:
            Dict with 'release', 'product', 'customer', 'license_date'
        """
        details_elem = license_element.find('details')
        if details_elem is None:
            return {}
        
        details = {}
        
        # Map detail names to result keys
        detail_map = {
            'release': 'release',
            'product': 'product',
            'customer': 'customer',
            'generated': 'license_date'
        }
        
        for detail in details_elem.findall('detail'):
            name = detail.get('name')
            value = detail.get('value')
            
            if name in detail_map:
                key = detail_map[name]
                
                # Parse dates
                if name == 'generated' and value:
                    try:
                        details[key] = datetime.strptime(value, '%Y-%m-%d')
                    except ValueError:
                        self._add_warning(f"Invalid date format: {value}", ValidationLevel.WARNING)
                        details[key] = None
                else:
                    details[key] = value
        
        return details
    
    def _extract_options(self, license_element: ET.Element) -> Dict[str, int]:
        """
        Extract license options (quantities).
        
        Args:
            license_element: <license> XML element
            
        Returns:
            Dict mapping option name to quantity (e.g., 'PROCESSPOINTS': 4750)
        """
        options_elem = license_element.find('options')
        if options_elem is None:
            return {}
        
        options = {}
        
        for option in options_elem.findall('option'):
            name = option.get('name')
            value = option.get('value')
            
            if name and value:
                try:
                    options[name] = int(value)
                except ValueError:
                    self._add_warning(
                        f"Non-numeric option value: {name}={value}",
                        ValidationLevel.WARNING
                    )
        
        return options
