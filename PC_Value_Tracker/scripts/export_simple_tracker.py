"""
Process Controls Value Tracker - Simple Excel Export
====================================================
Export JSON data directly to Excel with multiple analysis sheets.

Usage:
    python scripts/export_simple_tracker.py --input data/master_combined.json --output output/pc_value_tracker.xlsx

Author: Tony Chiu
Created: January 2026
"""

import pandas as pd
import json
from pathlib import Path
import argparse


def load_json(filepath: str) -> dict:
    """Load JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def create_tracker_excel(data: dict, output_path: Path):
    """Create Excel tracker with multiple sheets."""
    
    entries = data.get('entries', [])
    if not entries:
        print("No entries found in data.")
        return
    
    # Create main DataFrame
    df = pd.DataFrame(entries)
    
    print(f"\nCreating Excel tracker with {len(df)} entries...\n")
    
    # Create Excel writer
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        
        # Sheet 1: All Data
        df_export = df.copy()
        df_export.to_excel(writer, sheet_name='All_Data', index=False)
        print("✓ Created sheet: All_Data")
        
        # Sheet 2: Summary Statistics
        summary_data = {
            'Metric': [
                'Total Entries',
                'Unique Requesters',
                'Systems Covered',
                'Areas/Units Covered',
                'Date Range'
            ],
            'Value': [
                len(df),
                df['Requester'].nunique() if 'Requester' in df.columns else 'N/A',
                df['System'].nunique() if 'System' in df.columns else 'N/A',
                df['Area_Unit'].nunique() if 'Area_Unit' in df.columns else 'N/A',
                f"{df['Date'].min()} to {df['Date'].max()}" if 'Date' in df.columns else 'N/A'
            ]
        }
        df_summary = pd.DataFrame(summary_data)
        df_summary.to_excel(writer, sheet_name='Summary', index=False)
        print("✓ Created sheet: Summary")
        
        # Sheet 3: By System
        if 'System' in df.columns:
            df_by_system = df.groupby('System').size().reset_index(name='Count')
            df_by_system = df_by_system.sort_values('Count', ascending=False)
            df_by_system.to_excel(writer, sheet_name='By_System', index=False)
            print("✓ Created sheet: By_System")
        
        # Sheet 4: By Area
        if 'Area_Unit' in df.columns:
            df_by_area = df.groupby('Area_Unit').size().reset_index(name='Count')
            df_by_area = df_by_area.sort_values('Count', ascending=False)
            df_by_area.to_excel(writer, sheet_name='By_Area', index=False)
            print("✓ Created sheet: By_Area")
        
        # Sheet 5: By Year
        if 'Date' in df.columns:
            df['Year'] = pd.to_datetime(df['Date'], errors='coerce').dt.year
            df_by_year = df.groupby('Year').size().reset_index(name='Count')
            df_by_year.to_excel(writer, sheet_name='By_Year', index=False)
            print("✓ Created sheet: By_Year")
        
        # Sheet 6: By Complexity
        if 'Complexity' in df.columns:
            df_by_complexity = df.groupby('Complexity').size().reset_index(name='Count')
            df_by_complexity.to_excel(writer, sheet_name='By_Complexity', index=False)
            print("✓ Created sheet: By_Complexity")
        
        # Sheet 7: High Priority (Major/Significant complexity)
        if 'Complexity' in df.columns:
            df_high = df[df['Complexity'].str.contains('Major|Significant|Ongoing', case=False, na=False)]
            if len(df_high) > 0:
                df_high.to_excel(writer, sheet_name='High_Complexity', index=False)
                print(f"✓ Created sheet: High_Complexity ({len(df_high)} entries)")
        
        # Sheet 8: Cross-Site Work
        if 'Requester_Dept' in df.columns:
            df_cross = df[df['Requester_Dept'].str.contains('Other Site|Corporate', case=False, na=False)]
            if len(df_cross) > 0:
                df_cross.to_excel(writer, sheet_name='Cross_Site', index=False)
                print(f"✓ Created sheet: Cross_Site ({len(df_cross)} entries)")
        
        # Sheet 9: Training/Mentorship
        if 'My_Role' in df.columns:
            df_training = df[df['My_Role'].str.contains('Trained|Consulted', case=False, na=False)]
            if len(df_training) > 0:
                df_training.to_excel(writer, sheet_name='Training', index=False)
                print(f"✓ Created sheet: Training ({len(df_training)} entries)")
    
    print(f"\n{'='*60}")
    print(f"✓ Excel tracker created: {output_path}")
    print('='*60)


def main():
    parser = argparse.ArgumentParser(description='Export JSON to Excel tracker')
    parser.add_argument('--input', '-i', required=True, help='Input JSON file')
    parser.add_argument('--output', '-o', default='output/pc_value_tracker.xlsx', help='Output Excel file')
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    output_path = Path(args.output)
    
    if not input_path.exists():
        print(f"Input file not found: {input_path}")
        return
    
    # Load data
    data = load_json(input_path)
    
    # Create output folder
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Create tracker
    create_tracker_excel(data, output_path)
    
    print(f"\nYou can now open and review: {output_path}")


if __name__ == '__main__':
    main()
