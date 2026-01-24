"""
Process Controls Value Tracker - Convert Copilot Output to Template
===================================================================
Converts raw Copilot table output (pasted from Outlook/Teams) into the 
standardized PC_Value_Template format.

Usage:
    python scripts/convert_copilot_output.py --input copilot_raw.txt --output output/converted_data.xlsx

Or interactively:
    python scripts/convert_copilot_output.py --interactive

Author: Tony Chiu
Created: January 2026
"""

import pandas as pd
from pathlib import Path
import argparse
import re
from datetime import datetime
from io import StringIO


def parse_markdown_table(text: str) -> pd.DataFrame:
    """
    Parse a markdown-style table (from Copilot output) into a DataFrame.
    Handles various table formats Copilot might produce.
    """
    lines = text.strip().split('\n')
    
    # Find table lines (contain |)
    table_lines = [l for l in lines if '|' in l]
    
    if not table_lines:
        raise ValueError("No table found in input. Make sure to copy the full Copilot table output.")
    
    # Remove separator lines (like |---|---|---|)
    table_lines = [l for l in table_lines if not re.match(r'^[\s|:-]+$', l)]
    
    # Parse header
    header_line = table_lines[0]
    headers = [h.strip() for h in header_line.split('|') if h.strip()]
    
    # Parse data rows
    data = []
    for line in table_lines[1:]:
        values = [v.strip() for v in line.split('|') if v.strip() or line.count('|') > len(headers)]
        # Handle empty cells
        if len(values) < len(headers):
            values.extend([''] * (len(headers) - len(values)))
        elif len(values) > len(headers):
            values = values[:len(headers)]
        data.append(values)
    
    df = pd.DataFrame(data, columns=headers)
    return df


def map_to_template_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Map various Copilot output column names to standard template columns.
    """
    # Common column name mappings
    column_mappings = {
        # Date variations
        'date': 'Date',
        'email_date': 'Date',
        'sent_date': 'Date',
        
        # Requester variations
        'requester': 'Requester',
        'from': 'Requester',
        'requested_by': 'Requester',
        'who': 'Requester',
        
        # Department variations
        'requester_dept': 'Requester_Dept',
        'department': 'Requester_Dept',
        'dept': 'Requester_Dept',
        
        # System variations
        'system': 'System',
        'platform': 'System',
        'system/equipment': 'System',
        'system_equipment': 'System',
        
        # Area variations
        'area_unit': 'Area_Unit',
        'area': 'Area_Unit',
        'unit': 'Area_Unit',
        'location': 'Area_Unit',
        
        # Issue variations
        'issue_summary': 'Issue_Summary',
        'issue': 'Issue_Summary',
        'summary': 'Issue_Summary',
        'description': 'Issue_Summary',
        'problem': 'Issue_Summary',
        
        # Resolution variations
        'resolution': 'Resolution',
        'status': 'Resolution',
        'outcome': 'Resolution',
        
        # Time variations
        'time_spent': 'Time_Spent_Hrs',
        'time_estimate': 'Time_Spent_Hrs',
        'time': 'Time_Spent_Hrs',
        'hours': 'Time_Spent_Hrs',
        'complexity': 'Time_Spent_Hrs',  # Will need conversion
        
        # Role variations
        'my_role': 'Notes',
        'role': 'Notes',
    }
    
    # Normalize column names (lowercase, replace spaces)
    df.columns = [c.lower().replace(' ', '_').replace('/', '_') for c in df.columns]
    
    # Apply mappings
    rename_dict = {}
    for old_name, new_name in column_mappings.items():
        if old_name in df.columns:
            rename_dict[old_name] = new_name
    
    df = df.rename(columns=rename_dict)
    
    return df


def convert_complexity_to_hours(value: str) -> float:
    """
    Convert complexity descriptions to estimated hours.
    """
    value_lower = str(value).lower()
    
    if 'quick' in value_lower or '< 1' in value_lower or '<1' in value_lower:
        return 0.5
    elif 'moderate' in value_lower or '1-4' in value_lower:
        return 2.5
    elif 'significant' in value_lower or '4-8' in value_lower:
        return 6.0
    elif 'major' in value_lower or '8+' in value_lower or 'multi' in value_lower:
        return 12.0
    elif 'ongoing' in value_lower:
        return 16.0
    else:
        # Try to parse as number
        try:
            return float(re.search(r'[\d.]+', value).group())
        except:
            return None


def add_template_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add any missing template columns with empty values.
    """
    template_columns = [
        'Date',
        'Requester',
        'Requester_Dept',
        'System',
        'Area_Unit',
        'Issue_Summary',
        'Root_Cause_Category',
        'AMP_Related',
        'Resolution',
        'Time_Spent_Hrs',
        'Was_PC_Job',
        'Handed_Off_To',
        'Business_Impact',
        'Notes'
    ]
    
    for col in template_columns:
        if col not in df.columns:
            df[col] = ''
    
    # Reorder to match template
    existing_cols = [c for c in template_columns if c in df.columns]
    extra_cols = [c for c in df.columns if c not in template_columns]
    
    # Put extra columns in Notes if they have useful info
    if extra_cols:
        for col in extra_cols:
            if df[col].notna().any() and col not in ['subject']:
                # Append to Notes
                df['Notes'] = df.apply(
                    lambda row: f"{row['Notes']}; {col}: {row[col]}" if pd.notna(row[col]) and str(row[col]).strip() else row['Notes'],
                    axis=1
                )
    
    return df[template_columns]


