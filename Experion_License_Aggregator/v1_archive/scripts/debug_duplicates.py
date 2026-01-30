"""Check for duplicate M0921 systems."""
import json
import csv
from pathlib import Path
from xml_parser import parse_all_licenses

# Load licenses
data_dir = Path('../data/raw')
clusters = ['Carson']
exclude = []

licenses, errors = parse_all_licenses(data_dir, clusters, exclude)

# Find all M0921
m0921_systems = []
for lic in licenses:
    if 'M0921' in lic.get('msid', ''):
        m0921_systems.append({
            'cluster': lic.get('cluster'),
            'msid': lic.get('msid'),
            'system_number': lic.get('system_number'),
            'file_path': lic.get('file_path'),
            'PROCESSPOINTS': lic.get('PROCESSPOINTS')
        })

print(f'Found {len(m0921_systems)} systems with M0921 MSID:')
for sys in m0921_systems:
    print(f'  {sys["cluster"]}/{sys["msid"]}/{sys["system_number"]}')
    print(f'    File: {sys["file_path"]}')
    print(f'    Process Points: {sys["PROCESSPOINTS"]}')
    print()
