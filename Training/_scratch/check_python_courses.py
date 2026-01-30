import pandas as pd

df = pd.read_excel('Training/Training_Attendance_Tracker.xlsx', sheet_name='Employee-Course Matrix')
python_cols = [col for col in df.columns if 'Python' in col]

print('Python course columns found:', python_cols)
print(f'\nNumber of Python columns: {len(python_cols)}')

if python_cols:
    for col in python_cols:
        print(f'\n{col}:')
        non_empty = df[col][df[col] != ''].count()
        print(f'  Employees with this course: {non_empty}')

# Check master data to see all Python enrollments
df_master = pd.read_excel('Training/Training_Attendance_Tracker.xlsx', sheet_name='Master Data')
python_courses = df_master[df_master['Training Course'].str.contains('Python', na=False)]
print(f'\nTotal Python enrollments in Master Data: {len(python_courses)}')
print('\nUnique Python course names:')
print(python_courses['Training Course'].unique())
