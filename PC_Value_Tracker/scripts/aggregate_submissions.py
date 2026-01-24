"""
Process Controls Value Tracker - Aggregate Contributor Data
============================================================
Combines Excel submissions from multiple contributors into a single dataset.

Usage:
    python scripts/aggregate_submissions.py --input submissions/ --output output/aggregated_data.xlsx

Author: Tony Chiu
Created: January 2026
"""

import pandas as pd
from pathlib import Path
import argparse
from datetime import datetime
import os


def load_submission(filepath: str) -> tuple:
    """
    Load a contributor submission Excel file.
    Returns (metadata_dict, data_df) or (None, None) if invalid.
    """
    try:
        # Load metadata
        metadata_df = pd.read_excel(filepath, sheet_name='Submission_Info')
        metadata = dict(zip(metadata_df['Item'], metadata_df['Value']))
        
        # Load data
        data_df = pd.read_excel(filepath, sheet_name='Data_Entry')
        
        # Skip if no data
        if len(data_df) == 0:
            print(f"  Skipping {filepath} - no data entries")
            return None, None
        
        # Add contributor info to each row
        data_df['Contributor_Name'] = metadata.get('Contributor Name', 'Unknown')
        data_df['Contributor_Role'] = metadata.get('Role', 'Unknown')
        data_df['Submission_Date'] = metadata.get('Submission Date', '')
        data_df['Source_File'] = os.path.basename(filepath)
        
        print(f"  Loaded {filepath}: {len(data_df)} entries from {metadata.get('Contributor Name', 'Unknown')}")
        return metadata, data_df
        
    except Exception as e:
        print(f"  Error loading {filepath}: {e}")
        return None, None


