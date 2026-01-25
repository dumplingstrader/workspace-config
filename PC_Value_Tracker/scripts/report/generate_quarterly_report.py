#!/usr/bin/env python3
"""
Generate Quarterly Summary Report

Reads master.json and generates a comprehensive Excel report for the specified quarter.
Output includes quarterly summary, trend analysis, and stream scorecards.
"""

import pandas as pd
import json
from pathlib import Path
from datetime import datetime
import argparse
from collections import Counter


def load_master_data(master_file):
    """Load and return master.json data."""
    with open(master_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def parse_quarter(quarter_str):
    """Parse quarter string (YYYY-Q1, YYYY-Q2, etc.) into year and months."""
    try:
        year, q = quarter_str.split('-Q')
        year = int(year)
        q = int(q)
        
        if q not in [1, 2, 3, 4]:
            raise ValueError("Quarter must be 1, 2, 3, or 4")
        
        # Map quarter to months
        month_ranges = {
            1: ['01', '02', '03'],
            2: ['04', '05', '06'],
            3: ['07', '08', '09'],
            4: ['10', '11', '12']
        }
        
        months = [f"{year}-{m}" for m in month_ranges[q]]
        return year, q, months
    
    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid quarter format. Use YYYY-Q1, YYYY-Q2, YYYY-Q3, or YYYY-Q4")


def filter_by_quarter(records, months):
    """Filter records for specified quarter months."""
    return [r for r in records if r['date'] and r['date'][:7] in months]


def generate_quarterly_stats(records, by_month=False):
    """Generate quarterly statistics."""
    total = len(records)
    
    # By month (if requested)
    month_breakdown = None
    if by_month:
        month_breakdown = Counter(r['date'][:7] for r in records if r['date'])
    
    # By stream
    streams = Counter(r['stream'] for r in records if r['stream'])
    
    # By system (grouped)
    systems = Counter()
    for r in records:
        if r['system']:
            sys = r['system']
            if 'DCS' in sys or 'Experion' in sys:
                systems['DCS'] += 1
            elif 'PLC' in sys or 'ControlLogix' in sys or 'Studio' in sys:
                systems['PLC'] += 1
            elif 'SIS' in sys or 'Triconex' in sys:
                systems['SIS'] += 1
            elif 'Alarm' in sys:
                systems['Alarm'] += 1
            elif 'Network' in sys:
                systems['Network'] += 1
            elif 'HMI' in sys:
                systems['HMI'] += 1
            else:
                systems['Other'] += 1
    
    # By complexity
    complexity = Counter(r['complexity'] for r in records if r['complexity'])
    
    # By business impact
    impact = Counter(r['business_impact'] for r in records if r['business_impact'])
    
    # By resolution
    resolution = Counter(r['resolution'] for r in records if r['resolution'])
    
    return {
        'total': total,
        'month_breakdown': dict(month_breakdown) if month_breakdown else None,
        'streams': dict(streams),
        'systems': dict(systems),
        'complexity': dict(complexity),
        'impact': dict(impact),
        'resolution': dict(resolution)
    }


def create_summary_sheet(stats, quarter_name, months):
    """Create quarterly summary sheet."""
    rows = []
    
    rows.append(['PC VALUE TRACKER — QUARTERLY SUMMARY', ''])
    rows.append(['Quarter:', quarter_name])
    rows.append(['Generated:', datetime.now().strftime('%Y-%m-%d %H:%M')])
    rows.append(['', ''])
    
    rows.append(['TOTAL ISSUES', stats['total']])
    rows.append(['', ''])
    
    # Monthly breakdown
    if stats['month_breakdown']:
        rows.append(['BY MONTH', 'Count'])
        for month in sorted(stats['month_breakdown'].keys()):
            month_name = datetime.strptime(month, '%Y-%m').strftime('%B %Y')
            rows.append([month_name, stats['month_breakdown'][month]])
        rows.append(['', ''])
    
    # By Stream
    rows.append(['BY STREAM', 'Count'])
    for stream, count in sorted(stats['streams'].items(), key=lambda x: -x[1]):
        pct = (count / stats['total']) * 100 if stats['total'] > 0 else 0
        rows.append([stream, f"{count} ({pct:.1f}%)"])
    rows.append(['', ''])
    
    # By System
    rows.append(['BY SYSTEM', 'Count'])
    for system, count in sorted(stats['systems'].items(), key=lambda x: -x[1]):
        pct = (count / stats['total']) * 100 if stats['total'] > 0 else 0
        rows.append([system, f"{count} ({pct:.1f}%)"])
    rows.append(['', ''])
    
    # By Complexity
    rows.append(['BY COMPLEXITY', 'Count'])
    complexity_order = {'Quick': 1, 'Low': 2, 'Moderate': 3, 'Medium': 4, 'Major': 5, 'High': 6}
    sorted_complexity = sorted(stats['complexity'].items(), 
                              key=lambda x: complexity_order.get(x[0], 99))
    for comp, count in sorted_complexity:
        pct = (count / stats['total']) * 100 if stats['total'] > 0 else 0
        rows.append([comp, f"{count} ({pct:.1f}%)"])
    rows.append(['', ''])
    
    # By Business Impact
    rows.append(['BY BUSINESS IMPACT', 'Count'])
    impact_order = {'Production': 1, 'Safety': 2, 'Compliance': 3, 'Efficiency': 4, 'Reliability': 5, 'Low': 6}
    sorted_impact = sorted(stats['impact'].items(),
                          key=lambda x: impact_order.get(x[0], 99))
    for imp, count in sorted_impact:
        pct = (count / stats['total']) * 100 if stats['total'] > 0 else 0
        rows.append([imp, f"{count} ({pct:.1f}%)"])
    rows.append(['', ''])
    
    # By Resolution (if available)
    if stats['resolution']:
        rows.append(['BY RESOLUTION', 'Count'])
        for res, count in sorted(stats['resolution'].items(), key=lambda x: -x[1]):
            rows.append([res, count])
    
    return pd.DataFrame(rows, columns=['Metric', 'Value'])


def create_detail_sheet(records):
    """Create detailed issue list sorted by date."""
    df_data = []
    
    for r in sorted(records, key=lambda x: x['date'] or '9999-99-99'):
        df_data.append({
            'Date': r['date'],
            'System': r['system'],
            'Summary': r['summary'],
            'Stream': r['stream'],
            'Complexity': r['complexity'],
            'Resolution': r['resolution'],
            'Business Impact': r['business_impact']
        })
    
    return pd.DataFrame(df_data)


def create_stream_scorecard(records):
    """Create stream-focused scorecard with key metrics."""
    # Group by stream
    by_stream = {}
    for r in records:
        stream = r['stream'] or 'Unclassified'
        if stream not in by_stream:
            by_stream[stream] = []
        by_stream[stream].append(r)
    
    rows = []
    rows.append(['STREAM SCORECARD', '', '', '', ''])
    rows.append(['Stream', 'Count', 'High Complexity', 'Safety Impact', 'Key Systems'])
    rows.append(['', '', '', '', ''])
    
    for stream in sorted(by_stream.keys()):
        stream_records = by_stream[stream]
        count = len(stream_records)
        
        # Count high complexity (Major, High)
        high_complex = len([r for r in stream_records 
                           if r['complexity'] in ['Major', 'High', 'Medium']])
        
        # Count safety impact
        safety = len([r for r in stream_records 
                     if r['business_impact'] == 'Safety'])
        
        # Top systems
        systems = Counter(r['system'] for r in stream_records if r['system'])
        top_systems = ', '.join([s for s, _ in systems.most_common(3)])
        
        rows.append([stream, count, high_complex, safety, top_systems])
    
    rows.append(['', '', '', '', ''])
    rows.append(['', '', '', '', ''])
    
    # Now add detailed breakdown for each stream
    for stream in sorted(by_stream.keys()):
        stream_records = by_stream[stream]
        rows.append([f'=== {stream.upper()} ({len(stream_records)} issues) ===', '', '', '', ''])
        rows.append(['Date', 'System', 'Summary', 'Complexity', 'Impact'])
        
        for r in sorted(stream_records, key=lambda x: x['date'] or ''):
            rows.append([
                r['date'],
                r['system'],
                r['summary'][:80] if r['summary'] else '',
                r['complexity'],
                r['business_impact']
            ])
        
        rows.append(['', '', '', '', ''])
    
    return pd.DataFrame(rows, columns=['Stream', 'Count', 'High Complexity', 'Safety Impact', 'Key Systems'])


def create_trend_sheet(records, months):
    """Create monthly trend analysis."""
    rows = []
    rows.append(['QUARTERLY TRENDS', '', '', ''])
    rows.append(['', '', '', ''])
    
    # Group by month
    by_month = {}
    for month in months:
        by_month[month] = [r for r in records if r['date'] and r['date'].startswith(month)]
    
    # Create trend table
    rows.append(['Month', 'Total Issues', 'High Complexity', 'Top Stream', 'Top System'])
    
    for month in sorted(by_month.keys()):
        month_records = by_month[month]
        month_name = datetime.strptime(month, '%Y-%m').strftime('%b %Y')
        total = len(month_records)
        
        if total == 0:
            rows.append([month_name, 0, 0, 'N/A', 'N/A'])
            continue
        
        # High complexity count
        high_complex = len([r for r in month_records 
                           if r['complexity'] in ['Major', 'High', 'Medium']])
        
        # Top stream
        streams = Counter(r['stream'] for r in month_records if r['stream'])
        top_stream = streams.most_common(1)[0][0] if streams else 'N/A'
        
        # Top system (grouped)
        systems = Counter()
        for r in month_records:
            if r['system']:
                sys = r['system']
                if 'DCS' in sys or 'Experion' in sys:
                    systems['DCS'] += 1
                elif 'PLC' in sys or 'ControlLogix' in sys:
                    systems['PLC'] += 1
                elif 'SIS' in sys or 'Triconex' in sys:
                    systems['SIS'] += 1
                elif 'Alarm' in sys:
                    systems['Alarm'] += 1
                else:
                    systems['Other'] += 1
        top_system = systems.most_common(1)[0][0] if systems else 'N/A'
        
        rows.append([month_name, total, high_complex, top_stream, top_system])
    
    return pd.DataFrame(rows, columns=['Month', 'Total Issues', 'High Complexity', 'Top Stream', 'Top System'])


def generate_report(master_file, quarter, output_dir, verbose=False):
    """Generate the full quarterly report."""
    
    # Parse quarter
    try:
        year, q, months = parse_quarter(quarter)
        quarter_name = f"Q{q} {year}"
    except ValueError as e:
        print(f"Error: {e}")
        return False
    
    # Load data
    if verbose:
        print(f"Loading data from {master_file}...")
    records = load_master_data(master_file)
    
    # Filter by quarter
    quarter_records = filter_by_quarter(records, months)
    
    if not quarter_records:
        print(f"⚠️  No records found for {quarter_name}")
        return False
    
    if verbose:
        print(f"Found {len(quarter_records)} records for {quarter_name}")
        for month in months:
            count = len([r for r in quarter_records if r['date'] and r['date'].startswith(month)])
            if count > 0:
                print(f"  {month}: {count} records")
    
    # Generate statistics
    stats = generate_quarterly_stats(quarter_records, by_month=True)
    
    # Create output filename
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    output_file = output_path / f"Quarterly_Report_{year}-Q{q}.xlsx"
    
    # Create Excel file with multiple sheets
    if verbose:
        print(f"Creating Excel report...")
    
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # Summary sheet
        df_summary = create_summary_sheet(stats, quarter_name, months)
        df_summary.to_excel(writer, sheet_name='Summary', index=False, header=False)
        
        # Trend sheet
        df_trends = create_trend_sheet(quarter_records, months)
        df_trends.to_excel(writer, sheet_name='Trends', index=False, header=False)
        
        # Stream scorecard
        df_scorecard = create_stream_scorecard(quarter_records)
        df_scorecard.to_excel(writer, sheet_name='Stream Scorecard', index=False, header=False)
        
        # Detail sheet
        df_detail = create_detail_sheet(quarter_records)
        df_detail.to_excel(writer, sheet_name='All Issues', index=False)
        
        # Format Summary sheet
        workbook = writer.book
        summary_sheet = writer.sheets['Summary']
        
        # Set column widths
        summary_sheet.column_dimensions['A'].width = 30
        summary_sheet.column_dimensions['B'].width = 20
        
        # Bold headers
        from openpyxl.styles import Font
        for cell in summary_sheet['A']:
            if cell.value and isinstance(cell.value, str) and cell.value.isupper():
                cell.font = Font(bold=True, size=12)
    
    print(f"\n✅ Quarterly report generated!")
    print(f"   Quarter: {quarter_name}")
    print(f"   Issues: {len(quarter_records)}")
    print(f"   Output: {output_file}")
    
    return True


def main():
    parser = argparse.ArgumentParser(description='Generate quarterly summary report')
    parser.add_argument('--master', default='data/master.json', help='Master data file')
    parser.add_argument('--quarter', required=True, help='Quarter to report (YYYY-Q1, YYYY-Q2, etc.)')
    parser.add_argument('--output-dir', default='output/quarterly', help='Output directory')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    success = generate_report(args.master, args.quarter, args.output_dir, args.verbose)
    
    if not success:
        exit(1)


if __name__ == '__main__':
    main()