def convert_copilot_to_template(input_text: str) -> pd.DataFrame:
    """
    Full conversion pipeline from raw Copilot output to template format.
    """
    # Parse the markdown table
    df = parse_markdown_table(input_text)
    
    # Map columns to template names
    df = map_to_template_columns(df)
    
    # Convert complexity to hours if present
    if 'Time_Spent_Hrs' in df.columns:
        df['Time_Spent_Hrs'] = df['Time_Spent_Hrs'].apply(convert_complexity_to_hours)
    
    # Add missing template columns
    df = add_template_columns(df)
    
    # Clean up Notes column
    df['Notes'] = df['Notes'].str.strip('; ')
    
    return df


def interactive_mode():
    """
    Interactive mode - paste Copilot output directly.
    """
    print("="*60)
    print("Copilot Output Converter - Interactive Mode")
    print("="*60)
    print("\nPaste your Copilot table output below.")
    print("When done, enter a blank line followed by 'END' on its own line.\n")
    
    lines = []
    while True:
        try:
            line = input()
            if line.strip().upper() == 'END':
                break
            lines.append(line)
        except EOFError:
            break
    
    input_text = '\n'.join(lines)
    
    if not input_text.strip():
        print("No input received.")
        return
    
    try:
        df = convert_copilot_to_template(input_text)
        
        print(f"\nSuccessfully converted {len(df)} rows.")
        print("\nPreview (first 5 rows):")
        print(df.head().to_string())
        
        # Ask for output file
        output_path = input("\nEnter output Excel filename (or press Enter for 'converted_data.xlsx'): ").strip()
        if not output_path:
            output_path = 'converted_data.xlsx'
        if not output_path.endswith('.xlsx'):
            output_path += '.xlsx'
        
        # Save
        df.to_excel(output_path, index=False, sheet_name='Data_Entry')
        print(f"\nSaved to: {output_path}")
        
    except Exception as e:
        print(f"\nError converting data: {e}")
        print("Make sure you copied a complete Copilot table with headers.")


def main():
    parser = argparse.ArgumentParser(description='Convert Copilot table output to template format')
    parser.add_argument('--input', '-i', help='Input text file with Copilot output')
    parser.add_argument('--output', '-o', default='output/converted_data.xlsx', help='Output Excel file')
    parser.add_argument('--interactive', action='store_true', help='Interactive paste mode')
    
    args = parser.parse_args()
    
    if args.interactive:
        interactive_mode()
        return
    
    if not args.input:
        print("Either --input or --interactive is required")
        print("Usage:")
        print("  python convert_copilot_output.py --input copilot_raw.txt --output converted.xlsx")
        print("  python convert_copilot_output.py --interactive")
        return
    
    # Read input file
    with open(args.input, 'r', encoding='utf-8') as f:
        input_text = f.read()
    
    # Convert
    df = convert_copilot_to_template(input_text)
    
    # Save
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    df.to_excel(args.output, index=False, sheet_name='Data_Entry')
    
    print(f"Converted {len(df)} rows")
    print(f"Saved to: {args.output}")


if __name__ == '__main__':
    main()
