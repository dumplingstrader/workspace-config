#!/usr/bin/env python3
"""
Archive Processed Raw Files

Moves processed Excel files from data/raw/ to organized archive folders.
Organizes by year-month automatically based on file modification date.
"""

import shutil
from pathlib import Path
from datetime import datetime
import argparse


def get_file_month(file_path):
    """Get year-month from file modification date."""
    mtime = file_path.stat().st_mtime
    dt = datetime.fromtimestamp(mtime)
    return dt.strftime('%Y-%m')


def archive_files(raw_dir, archive_base, by_month=True, dry_run=False, verbose=False):
    """
    Archive Excel files from raw directory.
    
    Args:
        raw_dir: Source directory (data/raw/)
        archive_base: Archive base directory (data/archive/)
        by_month: Organize by YYYY-MM folders
        dry_run: Show what would be done without moving files
        verbose: Show detailed progress
    """
    raw_path = Path(raw_dir)
    archive_path = Path(archive_base)
    
    if not raw_path.exists():
        print(f"❌ Error: {raw_dir} does not exist")
        return False
    
    # Find all Excel files
    excel_files = list(raw_path.glob('*.xlsx')) + list(raw_path.glob('*.xls'))
    
    if not excel_files:
        print(f"ℹ️  No Excel files found in {raw_dir}")
        return True
    
    print(f"\n{'[DRY RUN] ' if dry_run else ''}Found {len(excel_files)} file(s) to archive")
    print("=" * 60)
    
    # Group files by destination
    by_destination = {}
    
    for file_path in excel_files:
        if by_month:
            month = get_file_month(file_path)
            dest_dir = archive_path / month
        else:
            dest_dir = archive_path
        
        if dest_dir not in by_destination:
            by_destination[dest_dir] = []
        by_destination[dest_dir].append(file_path)
    
    # Archive files
    total_moved = 0
    
    for dest_dir in sorted(by_destination.keys()):
        files = by_destination[dest_dir]
        
        # Display path relative to current directory or as absolute
        try:
            display_path = dest_dir.relative_to(Path.cwd())
        except ValueError:
            display_path = dest_dir
        
        print(f"\n📁 {display_path}/")
        
        if not dry_run:
            dest_dir.mkdir(parents=True, exist_ok=True)
        
        for file_path in sorted(files):
            dest_file = dest_dir / file_path.name
            
            if verbose or dry_run:
                print(f"   {'→' if dry_run else '✓'} {file_path.name}")
            
            if not dry_run:
                try:
                    shutil.move(str(file_path), str(dest_file))
                    total_moved += 1
                except Exception as e:
                    print(f"   ❌ Error moving {file_path.name}: {e}")
        
        if not verbose and not dry_run:
            print(f"   ✓ Moved {len(files)} file(s)")
    
    print("\n" + "=" * 60)
    
    if dry_run:
        print(f"\n🔍 DRY RUN: Would move {len(excel_files)} file(s)")
        print("   Run without --dry-run to actually move files")
    else:
        print(f"\n✅ Archived {total_moved} file(s)")
        print(f"   Raw folder: {raw_dir}")
        print(f"   Archive: {archive_base}")
    
    return True


def main():
    parser = argparse.ArgumentParser(
        description='Archive processed raw Excel files',
        epilog='Example: python archive_raw_files.py --by-month --verbose'
    )
    parser.add_argument('--raw-dir', default='data/raw', help='Raw files directory')
    parser.add_argument('--archive-dir', default='data/archive', help='Archive base directory')
    parser.add_argument('--by-month', action='store_true', default=True, 
                       help='Organize by YYYY-MM folders (default)')
    parser.add_argument('--flat', action='store_true', 
                       help='Archive to single folder (not by month)')
    parser.add_argument('--dry-run', '-n', action='store_true', 
                       help='Show what would be done without moving files')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show detailed progress')
    
    args = parser.parse_args()
    
    # If --flat specified, disable by-month
    by_month = args.by_month and not args.flat
    
    success = archive_files(
        args.raw_dir,
        args.archive_dir,
        by_month=by_month,
        dry_run=args.dry_run,
        verbose=args.verbose
    )
    
    if not success:
        exit(1)


if __name__ == '__main__':
    main()
