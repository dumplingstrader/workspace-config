import pandas as pd
import json

file_path = r'c:\Users\GF99\Documentation\SAP\15.-Assets-Hiearchy.xlsx'

# Read Excel file
xl = pd.ExcelFile(file_path)
sheet_names = xl.sheet_names

print("=" * 80)
print("EXCEL FILE ANALYSIS: 15.-Assets-Hiearchy.xlsx")
print("=" * 80)
print(f"\n1. SHEET NAMES ({len(sheet_names)} sheets):")
for i, sheet in enumerate(sheet_names, 1):
    print(f"   {i}. {sheet}")

print("\n" + "=" * 80)

# Analyze each sheet
for sheet in sheet_names:
    df = pd.read_excel(file_path, sheet_name=sheet)
    
    print(f"\n2. SHEET: '{sheet}'")
    print(f"   Total Rows: {len(df)}")
    print(f"\n   Column Headers ({len(df.columns)} columns):")
    for i, col in enumerate(df.columns, 1):
        print(f"      {i}. {col}")
    
    # Look for control system related columns
    print("\n   Analyzing control systems...")
    
    # Check all columns for control system keywords
    control_system_cols = [col for col in df.columns if any(keyword in str(col).lower() 
                          for keyword in ['control', 'system', 'type', 'dcs', 'plc', 'sis', 'category', 'description'])]
    
    if control_system_cols:
        print(f"\n   Found {len(control_system_cols)} relevant columns:")
        for col in control_system_cols:
            print(f"\n   Column: '{col}'")
            value_counts = df[col].value_counts()
            print(f"   Unique values: {len(value_counts)}")
            print("   Value counts:")
            for val, count in value_counts.items():
                print(f"      - {val}: {count}")
    
    # Also check for any column that might contain system types
    print("\n   Checking all columns for control system types (DCS, PLC, SIS, etc.)...")
    system_types = {'DCS': 0, 'PLC': 0, 'SIS': 0, 'SCADA': 0, 'BMS': 0, 'FGS': 0, 'ESD': 0}
    
    for col in df.columns:
        col_data = df[col].astype(str)
        for sys_type in system_types.keys():
            # Count occurrences in this column
            count = col_data.str.contains(sys_type, case=False, na=False).sum()
            if count > 0:
                system_types[sys_type] += count
                print(f"   Found {count} occurrences of '{sys_type}' in column '{col}'")
    
    print("\n   SUMMARY - Control System Types Found:")
    total_systems = sum(system_types.values())
    if total_systems > 0:
        for sys_type, count in system_types.items():
            if count > 0:
                print(f"      {sys_type}: {count}")
        print(f"      Total: {total_systems}")
    else:
        print("      No specific control system types found in this sheet")
    
    # Show sample data
    print(f"\n   Sample data (first 5 rows):")
    print(df.head(5).to_string())
    
    print("\n" + "=" * 80)
