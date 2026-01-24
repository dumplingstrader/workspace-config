"""
Process Controls Value Tracker - Create Contributor Template
=============================================================
Creates a blank Excel template for supervisors/team members to submit their data.

Usage:
    python scripts/create_template.py --output templates/PC_Value_Template.xlsx

Author: Tony Chiu
Created: January 2026
"""

import pandas as pd
from pathlib import Path
import argparse
from datetime import datetime


def create_contributor_template(output_path: str) -> None:
    """Create a standardized Excel template for data collection."""
    
    # Define columns with descriptions
    columns = [
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
    
    # Create empty dataframe with columns
    df = pd.DataFrame(columns=columns)
    
    # Create instructions dataframe
    instructions_data = [
        {'Field': 'Date', 'Description': 'Date the issue was reported (YYYY-MM-DD)', 'Example': '2026-01-24', 'Required': 'Yes'},
        {'Field': 'Requester', 'Description': 'Person who requested help', 'Example': 'John Smith', 'Required': 'Yes'},
        {'Field': 'Requester_Dept', 'Description': 'Department of requester', 'Example': 'Operations, Projects, Maintenance', 'Required': 'Yes'},
        {'Field': 'System', 'Description': 'System/platform involved', 'Example': 'Experion, PLC, SIS, HMI, Alarms, Network', 'Required': 'Yes'},
        {'Field': 'Area_Unit', 'Description': 'Refinery area or unit', 'Example': 'FCC, Coker, Utilities, Plantwide', 'Required': 'Yes'},
        {'Field': 'Issue_Summary', 'Description': 'Brief description of the problem', 'Example': 'Graphics loading slowly on console 4', 'Required': 'Yes'},
        {'Field': 'Root_Cause_Category', 'Description': 'Category of root cause', 'Example': 'PC Issue, Project Delivery, Vendor, Obsolete Equipment, Training Gap, Not PC', 'Required': 'Yes'},
        {'Field': 'AMP_Related', 'Description': 'Was this related to AMP project?', 'Example': 'Yes, No', 'Required': 'Yes'},
        {'Field': 'Resolution', 'Description': 'How was it resolved?', 'Example': 'Fixed, Handed Off, Escalated, Workaround, Pending', 'Required': 'Yes'},
        {'Field': 'Time_Spent_Hrs', 'Description': 'Hours spent on this issue', 'Example': '2.5', 'Required': 'Yes'},
        {'Field': 'Was_PC_Job', 'Description': 'Was this legitimately PC responsibility?', 'Example': 'Yes, No, Partial', 'Required': 'Yes'},
        {'Field': 'Handed_Off_To', 'Description': 'If not PC, who was it handed to?', 'Example': 'Electrical, Mechanical, IT, Projects', 'Required': 'If handed off'},
        {'Field': 'Business_Impact', 'Description': 'What was the impact?', 'Example': 'Production, Safety, Compliance, Efficiency, Low/None', 'Required': 'No'},
        {'Field': 'Notes', 'Description': 'Any additional context', 'Example': 'Recurring issue, flagged at FAT', 'Required': 'No'},
    ]
    instructions_df = pd.DataFrame(instructions_data)
    
    # Create dropdown values dataframe
    dropdowns_data = [
        {'Field': 'System', 'Valid_Values': 'Experion, TDC, PLC, SIS, HMI, Alarms, Network, APC, Server, Other'},
        {'Field': 'Root_Cause_Category', 'Valid_Values': 'PC Issue, Project Delivery, Vendor Issue, Obsolete Equipment, Training Gap, Mechanical/Electrical, Network/Infrastructure, Other'},
        {'Field': 'AMP_Related', 'Valid_Values': 'Yes, No'},
        {'Field': 'Resolution', 'Valid_Values': 'Fixed, Handed Off, Escalated, Workaround, Pending, In Progress'},
        {'Field': 'Was_PC_Job', 'Valid_Values': 'Yes, No, Partial'},
        {'Field': 'Business_Impact', 'Valid_Values': 'Production, Safety, Compliance, Efficiency, Low/None'},
        {'Field': 'Requester_Dept', 'Valid_Values': 'Operations, Projects, Maintenance, Engineering, IT, Safety, Other'},
    ]
    dropdowns_df = pd.DataFrame(dropdowns_data)
    
    # Create example data
    example_data = [
        {
            'Date': '2026-01-20',
            'Requester': 'Operator Console',
            'Requester_Dept': 'Operations',
            'System': 'HMI',
            'Area_Unit': 'FCC',
            'Issue_Summary': 'Graphics loading slowly, 30+ seconds to refresh',
            'Root_Cause_Category': 'Project Delivery',
            'AMP_Related': 'Yes',
            'Resolution': 'Workaround',
            'Time_Spent_Hrs': 3,
            'Was_PC_Job': 'Partial',
            'Handed_Off_To': '',
            'Business_Impact': 'Efficiency',
            'Notes': 'AMP graphics overloaded, flagged during FAT'
        },
        {
            'Date': '2026-01-21',
            'Requester': 'John Smith',
            'Requester_Dept': 'Maintenance',
            'System': 'PLC',
            'Area_Unit': 'Utilities',
            'Issue_Summary': 'PLC-5 communication fault, intermittent',
            'Root_Cause_Category': 'Obsolete Equipment',
            'AMP_Related': 'No',
            'Resolution': 'Fixed',
            'Time_Spent_Hrs': 4.5,
            'Was_PC_Job': 'Yes',
            'Handed_Off_To': '',
            'Business_Impact': 'Production',
            'Notes': '35-year old PLC-5, recommended replacement'
        },
        {
            'Date': '2026-01-22',
            'Requester': 'Project Engineer',
            'Requester_Dept': 'Projects',
            'System': 'Alarms',
            'Area_Unit': 'Coker',
            'Issue_Summary': 'New alarms not appearing in DynAMo',
            'Root_Cause_Category': 'Training Gap',
            'AMP_Related': 'No',
            'Resolution': 'Fixed',
            'Time_Spent_Hrs': 1,
            'Was_PC_Job': 'Partial',
            'Handed_Off_To': '',
            'Business_Impact': 'Low/None',
            'Notes': 'Showed them the configuration process'
        },
        {
            'Date': '2026-01-23',
            'Requester': 'Control Room',
            'Requester_Dept': 'Operations',
            'System': 'Other',
            'Area_Unit': 'FCC',
            'Issue_Summary': 'Transmitter reading erratic',
            'Root_Cause_Category': 'Mechanical/Electrical',
            'AMP_Related': 'No',
            'Resolution': 'Handed Off',
            'Time_Spent_Hrs': 0.5,
            'Was_PC_Job': 'No',
            'Handed_Off_To': 'Maintenance',
            'Business_Impact': 'Production',
            'Notes': 'Diagnosed as instrument issue, not controls'
        },
    ]
    example_df = pd.DataFrame(example_data)
    
    # Create metadata
    metadata_data = [
        {'Item': 'Contributor Name', 'Value': '[Enter your name]'},
        {'Item': 'Role', 'Value': '[Area PCE / Specialist / Supervisor / etc.]'},
        {'Item': 'Date Range Start', 'Value': '[Start date of data]'},
        {'Item': 'Date Range End', 'Value': '[End date of data]'},
        {'Item': 'Submission Date', 'Value': datetime.now().strftime('%Y-%m-%d')},
        {'Item': 'Notes', 'Value': '[Any notes about this submission]'},
    ]
    metadata_df = pd.DataFrame(metadata_data)
    
    # Write to Excel with multiple sheets
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        # Metadata sheet first
        metadata_df.to_excel(writer, sheet_name='Submission_Info', index=False)
        
        # Data entry sheet
        df.to_excel(writer, sheet_name='Data_Entry', index=False)
        
        # Examples sheet
        example_df.to_excel(writer, sheet_name='Examples', index=False)
        
        # Instructions sheet
        instructions_df.to_excel(writer, sheet_name='Field_Descriptions', index=False)
        
        # Valid values sheet
        dropdowns_df.to_excel(writer, sheet_name='Valid_Values', index=False)
        
        # Adjust column widths
        for sheet_name in writer.sheets:
            worksheet = writer.sheets[sheet_name]
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width
    
    print(f"Template created: {output_path}")
    print(f"Sheets:")
    print(f"  - Submission_Info: Fill in your name and date range")
    print(f"  - Data_Entry: Enter your issue data here")
    print(f"  - Examples: Sample entries to guide you")
    print(f"  - Field_Descriptions: What each field means")
    print(f"  - Valid_Values: Allowed values for dropdowns")


def main():
    parser = argparse.ArgumentParser(description='Create contributor data template')
    parser.add_argument('--output', '-o', default='templates/PC_Value_Template.xlsx', 
                        help='Output template file path')
    
    args = parser.parse_args()
    
    # Create output directory if needed
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    
    create_contributor_template(args.output)


if __name__ == '__main__':
    main()
