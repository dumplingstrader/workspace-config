"""
Experion License XML Parser
Extracts license information from Honeywell Experion XML files.
"""

import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime
import re
from typing import Dict, List, Optional, Tuple


class ExperionLicenseParser:
    """Parse Experion license XML files and extract key information."""
    
    def __init__(self, exclude_folders: List[str] = None):
        """
        Initialize parser with folder exclusions.
        
        Args:
            exclude_folders: List of folder names to skip (e.g., ['Emerson', 'Hot Spare'])
        """
        self.exclude_folders = exclude_folders or []
        self.errors = []
    
    def parse_xml_file(self, xml_path: Path) -> Optional[Dict]:
        """
        Parse a single Experion license XML file.
        
        Args:
            xml_path: Path to XML file
            
        Returns:
            Dictionary with license data or None if parse fails
        """
        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()
            
            # Extract basic system information
            license_data = {
                'file_path': str(xml_path),
                'file_name': xml_path.name,
                'folder_name': xml_path.parent.name,
                'cluster': self._extract_cluster(xml_path),
                'msid': self._extract_msid(xml_path.name),
                'system_number': self._extract_system_number(xml_path.name),
                'product': self._extract_product(root),
                'release': self._extract_release(root),
                'customer': self._extract_customer(root),
                'license_date': self._extract_license_date(root),
                'version': self._extract_version(xml_path.name),
            }
            
            # Extract all license options
            license_options = self._extract_license_options(root)
            license_data.update(license_options)
            
            return license_data
            
        except Exception as e:
            self.errors.append({
                'file': str(xml_path),
                'error': str(e)
            })
            return None
    
    def scan_directory(self, base_path: Path, cluster_name: str) -> List[Dict]:
        """
        Scan directory for Experion XML files, selecting highest version per system.
        
        Args:
            base_path: Base directory to scan (e.g., data/raw/Carson/)
            cluster_name: Name of cluster (e.g., 'Carson')
            
        Returns:
            List of parsed license data dictionaries
        """
        results = []
        system_files = {}  # Track files by system to select highest version
        
        # Find all XML files
        for xml_file in base_path.rglob('*.xml'):
            # Skip excluded folders
            if any(excluded in str(xml_file) for excluded in self.exclude_folders):
                continue
            
            # Group files by system (folder name)
            system_folder = xml_file.parent.name
            version = self._extract_version(xml_file.name)
            
            if system_folder not in system_files:
                system_files[system_folder] = []
            system_files[system_folder].append((version, xml_file))
        
        # Select highest version for each system
        for system_folder, files in system_files.items():
            # Sort by version number (descending)
            files.sort(key=lambda x: x[0], reverse=True)
            highest_version_file = files[0][1]
            
            # Parse the selected file
            license_data = self.parse_xml_file(highest_version_file)
            if license_data:
                license_data['cluster'] = cluster_name
                results.append(license_data)
        
        return results
    
    def _extract_cluster(self, xml_path: Path) -> str:
        """Extract cluster name from path."""
        # Assume cluster is parent folder name
        parts = xml_path.parts
        for i, part in enumerate(parts):
            if part in ['Carson', 'Wilmington', 'raw']:
                if part == 'raw' and i + 1 < len(parts):
                    return parts[i + 1]
                elif part != 'raw':
                    return part
        return 'Unknown'
    
    def _extract_msid(self, filename: str) -> str:
        """Extract MSID from filename (e.g., M0614 from M0614_Experion_PKS...)."""
        match = re.match(r'^([^_]+)_', filename)
        return match.group(1) if match else 'Unknown'
    
    def _extract_system_number(self, filename: str) -> str:
        """Extract system number from filename (e.g., 60806 from ...x_60806_40.xml)."""
        match = re.search(r'_x_(\d+)_\d+\.xml$', filename)
        return match.group(1) if match else 'Unknown'
    
    def _extract_product(self, root: ET.Element) -> str:
        """Extract product name from XML (PKS, HS, EAS)."""
        # Look for product in various XML locations
        for tag in ['Product', 'product', 'ProductName']:
            elem = root.find(f'.//{tag}')
            if elem is not None and elem.text:
                return elem.text.strip()
        
        # Fallback: extract from filename if in root attributes
        return root.attrib.get('product', 'PKS')
    
    def _extract_release(self, root: ET.Element) -> str:
        """Extract release version (e.g., R520)."""
        for tag in ['Release', 'release', 'Version']:
            elem = root.find(f'.//{tag}')
            if elem is not None and elem.text:
                return elem.text.strip()
        return 'Unknown'
    
    def _extract_customer(self, root: ET.Element) -> str:
        """Extract customer name."""
        for tag in ['Customer', 'customer', 'CustomerName']:
            elem = root.find(f'.//{tag}')
            if elem is not None and elem.text:
                return elem.text.strip()
        return 'Unknown'
    
    def _extract_license_date(self, root: ET.Element) -> Optional[str]:
        """Extract license issue date."""
        for tag in ['LicenseDate', 'IssueDate', 'Date']:
            elem = root.find(f'.//{tag}')
            if elem is not None and elem.text:
                # Try to parse and normalize date
                date_str = elem.text.strip()
                try:
                    dt = datetime.strptime(date_str, '%Y-%m-%d')
                    return dt.strftime('%Y-%m-%d')
                except ValueError:
                    try:
                        dt = datetime.strptime(date_str, '%m/%d/%Y')
                        return dt.strftime('%Y-%m-%d')
                    except ValueError:
                        return date_str
        return None
    
    def _extract_version(self, filename: str) -> int:
        """Extract version number from filename (e.g., 40 from ...60806_40.xml)."""
        match = re.search(r'_(\d+)\.xml$', filename)
        return int(match.group(1)) if match else 0
    
    def _extract_license_options(self, root: ET.Element) -> Dict[str, int]:
        """
        Extract all license option values from XML.
        
        Returns:
            Dictionary of option names to values (e.g., {'PROCESSPOINTS': 5000})
        """
        options = {}
        
        # Common license option tags
        option_tags = [
            'PROCESSPOINTS', 'SCADAPOINTS', 'CDA_IO_ANA', 'CDA_IO_DIG',
            'STATIONS', 'MULTISTATIONS', 'DIRECTSTATIONS', 'DIRECTCLIENTS',
            'DUAL', 'MULTI_SERVER', 'MULTI_COUNT',
            'DAS', 'API', 'SQL', 'LAS', 'DSPBLD',
            'CDA', 'TPS', 'FSC', 'MODICON', 'AB', 'AB_ETH', 'DNP3',
            'OPC_DA', 'OPC_UA_CLIENT', 'OPC_UA_SERVER',
            'VIRTUALIZATION', 'VIRTUALIZATION_CLIENT'
        ]
        
        # Search for each option in XML
        for option in option_tags:
            # Try multiple possible XML structures
            elem = root.find(f'.//{option}')
            if elem is None:
                elem = root.find(f'.//Option[@name="{option}"]')
            if elem is None:
                elem = root.find(f'.//LicenseOption[@type="{option}"]')
            
            if elem is not None:
                # Extract value (could be text or attribute)
                value_str = elem.text or elem.attrib.get('value', '0')
                try:
                    options[option] = int(value_str)
                except ValueError:
                    options[option] = 0
            else:
                options[option] = 0  # Default to 0 if not found
        
        return options
    
    def get_errors(self) -> List[Dict]:
        """Return list of parsing errors."""
        return self.errors