def aggregate_submissions(input_dir: str, output_path: str) -> None:
    """
    Aggregate all Excel submissions from a directory.
    """
    input_path = Path(input_dir)
    
    # Find all Excel files
    excel_files = list(input_path.glob('*.xlsx')) + list(input_path.glob('*.xls'))
    
    if not excel_files:
        print(f"No Excel files found in {input_dir}")
        return
    
    print(f"Found {len(excel_files)} Excel files in {input_dir}")
    
    # Load all submissions
    all_data = []
    all_metadata = []
    
    for filepath in excel_files:
        metadata, data_df = load_submission(str(filepath))
        if data_df is not None:
            all_data.append(data_df)
            all_metadata.append(metadata)
    
    if not all_data:
        print("No valid submissions found")
        return
    
    # Combine all data
    combined_df = pd.concat(all_data, ignore_index=True)
    
    # Create summary statistics
    summary_data = []
    summary_data.append({'Metric': 'Aggregation Date', 'Value': datetime.now().strftime('%Y-%m-%d %H:%M')})
    summary_data.append({'Metric': 'Total Submissions', 'Value': len(all_data)})
    summary_data.append({'Metric': 'Total Entries', 'Value': len(combined_df)})
    summary_data.append({'Metric': '', 'Value': ''})
    
    # Entries by contributor
    summary_data.append({'Metric': '--- By Contributor ---', 'Value': ''})
    for name, count in combined_df['Contributor_Name'].value_counts().items():
        summary_data.append({'Metric': f'  {name}', 'Value': count})
    summary_data.append({'Metric': '', 'Value': ''})
    
    # Entries by system
    if 'System' in combined_df.columns:
        summary_data.append({'Metric': '--- By System ---', 'Value': ''})
        for system, count in combined_df['System'].value_counts().items():
            summary_data.append({'Metric': f'  {system}', 'Value': count})
        summary_data.append({'Metric': '', 'Value': ''})
    
    # Entries by root cause
    if 'Root_Cause_Category' in combined_df.columns:
        summary_data.append({'Metric': '--- By Root Cause ---', 'Value': ''})
        for cause, count in combined_df['Root_Cause_Category'].value_counts().items():
            summary_data.append({'Metric': f'  {cause}', 'Value': count})
        summary_data.append({'Metric': '', 'Value': ''})
    
    # AMP-related
    if 'AMP_Related' in combined_df.columns:
        amp_yes = len(combined_df[combined_df['AMP_Related'].str.lower() == 'yes'])
        summary_data.append({'Metric': 'AMP-Related Issues', 'Value': amp_yes})
    
    # Was PC Job
    if 'Was_PC_Job' in combined_df.columns:
        summary_data.append({'Metric': '--- Was PC Responsibility ---', 'Value': ''})
        for val, count in combined_df['Was_PC_Job'].value_counts().items():
            summary_data.append({'Metric': f'  {val}', 'Value': count})
        summary_data.append({'Metric': '', 'Value': ''})
    
    # Total hours
    if 'Time_Spent_Hrs' in combined_df.columns:
        total_hours = combined_df['Time_Spent_Hrs'].sum()
        summary_data.append({'Metric': 'Total Hours Tracked', 'Value': f'{total_hours:.1f}'})
    
    summary_df = pd.DataFrame(summary_data)
    
    # Create contributor summary
    contributor_summary = []
    for metadata in all_metadata:
        contributor_summary.append({
            'Name': metadata.get('Contributor Name', 'Unknown'),
            'Role': metadata.get('Role', 'Unknown'),
            'Date_Range_Start': metadata.get('Date Range Start', ''),
            'Date_Range_End': metadata.get('Date Range End', ''),
            'Submission_Date': metadata.get('Submission Date', ''),
        })
    contributor_df = pd.DataFrame(contributor_summary)
    
    # Write output
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        # Summary first
        summary_df.to_excel(writer, sheet_name='Summary', index=False)
        
        # Contributors
        contributor_df.to_excel(writer, sheet_name='Contributors', index=False)
        
        # All data
        combined_df.to_excel(writer, sheet_name='All_Data', index=False)
        
        # By System (pivot-ready)
        if 'System' in combined_df.columns:
            system_summary = combined_df.groupby('System').agg({
                'Date': 'count',
                'Time_Spent_Hrs': 'sum'
            }).rename(columns={'Date': 'Issue_Count', 'Time_Spent_Hrs': 'Total_Hours'})
            system_summary.to_excel(writer, sheet_name='By_System')
        
        # By Root Cause
        if 'Root_Cause_Category' in combined_df.columns:
            cause_summary = combined_df.groupby('Root_Cause_Category').agg({
                'Date': 'count',
                'Time_Spent_Hrs': 'sum'
            }).rename(columns={'Date': 'Issue_Count', 'Time_Spent_Hrs': 'Total_Hours'})
            cause_summary.to_excel(writer, sheet_name='By_Root_Cause')
        
        # By Contributor
        if 'Contributor_Name' in combined_df.columns:
            contrib_summary = combined_df.groupby('Contributor_Name').agg({
                'Date': 'count',
                'Time_Spent_Hrs': 'sum'
            }).rename(columns={'Date': 'Issue_Count', 'Time_Spent_Hrs': 'Total_Hours'})
            contrib_summary.to_excel(writer, sheet_name='By_Contributor')
        
        # AMP-Related only
        if 'AMP_Related' in combined_df.columns:
            amp_df = combined_df[combined_df['AMP_Related'].str.lower() == 'yes']
            if len(amp_df) > 0:
                amp_df.to_excel(writer, sheet_name='AMP_Related', index=False)
        
        # Not PC Job (handed off)
        if 'Was_PC_Job' in combined_df.columns:
            not_pc_df = combined_df[combined_df['Was_PC_Job'].str.lower() == 'no']
            if len(not_pc_df) > 0:
                not_pc_df.to_excel(writer, sheet_name='Not_PC_Job', index=False)
        
        # Adjust column widths for Summary
        worksheet = writer.sheets['Summary']
        worksheet.column_dimensions['A'].width = 30
        worksheet.column_dimensions['B'].width = 15
    
    print(f"\nAggregated data saved to: {output_path}")
    print(f"  - {len(all_data)} submissions combined")
    print(f"  - {len(combined_df)} total entries")
    if 'Time_Spent_Hrs' in combined_df.columns:
        print(f"  - {combined_df['Time_Spent_Hrs'].sum():.1f} total hours tracked")


def main():
    parser = argparse.ArgumentParser(description='Aggregate contributor submissions')
    parser.add_argument('--input', '-i', required=True, help='Input directory with Excel submissions')
    parser.add_argument('--output', '-o', default='output/aggregated_data.xlsx', help='Output aggregated file')
    
    args = parser.parse_args()
    
    aggregate_submissions(args.input, args.output)


if __name__ == '__main__':
    main()
