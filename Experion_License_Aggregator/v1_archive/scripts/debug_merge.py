"""Debug merge process."""
import json
import csv
from pathlib import Path
from xml_parser import parse_all_licenses

# Load licenses
data_dir = Path('../data/raw')
clusters = ['Carson']
exclude = []

licenses, errors = parse_all_licenses(data_dir, clusters, exclude)

# Find M0921
m0921 = None
for lic in licenses:
    if lic.get('msid') == 'M0921' and lic.get('system_number') == '50216':
        m0921 = lic
        break

if not m0921:
    print('M0921/50216 not found')
    exit(1)

print('M0921 BEFORE merge:')
print(f'  PROCESSPOINTS (licensed): {m0921.get("PROCESSPOINTS")}')
print(f'  PROCESSPOINTS_USED: {m0921.get("PROCESSPOINTS_USED", "NOT SET")}')
print()

# Load utilization
utilization = {}
util_path = Path('../data/utilization_input.csv')

with open(util_path, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        key = (row['cluster'], row['msid'], row['system_number'])
        utilization[key] = row

# Merge
key = ('Carson', m0921['msid'], m0921['system_number'])
if key in utilization:
    util = utilization[key]
    print('Found utilization data:')
    print(f'  PROCESSPOINTS from CSV: {util.get("PROCESSPOINTS")}')
    print(f'  CONSOLE_STATIONS from CSV: {util.get("CONSOLE_STATIONS")}')
    print()
    
    # Add USED fields
    for field, value in util.items():
        if field not in ['cluster', 'msid', 'system_number', 'as_of_date']:
            try:
                m0921[f'{field.upper()}_USED'] = int(value) if value else 0
            except:
                m0921[f'{field.upper()}_USED'] = 0
    
    print('M0921 AFTER merge:')
    print(f'  PROCESSPOINTS_USED: {m0921.get("PROCESSPOINTS_USED")}')
    print(f'  CONSOLE_STATIONS_USED: {m0921.get("CONSOLE_STATIONS_USED")}')
else:
    print('NO utilization data found')
