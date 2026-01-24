"""
Process Controls Value Tracker - Archive Processed Files
=========================================================
Moves processed Excel files to archive folder after combining.

Usage:
    python scripts/archive_processed_files.py

Author: Tony Chiu
Created: January 2026
"""

from pathlib import Path
from datetime import datetime
import shutil
import argparse


def archive_files(data_folder: Path, archive_folder: Path, exclude_patterns: list):
    """Move processed files to archive folder."""
    
    print(f"\nArchiving processed files from {data_folder}...\n")
    
    # Create archive folder with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    archive_subfolder = archive_folder / f"archive_{timestamp}"
    archive_subfolder.mkdir(parents=True, exist_ok=True)
    
    # Find files to archive (exclude master and special files)
    files_to_archive = []
    for pattern in ['*.xlsx', '*.csv']:
        for filepath in data_folder.glob(pattern):
            # Skip if matches exclusion pattern
            skip = False
            for exclude in exclude_patterns:
                if exclude in filepath.name.lower():
                    skip = True
                    break
            
            if not skip and filepath.is_file():
                files_to_archive.append(filepath)
    
    if not files_to_archive:
        print("No files to archive.")
        return
    
    print(f"Found {len(files_to_archive)} files to archive:\n")
    
    # Move files
    archived_count = 0
    for filepath in files_to_archive:
        try:
            dest = archive_subfolder / filepath.name
            shutil.move(str(filepath), str(dest))
            print(f"  ✓ Archived: {filepath.name}")
            archived_count += 1
        except Exception as e:
            print(f"  ✗ Error moving {filepath.name}: {e}")
    
    print(f"\n{'='*60}")
    print(f"✓ Archived {archived_count} files to:")
    print(f"  {archive_subfolder}")
    print('='*60)
    
    print(f"\nRemaining in data folder:")
    remaining = list(data_folder.glob('*.xlsx')) + list(data_folder.glob('*.csv'))
    remaining = [f for f in remaining if f.is_file()]
    if remaining:
        for f in remaining:
            print(f"  - {f.name}")
    else:
        print("  (only master file and README)")


def main():
    parser = argparse.ArgumentParser(description='Archive processed Excel files')
    parser.add_argument('--data-folder', default='data', help='Data folder with files to archive')
    parser.add_argument('--archive-folder', default='data/archive', help='Archive destination')
    
    args = parser.parse_args()
    
    data_folder = Path(args.data_folder)
    archive_folder = Path(args.archive_folder)
    
    if not data_folder.exists():
        print(f"Data folder not found: {data_folder}")
        return
    
    # Files to exclude from archiving (keep in data folder)
    exclude_patterns = [
        'master_combined',  # The combined output
        'readme',           # Documentation
        '~$'               # Temp Excel files
    ]
    
    # Confirm before archiving
    print(f"This will move processed Excel/CSV files to archive folder.")
    print(f"Files containing these patterns will NOT be moved:")
    for pattern in exclude_patterns:
        print(f"  - {pattern}")
    
    response = input("\nProceed with archiving? (y/n): ").strip().lower()
    if response != 'y':
        print("Archive cancelled.")
        return
    
    archive_files(data_folder, archive_folder, exclude_patterns)


if __name__ == '__main__':
    main()
