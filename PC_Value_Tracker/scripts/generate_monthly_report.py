"""
Process Controls Value Tracker - Monthly Report Generator
==========================================================
Generates monthly summary report from master database with metrics,
charts, and analysis for leadership review.

Usage:
    python scripts/generate_monthly_report.py --input data/master_combined.json --output output/monthly_report_YYYY-MM.xlsx --month 2026-01

Author: Tony Chiu
Created: January 2026
"""

import pandas as pd
import json
from pathlib import Path
import argparse
from datetime import datetime
import calendar


def load_data(json_path: Path) -> pd.DataFrame:
    """Load master database from JSON."""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    df = pd.DataFrame(data.get('entries', []))
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    return df


def filter_by_month(df: pd.DataFrame, year: int, month: int) -> pd.DataFrame:
    """Filter data to specific month."""
    return df[(df['Date'].dt.year == year) & (df['Date'].dt.month == month)]


def calculate_metrics(df: pd.DataFrame) -> dict:
    """Calculate key metrics for the month."""
    
    metrics = {
        'total_issues': len(df),
        'by_system': df['System'].value_counts().to_dict() if 'System' in df.columns else {},
        'by_area': df['Area_Unit'].value_counts().to_dict() if 'Area_Unit' in df.columns else {},
        'by_complexity': df['Complexity'].value_counts().to_dict() if 'Complexity' in df.columns else {},
        'by_requester_dept': df['Requester_Dept'].value_counts().to_dict() if 'Requester_Dept' in df.columns else {},
        'by_resolution': df['Resolution'].value_counts().to_dict() if 'Resolution' in df.columns else {},
    }
    
    return metrics


def create_summary_sheet(df: pd.DataFrame, metrics: dict, month_name: str) -> pd.DataFrame:
    """Create summary statistics sheet."""
    
    summary_data = [
        ['Report Period', month_name],
        ['Total Issues Handled', metrics['total_issues']],
        ['', ''],
        ['TOP SYSTEMS', ''],
    ]
    
    # Top 5 systems
    for system, count in sorted(metrics['by_system'].items(), key=lambda x: x[1], reverse=True)[:5]:
        summary_data.append([f'  {system}', count])
    
    summary_data.append(['', ''])
    summary_data.append(['TOP AREAS', ''])
    
    # Top 5 areas
    for area, count in sorted(metrics['by_area'].items(), key=lambda x: x[1], reverse=True)[:5]:
        summary_data.append([f'  {area}', count])
    
    summary_data.append(['', ''])
    summary_data.append(['COMPLEXITY BREAKDOWN', ''])
    
    # Complexity
    for complexity, count in sorted(metrics['by_complexity'].items(), key=lambda x: x[1], reverse=True):
        summary_data.append([f'  {complexity}', count])
    
    summary_data.append(['', ''])
    summary_data.append(['REQUESTING DEPARTMENTS', ''])
    
    # Departments
    for dept, count in sorted(metrics['by_requester_dept'].items(), key=lambda x: x[1], reverse=True)[:5]:
        summary_data.append([f'  {dept}', count])
    
    return pd.DataFrame(summary_data, columns=['Metric', 'Value'])


def create_detail_sheet(df: pd.DataFrame) -> pd.DataFrame:
    """Create detailed issue list."""
    
    columns_to_include = [
        'Date', 'Subject', 'Requester', 'Requester_Dept', 'System',
        'Area_Unit', 'Issue_Summary', 'Resolution', 'Complexity'
    ]
    
    # Only include columns that exist
    available_columns = [col for col in columns_to_include if col in df.columns]
    
    detail_df = df[available_columns].copy()
    detail_df = detail_df.sort_values('Date', ascending=False)
    
    return detail_df


def create_system_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    """Create system-level breakdown."""
    
    if 'System' not in df.columns:
        return pd.DataFrame()
    
    system_summary = df.groupby('System').agg({
        'Subject': 'count',
        'Complexity': lambda x: x.value_counts().to_dict() if len(x) > 0 else {}
    }).rename(columns={'Subject': 'Count'})
    
    system_summary = system_summary.sort_values('Count', ascending=False)
    
    return system_summary


