"""Quick production data analysis script"""
from pathlib import Path
from v2.pipeline.coordinator import PipelineCoordinator
from v2.models.usage import UsageData

# Initialize coordinator
coordinator = PipelineCoordinator(
    config_dir=Path('v2/config'),
    output_dir=Path('data/output')
)

# Extract usage data from all CSV files in Usage directory
print('Loading usage data from CSV files...')
usage_dir = Path('data/raw/Usage')
all_usage_data = []

if usage_dir.exists():
    csv_files = list(usage_dir.glob('*.csv'))
    print(f'Found {len(csv_files)} CSV files in Usage directory')
    
    for csv_file in csv_files:
        try:
            result = coordinator.csv_extractor.extract_from_file(csv_file)
            if result.success and result.data:
                all_usage_data.extend(result.data)
                print(f'  [OK] {csv_file.name}: {len(result.data)} usage records')
            else:
                print(f'  [ERR] {csv_file.name}: {"; ".join(result.errors)}')
        except Exception as e:
            print(f'  [ERR] {csv_file.name}: {e}')
    
    print(f'Total usage records extracted: {len(all_usage_data)}')
else:
    print(f'[WARN] Usage directory not found: {usage_dir}')

# Process both Carson and Wilmington sites
all_licenses = []
all_costs = []
all_transfers = []

for site in ['Carson', 'Wilmington']:
    site_path = Path(f'data/raw/{site}')
    if not site_path.exists():
        print(f'\n[SKIP] {site} directory not found: {site_path}')
        continue
    
    print(f'\nProcessing {site} site data...')
    print('=' * 60)
    result = coordinator.run_pipeline(
        xml_dir=site_path,
        usage_data=all_usage_data,  # Pass pre-extracted usage data
        export_json=False,  # Don't export individual site data
        export_excel=False  # Wait until we combine all sites
    )
    
    all_licenses.extend(result.licenses)
    all_costs.extend(result.costs)
    all_transfers.extend(result.transfers)
    
    print(f'  {site}: {len(result.licenses)} systems processed')

print(f'\n[OK] Processing Complete')
print(f'  Total systems processed: {len(all_licenses)}')
print(f'  Costs calculated: {len(all_costs)}')
print(f'  Transfer candidates: {len(all_transfers)}')

# Export combined results
print(f'\n[EXPORT] Generating combined report...')
export_errors = coordinator._export_results(
    licenses=all_licenses,
    usage_data=all_usage_data,
    costs=all_costs,
    transfers=all_transfers,
    export_json=True,
    export_excel=True
)

# Find export files
excel_files = list(Path('data/output').glob('Experion_License_Report_*.xlsx'))
json_files = list(Path('data/output').glob('licenses_*.json'))

if excel_files:
    latest_excel = max(excel_files, key=lambda p: p.stat().st_mtime)
    print(f'\n[REPORT] Excel report: {latest_excel}')

if json_files:
    latest_json = max(json_files, key=lambda p: p.stat().st_mtime)
    print(f'📄 JSON export: {latest_json}')

# Show top 10 transfer candidates by value
if result.transfers:
    print(f'\n[TRANSFERS] Top 10 Transfer Candidates by Value:')
    print('=' * 60)
    sorted_transfers = sorted(result.transfers, key=lambda t: t.excess_value, reverse=True)[:10]
    for i, transfer in enumerate(sorted_transfers, 1):
        print(f'{i:2d}. {transfer.msid:10s} {transfer.cluster:15s} {transfer.license_type:20s}')
        print(f'    Licensed: {transfer.licensed_quantity:5d}, Used: {transfer.used_quantity:5d}, Excess: {transfer.excess_quantity:5d} points')
        print(f'    Value: ${transfer.unit_price:6.2f}/unit = ${transfer.excess_value:10,.2f} savings [{transfer.priority}]')

# Show summary by priority
print(f'\n[SUMMARY] Transfer Summary by Priority:')
print('=' * 60)
high = [t for t in result.transfers if t.priority == 'HIGH']
medium = [t for t in result.transfers if t.priority == 'MEDIUM']
low = [t for t in result.transfers if t.priority == 'LOW']

print(f'  HIGH:   {len(high):3d} transfers  (${sum(t.excess_value for t in high):12,.2f} potential savings)')
print(f'  MEDIUM: {len(medium):3d} transfers  (${sum(t.excess_value for t in medium):12,.2f} potential savings)')
print(f'  LOW:    {len(low):3d} transfers  (${sum(t.excess_value for t in low):12,.2f} potential savings)')
print(f'  TOTAL:  {len(result.transfers):3d} transfers  (${sum(t.excess_value for t in result.transfers):12,.2f} potential savings)')

# Show system breakdown
print(f'\n[SYSTEMS] Systems by Cluster:')
print('=' * 60)
from collections import Counter
cluster_counts = Counter(lic.cluster for lic in result.licenses)
for cluster, count in sorted(cluster_counts.items()):
    print(f'  {cluster:20s}: {count:3d} systems')

# Show cost summary
print(f'\n[COST] Cost Summary:')
print('=' * 60)
total_cost = sum(cost.total_cost for cost in result.costs)
print(f'  Total License Value: ${total_cost:15,.2f}')
print(f'  Average per System:  ${total_cost/len(result.licenses):15,.2f}')

# Show cost details for first few systems
print(f'\n  Sample Costs (first 5 systems):')
sample_costs = {}
for cost in result.costs[:20]:  # Get first 20 cost records
    if cost.msid not in sample_costs:
        sample_costs[cost.msid] = []
    sample_costs[cost.msid].append(cost)
    if len(sample_costs) >= 5:
        break

for msid, costs in list(sample_costs.items())[:5]:
    system_total = sum(c.total_cost for c in costs)
    print(f'    {msid}: ${system_total:10,.2f} ({len(costs)} license types, source: {costs[0].price_source})')

# Show license type breakdown
print(f'\n[LICENSE TYPES] License Type Breakdown:')
print('=' * 60)
license_types = {}
for lic in result.licenses:
    for lic_type, quantity in lic.licensed.items():
        if lic_type not in license_types:
            license_types[lic_type] = {'count': 0, 'total_quantity': 0}
        license_types[lic_type]['count'] += 1
        license_types[lic_type]['total_quantity'] += quantity

for lic_type, data in sorted(license_types.items(), key=lambda x: x[1]['total_quantity'], reverse=True):
    print(f'  {lic_type:25s}: {data["count"]:3d} systems, {data["total_quantity"]:8,d} total points')

print('\n' + '=' * 60)
print('[COMPLETE] Production analysis complete!')
print('=' * 60)