def parse_all_licenses(data_dir: Path, clusters: List[str], 
                       exclude_folders: List[str]) -> Tuple[List[Dict], List[Dict]]:
    """
    Parse all license files for all clusters.
    
    Args:
        data_dir: Base data directory (e.g., data/raw/)
        clusters: List of cluster names to process
        exclude_folders: List of folder names to skip
        
    Returns:
        Tuple of (license_data_list, errors_list)
    """
    parser = ExperionLicenseParser(exclude_folders=exclude_folders)
    all_licenses = []
    
    for cluster in clusters:
        cluster_path = data_dir / cluster
        if not cluster_path.exists():
            print(f"Warning: Cluster path not found: {cluster_path}")
            continue
        
        print(f"Scanning {cluster}...")
        licenses = parser.scan_directory(cluster_path, cluster)
        all_licenses.extend(licenses)
        print(f"  Found {len(licenses)} systems")
    
    return all_licenses, parser.get_errors()


if __name__ == '__main__':
    # Test parsing
    from pathlib import Path
    import json
    
    data_dir = Path('../data/raw')
    clusters = ['Carson', 'Wilmington']
    exclude = ['Emerson', 'EXELE', 'GE', 'Hot Spare']
    
    licenses, errors = parse_all_licenses(data_dir, clusters, exclude)
    
    print(f"\nTotal licenses parsed: {len(licenses)}")
    print(f"Errors: {len(errors)}")
    
    if licenses:
        print("\nSample license data:")
        print(json.dumps(licenses[0], indent=2))
    
    if errors:
        print("\nErrors:")
        for err in errors:
            print(f"  {err['file']}: {err['error']}")
