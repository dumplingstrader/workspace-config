"""
Process Controls Value Tracker - Excel Export Script
=====================================================
Exports enriched entries to Excel for filtering, pivoting, and manual review.

Usage:
    python export_to_excel.py --input output/enriched_entries.json --output output/pc_value_tracker.xlsx

Author: Tony Chiu
Created: January 2026
"""

import json
import pandas as pd
from pathlib import Path
from datetime import datetime
import argparse


def load_json(filepath: str) -> dict:
    """Load JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def flatten_entry(entry: dict) -> dict:
    """Flatten a nested entry into a flat dictionary for Excel."""
    flat = {
        # Core fields
        'text': entry.get('text', ''),
        'source_file': entry.get('source_file', ''),
        'score': entry.get('score', 0),
        'date_found': entry.get('date_found', ''),
        
        # Enrichment flags
        'amp_related': entry.get('amp_related', False),
        'obsolete_equipment': entry.get('obsolete_equipment', False),
        
        # Root cause
        'root_cause_category': entry.get('root_cause', {}).get('category', 'unknown'),
        'root_cause_confidence': entry.get('root_cause', {}).get('confidence', 'none'),
        'root_cause_matches': ', '.join(entry.get('root_cause', {}).get('matches', [])),
        'root_cause_needs_review': entry.get('root_cause', {}).get('needs_review', True),
        
        # Business impact
        'business_impact': entry.get('business_impact', {}).get('primary_impact', 'unknown'),
        'business_impact_needs_review': entry.get('business_impact', {}).get('needs_review', True),
        
        # Systems
        'systems_involved': ', '.join(entry.get('systems_involved', [])),
        
        # Manual review fields (blank for user to fill)
        'manual_time_spent_hrs': entry.get('manual_review', {}).get('time_spent_hrs', ''),
        'manual_was_pc_job': entry.get('manual_review', {}).get('was_pc_job', ''),
        'manual_notes': entry.get('manual_review', {}).get('notes', ''),
        'manual_reviewed': entry.get('manual_review', {}).get('reviewed', False),
        
        # Original keyword matches
        'problem_keywords': ', '.join(entry.get('matched_keywords', {}).get('problem', [])),
        'solution_keywords': ', '.join(entry.get('matched_keywords', {}).get('solution', [])),
        'system_keywords': ', '.join(entry.get('matched_keywords', {}).get('system', [])),
    }
    
    return flat


def create_summary_sheet(df: pd.DataFrame) -> pd.DataFrame:
    """Create a summary statistics dataframe."""
    summary_data = []
    
    # Overall stats
    summary_data.append({'Metric': 'Total Entries', 'Value': len(df)})
    summary_data.append({'Metric': 'AMP-Related Entries', 'Value': df['amp_related'].sum()})
    summary_data.append({'Metric': 'Obsolete Equipment Entries', 'Value': df['obsolete_equipment'].sum()})
    summary_data.append({'Metric': 'Entries Needing Review', 'Value': df['root_cause_needs_review'].sum()})
    summary_data.append({'Metric': '', 'Value': ''})
    
    # Score breakdown
    summary_data.append({'Metric': '--- Score Distribution ---', 'Value': ''})
    summary_data.append({'Metric': 'Score 50+', 'Value': len(df[df['score'] >= 50])})
    summary_data.append({'Metric': 'Score 30-49', 'Value': len(df[(df['score'] >= 30) & (df['score'] < 50)])})
    summary_data.append({'Metric': 'Score 20-29', 'Value': len(df[(df['score'] >= 20) & (df['score'] < 30)])})
    summary_data.append({'Metric': '', 'Value': ''})
    
    # Root cause breakdown
    summary_data.append({'Metric': '--- Root Cause Categories ---', 'Value': ''})
    for cat, count in df['root_cause_category'].value_counts().items():
        summary_data.append({'Metric': f'  {cat}', 'Value': count})
    summary_data.append({'Metric': '', 'Value': ''})
    
    # Business impact breakdown
    summary_data.append({'Metric': '--- Business Impact ---', 'Value': ''})
    for impact, count in df['business_impact'].value_counts().items():
        summary_data.append({'Metric': f'  {impact}', 'Value': count})
    summary_data.append({'Metric': '', 'Value': ''})
    
    # Systems breakdown
    summary_data.append({'Metric': '--- Systems Involved ---', 'Value': ''})
    # Count systems (they're comma-separated)
    all_systems = df['systems_involved'].str.split(', ').explode()
    all_systems = all_systems[all_systems != '']
    for sys, count in all_systems.value_counts().items():
        summary_data.append({'Metric': f'  {sys}', 'Value': count})
    
    return pd.DataFrame(summary_data)


def create_review_sheet(df: pd.DataFrame, score_threshold: int = 30) -> pd.DataFrame:
    """Create a filtered sheet for high-priority manual review."""
    review_df = df[df['score'] >= score_threshold].copy()
    
    # Select and order columns for review
    review_columns = [
        'score',
        'text',
        'root_cause_category',
        'root_cause_confidence',
        'amp_related',
        'obsolete_equipment',
        'business_impact',
        'systems_involved',
        'manual_time_spent_hrs',
        'manual_was_pc_job',
        'manual_notes',
        'manual_reviewed',
        'source_file'
    ]
    
    return review_df[review_columns].sort_values('score', ascending=False)


def export_to_excel(enriched_data: dict, output_path: str) -> None:
    """Export enriched data to Excel workbook with multiple sheets."""
    
    # Flatten all entries
    entries = enriched_data.get('ideas', [])
    flat_entries = [flatten_entry(e) for e in entries]
    
    # Create main dataframe
    df = pd.DataFrame(flat_entries)
    
    # Sort by score descending
    df = df.sort_values('score', ascending=False)
    
    # Create Excel writer
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        
        # Sheet 1: Summary
        summary_df = create_summary_sheet(df)
        summary_df.to_excel(writer, sheet_name='Summary', index=False)
        
        # Sheet 2: High Priority Review (score 30+)
        review_df = create_review_sheet(df, score_threshold=30)
        review_df.to_excel(writer, sheet_name='Review_Priority', index=False)
        
        # Sheet 3: AMP Related
        amp_df = df[df['amp_related'] == True].copy()
        if len(amp_df) > 0:
            amp_df.to_excel(writer, sheet_name='AMP_Related', index=False)
        
        # Sheet 4: Obsolete Equipment
        obsolete_df = df[df['obsolete_equipment'] == True].copy()
        if len(obsolete_df) > 0:
            obsolete_df.to_excel(writer, sheet_name='Obsolete_Equipment', index=False)
        
        # Sheet 5: By System - Alarm
        alarm_df = df[df['systems_involved'].str.contains('alarm', case=False, na=False)].copy()
        if len(alarm_df) > 0:
            alarm_df.to_excel(writer, sheet_name='System_Alarm', index=False)
        
        # Sheet 6: By System - PLC/SIS
        plc_sis_df = df[df['systems_involved'].str.contains('plc|sis', case=False, na=False)].copy()
        if len(plc_sis_df) > 0:
            plc_sis_df.to_excel(writer, sheet_name='System_PLC_SIS', index=False)
        
        # Sheet 7: By System - HMI
        hmi_df = df[df['systems_involved'].str.contains('hmi', case=False, na=False)].copy()
        if len(hmi_df) > 0:
            hmi_df.to_excel(writer, sheet_name='System_HMI', index=False)
        
        # Sheet 8: All Data
        df.to_excel(writer, sheet_name='All_Data', index=False)
        
        # Adjust column widths for Summary sheet
        worksheet = writer.sheets['Summary']
        worksheet.column_dimensions['A'].width = 35
        worksheet.column_dimensions['B'].width = 15
        
        # Adjust column widths for Review sheet
        worksheet = writer.sheets['Review_Priority']
        worksheet.column_dimensions['A'].width = 8   # score
        worksheet.column_dimensions['B'].width = 80  # text
        worksheet.column_dimensions['C'].width = 20  # root_cause_category
    
    print(f"Excel workbook saved to: {output_path}")
    print(f"  - Summary: Overall statistics")
    print(f"  - Review_Priority: {len(review_df)} high-score entries for manual review")
    print(f"  - AMP_Related: {len(amp_df)} entries")
    print(f"  - Obsolete_Equipment: {len(obsolete_df)} entries")
    print(f"  - System_Alarm: {len(alarm_df)} entries")
    print(f"  - System_PLC_SIS: {len(plc_sis_df)} entries")
    print(f"  - System_HMI: {len(hmi_df)} entries")
    print(f"  - All_Data: {len(df)} total entries")


def main():
    parser = argparse.ArgumentParser(description='Export enriched entries to Excel')
    parser.add_argument('--input', '-i', required=True, help='Input enriched JSON file')
    parser.add_argument('--output', '-o', required=True, help='Output Excel file path')
    
    args = parser.parse_args()
    
    print(f"Loading enriched data from {args.input}...")
    data = load_json(args.input)
    
    print(f"Exporting to Excel...")
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    export_to_excel(data, args.output)
    
    print("\nDone!")


if __name__ == '__main__':
    main()
