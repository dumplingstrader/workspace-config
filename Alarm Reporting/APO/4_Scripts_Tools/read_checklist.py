import pandas as pd

file_path = 'C:/Users/GF99/Documentation/Alarm Reporting/APO/APO_Deployment_Workflow_Checklist.xlsx'

# Read all sheets
xl = pd.ExcelFile(file_path)
print("Sheet Names:", xl.sheet_names)
print("\n" + "="*80 + "\n")

# Read each sheet
for sheet in xl.sheet_names:
    if 'DELETE' in sheet:
        continue
    print(f"\n{'='*80}")
    print(f"SHEET: {sheet}")
    print('='*80)
    df = pd.read_excel(file_path, sheet_name=sheet)
    print(df.head(30).to_string())
    print(f"\nTotal rows: {len(df)}")
    print("\n")
