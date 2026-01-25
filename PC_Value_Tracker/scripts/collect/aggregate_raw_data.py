#!/usr/bin/env python3
"""
Aggregate raw Copilot exports into master.json

Reads all Excel files from data/raw/ and consolidates them into the master database.
Handles both V2.0 format (Date/System/Summary/Stream/Complexity/Resolution/Business Impact)
and historical formats with different column structures.
"""

import pandas as pd
import json
import shutil
from pathlib import Path
from datetime import datetime
import argparse


def normalize_date(date_value):
    """Convert various date formats to YYYY-MM-DD string."""
    if pd.isna(date_value):
        return None
    
    if isinstance(date_value, str):
        # Try parsing various formats
        for fmt in ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%Y/%m/%d']:
            try:
                return datetime.strptime(date_value, fmt).strftime('%Y-%m-%d')
            except ValueError:
                continue
        return date_value  # Return as-is if can't parse
    
    # If it's already a datetime
    if isinstance(date_value, (pd.Timestamp, datetime)):
        return date_value.strftime('%Y-%m-%d')
    
    return str(date_value)


def read_v2_format(file_path):
    """
    Read V2.0 format Excel files (LastMonth_*.xlsx).
    Columns: Date, System, Summary, Stream, Complexity, Resolution, Business Impact
    """
    df = pd.read_excel(file_path)
    
    records = []
    for _, row in df.iterrows():
        record = {
            'date': normalize_date(row.get('Date')),
            'system': str(row.get('System', '')).strip() if pd.notna(row.get('System')) else '',
            'summary': str(row.get('Summary', '')).strip() if pd.notna(row.get('Summary')) else '',
            'stream': str(row.get('Stream', '')).strip() if pd.notna(row.get('Stream')) else '',
            'complexity': str(row.get('Complexity', '')).strip() if pd.notna(row.get('Complexity')) else '',
            'resolution': str(row.get('Resolution', '')).strip() if pd.notna(row.get('Resolution')) else '',
            'business_impact': str(row.get('Business Impact', '')).strip() if pd.notna(row.get('Business Impact')) else '',
            'source_file': file_path.name
        }
        records.append(record)
    
    return records


def read_historical_format(file_path):
    """
    Read historical format Excel files (TonyChiu_*_Sent_Support_Emails_*.xlsx).
    Columns: Date, Subject, System Category, System, Stream, Complexity, 
             Business Impact, Your Action, Evidence Snippet, Reference
    """
    df = pd.read_excel(file_path)
    
    records = []
    for _, row in df.iterrows():
        # Combine Subject and Your Action for summary
        subject = str(row.get('Subject', '')).strip() if pd.notna(row.get('Subject')) else ''
        action = str(row.get('Your Action', '')).strip() if pd.notna(row.get('Your Action')) else ''
        summary = f"{subject}: {action}" if subject and action else (subject or action)
        
        # Use System from "System" column, fallback to "System Category"
        system = str(row.get('System', '')).strip() if pd.notna(row.get('System')) else ''
        if not system:
            system = str(row.get('System Category', '')).strip() if pd.notna(row.get('System Category')) else ''
        
        # Map "Routine Support" to "Day-to-Day" for consistency
        stream = str(row.get('Stream', '')).strip() if pd.notna(row.get('Stream')) else ''
        if stream == 'Routine Support':
            stream = 'Day-to-Day'
        
        record = {
            'date': normalize_date(row.get('Date')),
            'system': system,
            'summary': summary,
            'stream': stream,
            'complexity': str(row.get('Complexity', '')).strip() if pd.notna(row.get('Complexity')) else '',
            'resolution': '',  # Not in historical format
            'business_impact': str(row.get('Business Impact', '')).strip() if pd.notna(row.get('Business Impact')) else '',
            'source_file': file_path.name,
            'reference': str(row.get('Reference', '')).strip() if pd.notna(row.get('Reference')) else ''
        }
        records.append(record)
    
    return records


