"""
Process Controls Value Tracker - Excel to JSON Converter
=========================================================
Converts Excel file to JSON format expected by enrichment scripts.

Usage:
    python scripts/excel_to_json.py --input data/master_combined_issues.xlsx --output data/master_combined.json

Author: Tony Chiu
Created: January 2026
"""

import pandas as pd
import json
from pathlib import Path
import argparse
from datetime import datetime


def excel_to_json(input_path: Path, output_path: Path):
    """Convert Excel file to JSON format for enrichment pipeline."""
    
    print(f"\nConverting {input_path.name} to JSON...\n")
    
    # Read Excel file
    df = pd.read_excel(input_path)
    print(f"Loaded {len(df)} rows from Excel")
    
    # Convert to list of dictionaries
    records = df.to_dict('records')
    
    # Convert dates to strings for JSON serialization
    for record in records:
        for key, value in record.items():
            if pd.isna(value):
                record[key] = None
            elif isinstance(value, (pd.Timestamp, datetime)):
                record[key] = value.strftime('%Y-%m-%d %H:%M:%S') if value else None
            elif isinstance(value, (int, float)) and pd.isna(value):
                record[key] = None
    
    # Create output structure
    output_data = {
        "metadata": {
            "source_file": input_path.name,
            "conversion_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "total_entries": len(records)
        },
        "entries": records
    }
    
    # Save to JSON
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Converted {len(records)} entries to JSON")
    print(f"✓ Saved to: {output_path}")
    
    # Show sample of first entry
    if records:
        print(f"\nSample entry (fields):")
        for key in list(records[0].keys())[:10]:  # Show first 10 fields
            print(f"  - {key}")
        if len(records[0]) > 10:
            print(f"  ... and {len(records[0]) - 10} more fields")
    
    print(f"\nNext step:")
    print(f"  python scripts/enrich_entries.py --input {output_path} --output output/enriched_entries.json")


def main():
    parser = argparse.ArgumentParser(description='Convert Excel to JSON for enrichment pipeline')
    parser.add_argument('--input', '-i', required=True, help='Input Excel file')
    parser.add_argument('--output', '-o', help='Output JSON file (default: same name as input)')
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    
    if not input_path.exists():
        print(f"Input file not found: {input_path}")
        return
    
    # Default output path
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = input_path.with_suffix('.json')
    
    excel_to_json(input_path, output_path)


if __name__ == '__main__':
    main()
