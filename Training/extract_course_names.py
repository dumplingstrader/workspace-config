import pandas as pd
import glob
import re

files = sorted(glob.glob('Training/BC-LAR-ENGPRO*.xlsx'))

for f in files:
    try:
        xl = pd.ExcelFile(f)
        sheets = xl.sheet_names
        sheet = 'View Learning Content Enrollmen' if 'View Learning Content Enrollmen' in sheets else 'View Learning Content Assignmen'
        df = pd.read_excel(f, sheet_name=sheet)
        col = 'Enrollment' if 'Enrollment' in df.columns else 'Learner'
        
        if len(df) > 0:
            sample = df[col].iloc[0]
            # Extract course name from enrollment string
            # Format: "Name - LAR 8901C Course Name (BC_LAR_ENGPRO001)"
            match = re.search(r'- (.*?) \(BC_LAR', sample)
            if match:
                course_name = match.group(1)
            else:
                course_name = sample
            
            file_name = f.split('\\')[-1]
            print(f'{file_name}: {course_name}')
    except Exception as e:
        print(f'{f}: Error - {e}')