def main():
    parser = argparse.ArgumentParser(description='Generate monthly report from master database')
    parser.add_argument('--input', default='data/master_combined.json', help='Master JSON database')
    parser.add_argument('--output', '-o', help='Output Excel file (e.g., output/monthly_report_2026-01.xlsx)')
    parser.add_argument('--month', required=True, help='Month in YYYY-MM format (e.g., 2026-01)')
    
    args = parser.parse_args()
    
    # Parse month
    try:
        year, month = map(int, args.month.split('-'))
        month_name = f"{calendar.month_name[month]} {year}"
    except:
        print(f"❌ Invalid month format. Use YYYY-MM (e.g., 2026-01)")
        return
    
    # Default output filename if not provided
    if not args.output:
        args.output = f'output/monthly_report_{args.month}.xlsx'
    
    input_path = Path(args.input)
    output_path = Path(args.output)
    
    if not input_path.exists():
        print(f"❌ Input file not found: {input_path}")
        return
    
    print("\n" + "="*60)
    print(f"Monthly Report Generator - {month_name}")
    print("="*60)
    
    # Load data
    print(f"\n📊 Loading database: {input_path.name}")
    df = load_data(input_path)
    print(f"  ✓ Loaded {len(df)} total entries")
    
    # Filter to month
    df_month = filter_by_month(df, year, month)
    print(f"  ✓ Filtered to {len(df_month)} entries for {month_name}")
    
    if len(df_month) == 0:
        print(f"\n⚠️ No data found for {month_name}")
        return
    
    # Calculate metrics
    print(f"\n📈 Calculating metrics...")
    metrics = calculate_metrics(df_month)
    
    print(f"  ✓ Total issues: {metrics['total_issues']}")
    print(f"  ✓ Systems tracked: {len(metrics['by_system'])}")
    print(f"  ✓ Areas tracked: {len(metrics['by_area'])}")
    
    # Create report
    print(f"\n📝 Generating report sheets...")
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        # Summary sheet
        summary_df = create_summary_sheet(df_month, metrics, month_name)
        summary_df.to_excel(writer, sheet_name='Summary', index=False, header=False)
        print(f"  ✓ Created Summary sheet")
        
        # Detail sheet
        detail_df = create_detail_sheet(df_month)
        detail_df.to_excel(writer, sheet_name='All_Issues', index=False)
        print(f"  ✓ Created All_Issues sheet ({len(detail_df)} entries)")
        
        # System breakdown
        system_df = create_system_breakdown(df_month)
        if not system_df.empty:
            system_df.to_excel(writer, sheet_name='By_System')
            print(f"  ✓ Created By_System sheet")
        
        # High complexity items
        if 'Complexity' in df_month.columns:
            high_complexity = df_month[df_month['Complexity'].isin(['Major', 'Significant'])]
            if len(high_complexity) > 0:
                high_complexity_df = create_detail_sheet(high_complexity)
                high_complexity_df.to_excel(writer, sheet_name='High_Complexity', index=False)
                print(f"  ✓ Created High_Complexity sheet ({len(high_complexity)} entries)")
        
        # Format Summary sheet
        worksheet = writer.sheets['Summary']
        worksheet.column_dimensions['A'].width = 40
        worksheet.column_dimensions['B'].width = 20
        
        # Format All_Issues sheet
        worksheet = writer.sheets['All_Issues']
        worksheet.column_dimensions['A'].width = 12  # Date
        worksheet.column_dimensions['B'].width = 50  # Subject
        worksheet.column_dimensions['C'].width = 20  # Requester
        worksheet.column_dimensions['D'].width = 20  # Dept
        worksheet.column_dimensions['E'].width = 20  # System
        worksheet.column_dimensions['F'].width = 20  # Area
        worksheet.column_dimensions['G'].width = 60  # Issue Summary
        worksheet.column_dimensions['H'].width = 30  # Resolution
        worksheet.column_dimensions['I'].width = 15  # Complexity
    
    print(f"\n{'='*60}")
    print(f"✓ Report saved: {output_path}")
    print('='*60)
    
    print(f"\n📊 Quick Stats for {month_name}:")
    print(f"  • Total Issues: {metrics['total_issues']}")
    if metrics['by_system']:
        top_system = max(metrics['by_system'].items(), key=lambda x: x[1])
        print(f"  • Top System: {top_system[0]} ({top_system[1]} issues)")
    if metrics['by_complexity']:
        print(f"  • Complexity Breakdown:")
        for comp, count in sorted(metrics['by_complexity'].items(), key=lambda x: x[1], reverse=True):
            print(f"    - {comp}: {count}")


if __name__ == '__main__':
    main()