def aggregate_all_files(raw_dir, output_file, verbose=False):
    """
    Aggregate all Excel files from raw directory into master.json.
    
    IMPORTANT: This function preserves existing data in master.json.
    Only NEW records from raw files are added. Existing records are never deleted.
    This makes master.json the persistent source of truth.
    """
    raw_path = Path(raw_dir)
    output_path = Path(output_file)
    
    # Load existing master.json first (if it exists)
    existing_records = []
    if output_path.exists():
        if verbose:
            print(f"Loading existing data from {output_file}...")
        try:
            with open(output_path, 'r', encoding='utf-8') as f:
                existing_records = json.load(f)
            if verbose:
                print(f"  → Found {len(existing_records)} existing records")
        except Exception as e:
            print(f"Warning: Could not load existing master.json: {e}")
            print("Starting fresh...")
    
    # Find all Excel files in raw directory
    if not raw_path.exists():
        print(f"Warning: Directory {raw_dir} does not exist")
        if existing_records:
            print(f"Keeping {len(existing_records)} existing records in master.json")
            return True
        return False
    
    excel_files = list(raw_path.glob('*.xlsx')) + list(raw_path.glob('*.xls'))
    
    if not excel_files:
        print(f"No Excel files found in {raw_dir}")
        if existing_records:
            print(f"Keeping {len(existing_records)} existing records in master.json")
            return True
        return False
    
    # Process raw files
    new_records = []
    
    for file_path in sorted(excel_files):
        if verbose:
            print(f"Processing: {file_path.name}")
        
        try:
            # Detect format by filename pattern
            if file_path.name.startswith('LastMonth_'):
                records = read_v2_format(file_path)
            elif 'Sent_Support_Emails' in file_path.name:
                records = read_historical_format(file_path)
            else:
                # Try V2 format as default
                records = read_v2_format(file_path)
            
            new_records.extend(records)
            
            if verbose:
                print(f"  → Extracted {len(records)} records")
        
        except Exception as e:
            print(f"Error processing {file_path.name}: {e}")
            continue
    
    # Combine existing and new records
    all_records = existing_records + new_records
    
    # Remove duplicates based on date + summary
    unique_records = []
    seen = set()
    
    for record in all_records:
        key = (record['date'], record['summary'][:100])  # Use first 100 chars of summary
        if key not in seen:
            seen.add(key)
            unique_records.append(record)
    
    # Sort by date
    unique_records.sort(key=lambda x: x['date'] or '9999-99-99')
    
    # Calculate what's new
    new_count = len(unique_records) - len(existing_records)
    
    # Save to JSON
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(unique_records, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Aggregation complete!")
    print(f"   Existing records: {len(existing_records)}")
    print(f"   New records added: {new_count}")
    print(f"   Total records: {len(unique_records)}")
    print(f"   Saved to: {output_file}")
    
    if new_count > 0:
        print(f"\n   💡 You can now safely move or delete processed files from {raw_dir}")
    
    # Summary by year
    by_year = {}
    for record in unique_records:
        if record['date']:
            year = record['date'][:4]
            by_year[year] = by_year.get(year, 0) + 1
    
    print(f"\n   By year:")
    for year in sorted(by_year.keys()):
        print(f"     {year}: {by_year[year]} records")
    
    return True


def archive_processed_files(raw_dir, archive_base, verbose=False):
    """Archive processed Excel files to organized folders by month."""
    raw_path = Path(raw_dir)
    archive_path = Path(archive_base)
    
    excel_files = list(raw_path.glob('*.xlsx')) + list(raw_path.glob('*.xls'))
    
    if not excel_files:
        if verbose:
            print("\nℹ️  No files to archive")
        return True
    
    print(f"\n📦 Archiving {len(excel_files)} processed file(s)...")
    
    # Group files by month (based on modification date)
    by_month = {}
    for file_path in excel_files:
        mtime = file_path.stat().st_mtime
        dt = datetime.fromtimestamp(mtime)
        month = dt.strftime('%Y-%m')
        
        if month not in by_month:
            by_month[month] = []
        by_month[month].append(file_path)
    
    # Move files
    total_moved = 0
    for month in sorted(by_month.keys()):
        files = by_month[month]
        dest_dir = archive_path / month
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        if verbose:
            try:
                display_path = dest_dir.relative_to(Path.cwd())
            except ValueError:
                display_path = dest_dir
            print(f"   → {display_path}/")
        
        for file_path in files:
            try:
                dest_file = dest_dir / file_path.name
                shutil.move(str(file_path), str(dest_file))
                total_moved += 1
                if verbose:
                    print(f"      ✓ {file_path.name}")
            except Exception as e:
                print(f"      ❌ Error moving {file_path.name}: {e}")
    
    print(f"   ✅ Archived {total_moved} file(s) to {archive_base}")
    return True


def main():
    parser = argparse.ArgumentParser(description='Aggregate raw Copilot exports into master.json')
    parser.add_argument('--raw-dir', default='data/raw', help='Directory with raw Excel files')
    parser.add_argument('--output', default='data/master.json', help='Output JSON file')
    parser.add_argument('--archive', action='store_true', help='Archive processed files after aggregation')
    parser.add_argument('--archive-dir', default='data/archive', help='Archive directory (used with --archive)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    success = aggregate_all_files(args.raw_dir, args.output, args.verbose)
    
    if not success:
        exit(1)
    
    # Archive files if requested
    if args.archive:
        archive_success = archive_processed_files(args.raw_dir, args.archive_dir, args.verbose)
        if not archive_success:
            exit(1)


if __name__ == '__main__':
    main()
