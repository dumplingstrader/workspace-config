#!/usr/bin/env python3
"""
Quick Data Summary

Shows a high-level summary of all data in master.json.
Useful for checking data coverage and identifying trends.
"""

import json
from collections import Counter
from pathlib import Path
import argparse


def show_summary(master_file):
    """Display comprehensive summary of master data."""
    
    with open(master_file, 'r', encoding='utf-8') as f:
        records = json.load(f)
    
    print("\n" + "="*60)
    print("PC VALUE TRACKER — DATA SUMMARY")
    print("="*60)
    
    # Total records
    print(f"\n📊 TOTAL RECORDS: {len(records)}")
    
    # By year-month
    by_month = Counter()
    for r in records:
        if r['date'] and len(r['date']) >= 7:
            by_month[r['date'][:7]] += 1
    
    print(f"\n📅 BY MONTH:")
    for month in sorted(by_month.keys()):
        print(f"   {month}: {by_month[month]:3d} issues")
    
    # By stream
    by_stream = Counter(r['stream'] for r in records if r['stream'])
    print(f"\n🎯 BY STREAM:")
    for stream, count in by_stream.most_common():
        pct = (count / len(records)) * 100
        print(f"   {stream:20s}: {count:3d} ({pct:5.1f}%)")
    
    # By system category
    by_system = Counter()
    for r in records:
        if r['system']:
            sys = r['system']
            if 'DCS' in sys or 'Experion' in sys:
                by_system['DCS'] += 1
            elif 'PLC' in sys or 'ControlLogix' in sys or 'Studio' in sys:
                by_system['PLC'] += 1
            elif 'SIS' in sys or 'Triconex' in sys:
                by_system['SIS'] += 1
            elif 'Alarm' in sys:
                by_system['Alarm'] += 1
            elif 'Network' in sys:
                by_system['Network'] += 1
            elif 'HMI' in sys:
                by_system['HMI'] += 1
            else:
                by_system['Other'] += 1
    
    print(f"\n🖥️  BY SYSTEM:")
    for system, count in by_system.most_common():
        pct = (count / len(records)) * 100
        print(f"   {system:20s}: {count:3d} ({pct:5.1f}%)")
    
    # By complexity
    by_complexity = Counter(r['complexity'] for r in records if r['complexity'])
    print(f"\n⚙️  BY COMPLEXITY:")
    for comp, count in by_complexity.most_common():
        pct = (count / len(records)) * 100
        print(f"   {comp:20s}: {count:3d} ({pct:5.1f}%)")
    
    # By business impact
    by_impact = Counter(r['business_impact'] for r in records if r['business_impact'])
    print(f"\n💼 BY BUSINESS IMPACT:")
    for impact, count in by_impact.most_common():
        pct = (count / len(records)) * 100
        print(f"   {impact:20s}: {count:3d} ({pct:5.1f}%)")
    
    # By resolution (if available)
    by_resolution = Counter(r['resolution'] for r in records if r['resolution'])
    if by_resolution:
        print(f"\n✅ BY RESOLUTION:")
        for res, count in by_resolution.most_common():
            pct = (count / len([r for r in records if r['resolution']])) * 100
            print(f"   {res:20s}: {count:3d} ({pct:5.1f}%)")
    
    # Data quality check
    print(f"\n🔍 DATA QUALITY:")
    missing_date = len([r for r in records if not r['date']])
    missing_system = len([r for r in records if not r['system']])
    missing_stream = len([r for r in records if not r['stream']])
    missing_summary = len([r for r in records if not r['summary']])
    
    print(f"   Missing date:    {missing_date:3d}")
    print(f"   Missing system:  {missing_system:3d}")
    print(f"   Missing stream:  {missing_stream:3d}")
    print(f"   Missing summary: {missing_summary:3d}")
    
    print("\n" + "="*60 + "\n")


def main():
    parser = argparse.ArgumentParser(description='Show data summary from master.json')
    parser.add_argument('--master', default='data/master.json', help='Master data file')
    
    args = parser.parse_args()
    
    master_path = Path(args.master)
    if not master_path.exists():
        print(f"Error: {args.master} not found")
        exit(1)
    
    show_summary(args.master)


if __name__ == '__main__':
    main()
