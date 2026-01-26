#!/usr/bin/env python3
"""
Re-apply V3.0 auto-classification to all records in master.json

This script reads master.json, applies classification rules to ALL records,
and saves the updated data. Use this after updating classification_rules.json
or to apply V3.0 rules to historical data.
"""

import json
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from collect.aggregate_raw_data import load_classification_rules, auto_classify_record


def reclassify_master(master_path, verbose=False):
    """Re-apply classification rules to all records in master.json"""

    master_file = Path(master_path)

    if not master_file.exists():
        print(f"Error: {master_path} not found")
        return False

    # Load classification rules
    rules_config = load_classification_rules()
    if not rules_config:
        print("Error: Could not load classification rules")
        return False

    if verbose:
        print(f"[OK] Loaded V3.0 classification rules")

    # Load master.json
    with open(master_file, 'r', encoding='utf-8') as f:
        records = json.load(f)

    if verbose:
        print(f"Loaded {len(records)} records from {master_path}")

    # Re-classify all records
    # First, clear existing classifications to force re-evaluation
    classified_count = 0
    resolution_changes = 0
    impact_changes = 0
    stream_changes = 0

    for record in records:
        # Store original values
        orig_resolution = record.get('resolution', '')
        orig_impact = record.get('business_impact', '')
        orig_stream = record.get('stream', '')

        # Clear resolution if Unknown to force re-classification
        if orig_resolution.lower() in ['unknown', '']:
            record['resolution'] = ''

        # Apply classification
        auto_classify_record(record, rules_config)

        # Count changes
        if record.get('corrected'):
            classified_count += 1
            corrections = record.get('corrected', '').split(',')
            if 'resolution' in corrections:
                resolution_changes += 1
            if 'business_impact' in corrections:
                impact_changes += 1
            if 'stream' in corrections:
                stream_changes += 1

    # Save updated master.json
    with open(master_file, 'w', encoding='utf-8') as f:
        json.dump(records, f, indent=2, ensure_ascii=False)

    print(f"\n[SUCCESS] Re-classification complete!")
    print(f"   Total records: {len(records)}")
    print(f"   Records modified: {classified_count}")
    print(f"   Resolution changes: {resolution_changes}")
    print(f"   Business Impact changes: {impact_changes}")
    print(f"   Stream changes: {stream_changes}")
    print(f"   Saved to: {master_path}")

    return True


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Re-apply V3.0 classification to master.json')
    parser.add_argument('--input', default='data/master.json', help='Path to master.json')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')

    args = parser.parse_args()

    success = reclassify_master(args.input, args.verbose)
    if not success:
        exit(1)
