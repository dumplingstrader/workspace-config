import openpyxl
from pathlib import Path

TRACKER_PATH = Path("Training") / "Training_Attendance_Tracker.xlsx"

if not TRACKER_PATH.exists():
    print(f"Tracker file not found: {TRACKER_PATH}")
else:
    wb = openpyxl.load_workbook(TRACKER_PATH)
    if 'By Employee' in wb.sheetnames:
        wb.remove(wb['By Employee'])
        wb.save(TRACKER_PATH)
        print('Removed By Employee sheet')
    else:
        print('By Employee sheet not found')
