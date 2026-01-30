"""
Parse utilization CSV files from Experion Station Manager exports.

Converts detailed CSV exports from System Manager/Station into the 
utilization_input.csv format required by the license aggregator.

Usage:
    python parse_utilization_csvs.py

Input: 
    data/raw/Usage/*.csv (station export format)
    
Output:
    data/utilization_input.csv (aggregator format)
"""

import csv
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List


def parse_experion_csv(file_path: Path) -> Dict:
    """
    Parse Experion Station Manager CSV export.
    
    Expected format:
        Category,License Option,Detail Type,{SystemName}
        ...
        System sizing - Points,Process point(s),License,4750
        System sizing - Points,Process point(s),Used,108
        ...
    
    Returns:
        Dict with system info and license usage values
    """
    result = {
        'system_name': file_path.stem,  # Filename without extension
        'msid': None,
        'system_number': None,
        'server_name': None,
        'collate_date': None,
        'license_version': None,
        'customer': None,
        'product': None,
        'release': None
    }
    
    # License fields we're tracking
    license_fields = {}
    
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        
        for row in reader:
            if len(row) < 4:
                continue
            
            category = row[0].strip()
            option = row[1].strip()
            detail_type = row[2].strip()
            value = row[3].strip() if len(row) > 3 else ''
            
            # Extract header information
            if category == 'Collate header':
                if option == 'Collate date':
                    result['collate_date'] = value
                elif option == 'Server name':
                    result['server_name'] = value
            
            # Extract license certificate info
            elif category == 'License certificate':
                if option == 'MSID/ESID':
                    result['msid'] = value
                elif option == 'System number':
                    result['system_number'] = value
                elif option == 'License version':
                    result['license_version'] = value
                elif option == 'Customer name':
                    result['customer'] = value
                elif option == 'Product':
                    result['product'] = value
                elif option == 'Release':
                    result['release'] = value
            
            # Extract license/usage data
            elif category == 'System sizing - Points':
                if option == 'Process point(s)' and detail_type == 'Used':
                    license_fields['PROCESSPOINTS'] = value
                elif option == 'SCADA point(s)' and detail_type == 'Used':
                    license_fields['SCADAPOINTS'] = value
                elif option == 'Analog IO Point(s)' and detail_type == 'Used':
                    license_fields['CDA_IO_ANA'] = value
                elif option == 'Digital IO Point(s)' and detail_type == 'Used':
                    license_fields['CDA_IO_DIG'] = value
            
            elif category == 'System sizing - Stations':
                # Flex stations (regular)
                if option == 'Flex station(s)' and detail_type == 'Used':
                    license_fields['STATIONS'] = value
                # Multi-window flex stations (separate license)
                elif option == 'Multi window flex station(s)' and detail_type == 'Used':
                    license_fields['MULTISTATIONS'] = value
                # Console stations (dedicated operator consoles)
                elif option == 'Console station(s)' and detail_type == 'Used':
                    license_fields['CONSOLE_STATIONS'] = value
                # Console extension stations
                elif option == 'Console extension station(s)' and detail_type == 'Used':
                    license_fields['CONSOLE_EXTENSION'] = value
                # Direct connect stations
                elif option == 'Direct connect station(s)' and detail_type == 'Used':
                    license_fields['DIRECTSTATIONS'] = value
                # Direct connect clients
                elif option == 'Direct connect client(s)' and detail_type == 'Used':
                    license_fields['DIRECTCLIENTS'] = value
                # Read-only stations
                elif option == 'Read only station(s)' and detail_type == 'Used':
                    license_fields['READONLY_STATIONS'] = value
                # Collaboration stations
                elif option == 'Collaboration station(s)' and detail_type == 'Used':
                    license_fields['COLLABORATION_STATIONS'] = value
                # Experion app clients
                elif option == 'Experion app client(s)' and detail_type == 'Used':
                    license_fields['EXPERION_APP_CLIENTS'] = value
            
            
            elif category == 'Options':
                # Operator touch panels
                if option == 'Operator touch panel(s)' and detail_type == 'Used':
                    license_fields['OPERATOR_TOUCH_PANELS'] = value
                # Virtualization CALs
                elif option == 'Virtualization Server CAL' and detail_type == 'License':
                    license_fields['VIRTUALIZATION'] = value
                elif option == 'Virtualization Client CAL' and detail_type == 'License':
                    license_fields['VIRTUALIZATION_CLIENT'] = value
                # Server redundancy (DUAL)
                elif option == 'Redundancy - Server redundancy' and detail_type == 'License':
                    license_fields['DUAL'] = '1' if 'Licensed' in value else '0'
                # OPC DA servers
                elif option == 'OPC classic data access client application instance(s)' and detail_type == 'License':
                    license_fields['OPC_DA'] = value
                # OPC UA clients  
                elif option == 'OPC UA data access client application instance(s)' and detail_type == 'License':
                    license_fields['OPC_UA_CLIENT'] = value
                # DSA (Data Acquisition Service)
                elif option == 'DSA enabling license' and detail_type == 'License':
                    license_fields['DAS'] = '1' if 'Licensed' in value else '0'
                # Layered Application Services
                elif option == 'Layered application services' and detail_type == 'License':
                    license_fields['LAS'] = '1' if 'Licensed' in value else '0'
                # Display Builder
                elif option == 'Equipment display' and detail_type == 'License':
                    license_fields['DSPBLD'] = '1' if 'Licensed' in value else '0'
                # Microsoft Excel data exchange (API-like)
                elif option == 'Microsoft Excel data exchange' and detail_type == 'License':
                    if value.isdigit() and int(value) > 0:
                        license_fields['API'] = '1'
                # ODBC driver (SQL access)
                elif option == 'ODBC driver' and detail_type == 'License':
                    license_fields['SQL'] = '1' if 'Licensed' in value else '0'
            
            elif category == 'Interfaces':
                # CDA subsystems
                if option == 'CDA subsystems interface' and detail_type == 'License':
                    license_fields['CDA'] = '1' if 'Licensed' in value else '0'
                # TDC 3000 / TPS
                elif 'TDC 3000' in option and detail_type == 'License':
                    license_fields['TPS'] = '1' if 'Licensed' in value else '0'
                # Safety Manager / FSC
                elif 'Safety manager' in option or 'FSC' in option:
                    if detail_type == 'License':
                        license_fields['FSC'] = '1' if 'Licensed' in value else '0'
                # Modicon interfaces
                elif 'Modicon' in option and detail_type == 'License':
                    license_fields['MODICON'] = '1' if 'Licensed' in value else '0'
                # Allen Bradley
                elif 'Allen Bradley' in option or 'Rockwell' in option:
                    if 'Ethernet' in option and detail_type == 'License':
                        license_fields['AB_ETH'] = '1' if 'Licensed' in value else '0'
                    elif detail_type == 'License':
                        license_fields['AB'] = '1' if 'Licensed' in value else '0'
                # DNP3
                elif 'DNP3' in option and detail_type == 'License':
                    license_fields['DNP3'] = '1' if 'Licensed' in value else '0'
    
    result['license_fields'] = license_fields
    return result


