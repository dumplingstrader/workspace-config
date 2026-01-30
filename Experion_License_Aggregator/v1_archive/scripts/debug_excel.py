"""Test Excel generation with debug output."""
import json
import csv
from pathlib import Path
from xml_parser import parse_all_licenses
from excel_generator import ExcelReportGenerator

# Load licenses
data_dir = Path('../data/raw')
clusters = ['Carson']
exclude = []

licenses, errors = parse_all_licenses(data_dir, clusters, exclude)

# Load utilization
utilization = {}
util_path = Path('../data/utilization_input.csv')
with open(util_path, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        key = (row['cluster'], row['msid'], row['system_number'])
        utilization[key] = row

# Merge
for lic in licenses:
    cluster = lic.get('cluster', '')
    msid = lic.get('msid', '')
    system_number = lic.get('system_number', '')
    key = (cluster, msid, system_number)
    
    if key in utilization:
        util = utilization[key]
        for field, value in util.items():
            if field not in ['cluster', 'msid', 'system_number', 'as_of_date']:
                try:
                    lic[f'{field.upper()}_USED'] = int(value) if value else 0
                except:
                    lic[f'{field.upper()}_USED'] = 0

# Find M0921
m0921 = None
for lic in licenses:
    if lic.get('msid') == 'M0921' and lic.get('system_number') == '50216':
        m0921 = lic
        break

print('M0921 before Excel generation:')
print(f'  PROCESSPOINTS: {m0921.get("PROCESSPOINTS")}')
print(f'  PROCESSPOINTS_USED: {m0921.get("PROCESSPOINTS_USED")}')
print()

# Now test Excel generation
generator = ExcelReportGenerator(system_names_file='../config/system_names.json')

# Mock cost summary
cost_summary = {'grand_total': 0, 'total_by_cluster': {}, 'system_costs': []}

generator.create_pks_sheet(licenses, [])
generator.save('../data/output/test_debug.xlsx')

print('Excel generated: ../data/output/test_debug.xlsx')
