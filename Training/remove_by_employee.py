import openpyxl

wb = openpyxl.load_workbook('Training/Training_Attendance_Tracker.xlsx')
if 'By Employee' in wb.sheetnames:
    wb.remove(wb['By Employee'])
    wb.save('Training/Training_Attendance_Tracker.xlsx')
    print('Removed By Employee sheet')
else:
    print('By Employee sheet not found')