def map_to_cluster(system_name: str, msid: str) -> str:
    """
    Map system name or MSID to cluster.
    
    Customize this function based on your site's naming conventions.
    """
    # Default mapping - customize for your sites
    carson_systems = ['ESVT0', 'ESVT1', 'ESVT2', 'ESVT3', 'ESVT4', 'ESVT5', 'ESVT6',
                     'CPD', 'CRU', 'DCU', 'CALK', 'CHCU', 'WHCU', 'REF1']
    wilmington_systems = ['WALK', 'SPW', 'SHB', 'SCR', 'SA', 'RPS', 'NA', 'HTU', 'ETD']
    
    if system_name in carson_systems:
        return 'Carson'
    elif system_name in wilmington_systems:
        return 'Wilmington'
    elif 'LARC' in system_name:
        return 'Carson'
    elif 'LARW' in system_name:
        return 'Wilmington'
    elif 'SRP' in system_name:
        return 'Salt Lake City'
    else:
        return 'Unknown'


def convert_date(date_str: str) -> str:
    """
    Convert date from 'M/D/YYYY H:MM:SS AM/PM' to 'YYYY-MM-DD'.
    """
    if not date_str:
        return datetime.now().strftime('%Y-%m-%d')
    
    try:
        # Try parsing with time
        dt = datetime.strptime(date_str, '%m/%d/%Y %I:%M:%S %p')
        return dt.strftime('%Y-%m-%d')
    except ValueError:
        try:
            # Try without time
            dt = datetime.strptime(date_str, '%m/%d/%Y')
            return dt.strftime('%Y-%m-%d')
        except ValueError:
            # Default to today
            return datetime.now().strftime('%Y-%m-%d')


