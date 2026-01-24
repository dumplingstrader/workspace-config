# Submissions Folder

Place contributor Excel submissions here.

## Naming Convention

Files should be named: `PC_Value_[Name]_[YYYYMMDD].xlsx`

Examples:
- `PC_Value_JSmith_20260124.xlsx`
- `PC_Value_Area1_20260131.xlsx`

## Aggregating Submissions

Run:
```cmd
python scripts/aggregate_submissions.py --input submissions/ --output output/aggregated_data.xlsx
```

This will combine all Excel files in this folder into a single aggregated report.
