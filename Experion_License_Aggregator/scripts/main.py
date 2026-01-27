"""
Main Entry Point for Experion License Aggregator
Orchestrates XML parsing, database operations, cost calculations, and Excel generation.
"""

import argparse
import json
from pathlib import Path
from datetime import datetime
import sys

from xml_parser import parse_all_licenses
from database import LicenseDatabase
from cost_calculator import CostCalculator
from excel_generator import ExcelReportGenerator


def load_config(config_path: str = '../config/settings.json') -> dict:
    """Load configuration from JSON file."""
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Config file not found: {config_path}")
        print("Using default configuration...")
        return {
            'clusters': ['Carson', 'Wilmington'],
            'exclude_folders': ['Emerson', 'EXELE', 'GE', 'MAXUM', 'Hot Spare'],
            'thresholds': {
                'license_age_warning_days': 730,
                'excess_points_absolute': 500,
                'excess_points_percent': 25,
                'placeholder_cost': 100.00
            }
        }


def main():
    """Main execution function."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Experion License Aggregator - Parse XML licenses and generate Excel report'
    )
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Show detailed progress')
    parser.add_argument('-i', '--input-dir', default='../data/raw',
                       help='Input directory for XML files (default: ../data/raw)')
    parser.add_argument('-o', '--output-dir', default='../data/output',
                       help='Output directory for Excel files (default: ../data/output)')
    parser.add_argument('-c', '--clusters', nargs='+',
                       help='Process specific clusters only (e.g., Carson Wilmington)')
    parser.add_argument('--diff', action='store_true',
                       help='Show changes since last run')
    parser.add_argument('--no-history', action='store_true',
                       help='Skip saving to database')
    parser.add_argument('--config', default='../config/settings.json',
                       help='Custom config file path')
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Override clusters if specified
    clusters = args.clusters if args.clusters else config['clusters']
    exclude_folders = config['exclude_folders']
    thresholds = config['thresholds']
    
    print("=" * 60)
    print("EXPERION LICENSE AGGREGATOR v2.0")
    print("=" * 60)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Clusters: {', '.join(clusters)}")
    print(f"Input directory: {args.input_dir}")
    print(f"Output directory: {args.output_dir}")
    print()
    
    # Step 1: Parse XML files
    print("[1/5] Parsing XML license files...")
    data_dir = Path(args.input_dir)
    if not data_dir.exists():
        print(f"Error: Input directory not found: {data_dir}")
        sys.exit(1)
    
    licenses, errors = parse_all_licenses(data_dir, clusters, exclude_folders)
    
    if not licenses:
        print("Error: No license files found!")
        print("Ensure XML files are in: data/raw/{Cluster}/{SystemFolder}/")
        sys.exit(1)
    
    print(f"✓ Parsed {len(licenses)} systems")
    if errors and args.verbose:
        print(f"  Warnings: {len(errors)} files could not be parsed")
    print()
    
    # Step 2: Calculate costs
    print("[2/5] Calculating costs...")
    cost_calc = CostCalculator(
        catalog_path='../config/cost_catalog.json',
        placeholder_cost=thresholds['placeholder_cost']
    )
    
    cost_summary = cost_calc.calculate_all_systems(licenses)
    
    # Add costs back to license data for Excel
    for lic, sys_cost in zip(licenses, cost_summary['system_costs']):
        lic['_estimated_cost'] = sys_cost['total_cost']
    
    print(f"✓ Total estimated cost: ${cost_summary['grand_total']:,.2f}")
    print()
    
    # Step 3: Database operations (change detection)
    changes = []
    if not args.no_history:
        print("[3/5] Checking for changes...")
        run_date = datetime.now().strftime('%Y-%m-%d')
        
        with LicenseDatabase() as db:
            # Get previous snapshot
            previous = db.get_previous_snapshot(run_date)
            
            if previous and args.diff:
                changes = db.detect_changes(licenses, previous)
                print(f"✓ Detected {len(changes)} changes from previous run")
                if args.verbose and changes:
                    for change in changes[:5]:  # Show first 5
                        print(f"  - {change['msid']}: {change['field']} "
                              f"{change.get('old_value')} → {change.get('new_value')}")
            else:
                print("✓ First run - establishing baseline")
            
            # Save current snapshot
            db.save_snapshot(run_date, licenses)
            
            # Purge old data
            db.purge_old_data(days_to_keep=1095)  # 3 years
        print()
    else:
        print("[3/5] Skipping database operations (--no-history)")
        print()
    
    # Step 4: Identify transfer candidates
    print("[4/5] Identifying transfer candidates...")
    candidates = cost_calc.identify_transfer_candidates(
        licenses,
        excess_points_absolute=thresholds['excess_points_absolute'],
        excess_points_percent=thresholds['excess_points_percent']
    )
    print(f"✓ Found {len(candidates)} potential transfer candidates")
    print()
    
    # Step 5: Generate Excel report
    print("[5/5] Generating Excel report...")
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = output_dir / f'Experion_License_Report_{timestamp}.xlsx'
    
    generator = ExcelReportGenerator(system_names_file='../config/system_names.json')
    
    # Add action items to summary
    action_items = []
    if errors:
        action_items.append(f"Review {len(errors)} files with parsing errors")
    if changes:
        action_items.append(f"Review {len(changes)} changed license parameters")
    if candidates:
        action_items.append(f"Evaluate {len(candidates)} systems for license transfers")
    
    # Check for stale licenses
    stale_count = sum(1 for lic in licenses 
                     if lic.get('license_date') and 
                     (datetime.now() - datetime.strptime(lic['license_date'], '%Y-%m-%d')).days > 730)
    if stale_count:
        action_items.append(f"Update {stale_count} stale licenses (>2 years old)")
    
    action_items.append("Collect actual usage data (utilization_input.csv)")
    
    cost_summary['action_items'] = action_items
    
    # Create sheets
    generator.create_executive_summary(cost_summary)
    generator.create_pks_sheet(licenses, changes)
    generator.create_summary_sheet(cost_summary)
    generator.create_transfer_candidates_sheet(candidates)
    if changes:
        generator.create_changes_sheet(changes)
    if errors:
        generator.create_errors_sheet(errors)
    
    generator.save(str(output_file))
    print()
    
    # Summary
    print("=" * 60)
    print("COMPLETED")
    print("=" * 60)
    print(f"Systems processed: {len(licenses)}")
    print(f"Total cost: ${cost_summary['grand_total']:,.2f}")
    print(f"Transfer candidates: {len(candidates)}")
    if changes:
        print(f"Changes detected: {len(changes)}")
    print(f"\nReport: {output_file}")
    print("=" * 60)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nError: {e}")
        if '--verbose' in sys.argv or '-v' in sys.argv:
            import traceback
            traceback.print_exc()
        sys.exit(1)