def create_utilization_csv(parsed_data: List[Dict], output_file: Path):
    """
    Create utilization_input.csv from parsed system data.
    """
    # Define all possible fields
    all_fields = [
        'cluster', 'msid', 'system_number', 'as_of_date',
        'PROCESSPOINTS', 'SCADAPOINTS', 'CDA_IO_ANA', 'CDA_IO_DIG',
        'STATIONS', 'MULTISTATIONS', 'CONSOLE_STATIONS', 'CONSOLE_EXTENSION',
        'READONLY_STATIONS', 'COLLABORATION_STATIONS', 'EXPERION_APP_CLIENTS',
        'OPERATOR_TOUCH_PANELS', 'DIRECTSTATIONS', 'DIRECTCLIENTS',
        'DUAL', 'MULTI_SERVER', 'MULTI_COUNT',
        'DAS', 'API', 'SQL', 'LAS', 'DSPBLD',
        'CDA', 'TPS', 'FSC', 'MODICON', 'AB', 'AB_ETH', 'DNP3',
        'OPC_DA', 'OPC_UA_CLIENT',
        'VIRTUALIZATION', 'VIRTUALIZATION_CLIENT'
    ]
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=all_fields)
        writer.writeheader()
        
        for data in parsed_data:
            row = {
                'cluster': map_to_cluster(data['system_name'], data['msid']),
                'msid': data['msid'] or data['system_name'],
                'system_number': data['system_number'] or '',
                'as_of_date': convert_date(data['collate_date'])
            }
            
            # Add license field values
            for field in all_fields[4:]:  # Skip first 4 (cluster, msid, etc.)
                row[field] = data['license_fields'].get(field, '')
            
            writer.writerow(row)


def main():
    """
    Main execution: Parse all CSVs from Usage/ folder and create utilization_input.csv.
    """
    # Setup paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    usage_dir = project_root / 'data' / 'raw' / 'Usage'
    output_file = project_root / 'data' / 'utilization_input.csv'
    
    if not usage_dir.exists():
        print(f"❌ Error: Usage directory not found: {usage_dir}")
        return
    
    # Find all CSV files
    csv_files = list(usage_dir.glob('*.csv'))
    
    if not csv_files:
        print(f"❌ No CSV files found in {usage_dir}")
        return
    
    print(f"Found {len(csv_files)} CSV files to process...")
    
    # Parse all files
    parsed_data = []
    errors = []
    
    for csv_file in csv_files:
        try:
            print(f"  Parsing {csv_file.name}...", end=' ')
            data = parse_experion_csv(csv_file)
            parsed_data.append(data)
            print(f"✓ (MSID: {data['msid']}, System: {data['system_number']})")
        except Exception as e:
            errors.append((csv_file.name, str(e)))
            print(f"✗ Error: {e}")
    
    # Create output
    if parsed_data:
        create_utilization_csv(parsed_data, output_file)
        print(f"\n✓ Successfully created {output_file}")
        print(f"  Processed {len(parsed_data)} systems")
        
        # Show cluster summary
        clusters = {}
        for data in parsed_data:
            cluster = map_to_cluster(data['system_name'], data['msid'])
            clusters[cluster] = clusters.get(cluster, 0) + 1
        
        print("\n  Systems by cluster:")
        for cluster, count in sorted(clusters.items()):
            print(f"    {cluster}: {count} systems")
    
    # Report errors
    if errors:
        print(f"\n⚠ {len(errors)} files had parsing errors:")
        for filename, error in errors:
            print(f"    {filename}: {error}")
    
    print("\nNext steps:")
    print(f"  1. Review {output_file} for accuracy")
    print(f"  2. Verify cluster mappings (edit map_to_cluster() if needed)")
    print(f"  3. Run license aggregator: python scripts/main.py")


if __name__ == '__main__':
    main()
