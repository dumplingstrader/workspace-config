"""
Process Controls Value Tracker - Combine Multiple Excel Files
==============================================================
Combines multiple Copilot export Excel files into one PERSISTENT master file.

PERSISTENT DATABASE MODE:
- Reads existing master file FIRST (preserves all historical data)
- Adds new Excel files from data folder
- Removes duplicates based on Date + Subject + Issue_Summary
- Saves back to master file (cumulative, never loses data)

Workflow:
1. Add new Copilot exports to data folder
2. Run this script to merge them into master
3. Delete/archive individual exports (data is safe in master file)

Usage:
    python scripts/combine_excel_files.py --output data/master_combined_issues.xlsx

Author: Tony Chiu
Created: January 2026
Updated: January 2026 - Added persistent database mode
"""

import pandas as pd
from pathlib import Path
import argparse


def load_excel_file(filepath: Path) -> pd.DataFrame:
    """Load Excel file and standardize column names."""
    try:
        df = pd.read_excel(filepath)
        
        # Standardize column names (remove extra spaces, normalize case)
        df.columns = df.columns.str.strip()
        
        # Add source file tracking
        df['Source_File'] = filepath.name
        
        print(f"  ✓ Loaded {len(df)} rows from {filepath.name}")
        return df
    except Exception as e:
        print(f"  ✗ Error loading {filepath.name}: {e}")
        return None


def combine_excel_files(data_folder: Path, output_path: Path):
    """Combine all Excel files in data folder into one PERSISTENT master file."""
    
    print(f"\nScanning {data_folder} for Excel files...\n")
    
    # STEP 1: Load existing master file FIRST (persistent database)
    existing_data = None
    if output_path.exists():
        print(f"📊 Loading existing master file: {output_path.name}")
        try:
            existing_data = pd.read_excel(output_path)
            print(f"  ✓ Found {len(existing_data)} existing entries")
            # Ensure Source_File column exists
            if 'Source_File' not in existing_data.columns:
                existing_data['Source_File'] = 'master_file'
        except Exception as e:
            print(f"  ⚠️ Could not load existing master file: {e}")
            existing_data = None
    else:
        print(f"📝 No existing master file found. Creating new database.")
    
    print()
    
    # STEP 2: Find new Excel files to add (exclude master file itself)
    excel_files = [f for f in data_folder.glob('*.xlsx') 
                   if not f.name.startswith('master_') 
                   and not f.name.startswith('~$')
                   and f != output_path]
    
    if not excel_files and existing_data is None:
        print("No Excel files found and no existing master file.")
        return
    
    if excel_files:
        print(f"Found {len(excel_files)} new Excel files:\n")
        for f in excel_files:
            print(f"  - {f.name}")
        print()
    else:
        print("No new Excel files to add.\n")
    
    # STEP 3: Load all new files
    dataframes = []
    
    # Add existing master data FIRST
    if existing_data is not None:
        dataframes.append(existing_data)
    
    # Add new files
    for filepath in excel_files:
        df = load_excel_file(filepath)
        if df is not None and len(df) > 0:
            dataframes.append(df)
    
    if not dataframes:
        print("\n⚠️ No data to process.")
        return
    
    print(f"\n{'='*60}")
    print("Combining data (PERSISTENT MODE)...")
    print('='*60)
    
    # Combine all dataframes
    combined = pd.concat(dataframes, ignore_index=True, sort=False)
    
    if existing_data is not None:
        print(f"Existing entries: {len(existing_data)}")
        print(f"New entries loaded: {len(combined) - len(existing_data)}")
    
    print(f"Total rows before deduplication: {len(combined)}")
    
    # Remove duplicates based on key fields
    # Try different combinations of fields that might exist
    dedupe_columns = []
    
    if 'Date' in combined.columns:
        dedupe_columns.append('Date')
    if 'Subject' in combined.columns:
        dedupe_columns.append('Subject')
    elif 'Issue_Summary' in combined.columns:
        dedupe_columns.append('Issue_Summary')
    
    if dedupe_columns:
        before_count = len(combined)
        combined = combined.drop_duplicates(subset=dedupe_columns, keep='first')
        removed = before_count - len(combined)
        print(f"Removed {removed} duplicate rows")
    
    print(f"Total unique rows: {len(combined)}")
    
    # Sort by date if available
    if 'Date' in combined.columns:
        combined['Date'] = pd.to_datetime(combined['Date'], errors='coerce')
        combined = combined.sort_values('Date', ascending=False)
        print("Sorted by date (newest first)")
    
    # Save to output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    combined.to_excel(output_path, index=False, sheet_name='Combined_Data')
    
    print(f"\n{'='*60}")
    print(f"✓ Saved PERSISTENT master file: {output_path}")
    print(f"✓ Total entries in database: {len(combined)}")
    print('='*60)
    
    # Summary by source file
    if 'Source_File' in combined.columns:
        print("\nRows per source file:")
        summary = combined['Source_File'].value_counts()
        for source, count in summary.items():
            print(f"  {source}: {count} rows")
    
    print(f"\n💡 Safe to delete/archive individual Excel files now - data is preserved in master!")
    print(f"\nNext steps:")
    print(f"1. Review {output_path.name} and clean up any issues")
    print(f"2. Convert to JSON: python scripts/excel_to_json.py --input {output_path}")
    print(f"3. Export tracker: python scripts/export_simple_tracker.py")


def main():
    parser = argparse.ArgumentParser(description='Combine multiple Excel files into master file')
    parser.add_argument('--data-folder', default='data', help='Folder containing Excel files')
    parser.add_argument('--output', '-o', default='data/master_combined_issues.xlsx', 
                       help='Output master file path')
    
    args = parser.parse_args()
    
    data_folder = Path(args.data_folder)
    output_path = Path(args.output)
    
    if not data_folder.exists():
        print(f"Data folder not found: {data_folder}")
        return
    
    combine_excel_files(data_folder, output_path)


if __name__ == '__main__':
    main()
