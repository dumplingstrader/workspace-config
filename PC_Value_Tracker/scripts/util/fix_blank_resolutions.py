#!/usr/bin/env python3
"""
Fix blank resolution fields in master.json by setting them to "Unknown".
This makes it easier to spot records that need resolution updates.
"""

import json
from pathlib import Path


def fix_blank_resolutions(master_file='data/master.json'):
    """Update blank resolution fields to 'Unknown'."""
    
    # Load data
    print(f"Loading {master_file}...")
    with open(master_file, 'r', encoding='utf-8') as f:
        records = json.load(f)
    
    print(f"Total records: {len(records)}")
    
    # Find and fix blank resolutions
    fixed_count = 0
    for record in records:
        resolution = record.get('resolution', '')
        if not resolution or resolution.strip() == '':
            record['resolution'] = 'Unknown'
            fixed_count += 1
    
    # Save updated data
    if fixed_count > 0:
        print(f"Fixed {fixed_count} blank resolution fields")
        
        # Backup original
        backup_file = Path(master_file).with_suffix('.json.backup')
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(records, f, indent=2, ensure_ascii=False)
        print(f"Backup saved to: {backup_file}")
        
        # Save updated
        with open(master_file, 'w', encoding='utf-8') as f:
            json.dump(records, f, indent=2, ensure_ascii=False)
        print(f"✅ Updated {master_file}")
        
        # Show resolution summary
        from collections import Counter
        resolution_counts = Counter(r['resolution'] for r in records if r.get('resolution'))
        print("\nResolution field summary:")
        for res, count in sorted(resolution_counts.items(), key=lambda x: -x[1]):
            print(f"  {res}: {count}")
    else:
        print("No blank resolution fields found!")
    
    return fixed_count


if __name__ == '__main__':
    fix_blank_resolutions()
