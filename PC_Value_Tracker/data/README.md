# Data Folder

This folder contains the master database and Copilot export files.

**DO NOT share this folder** — it contains company data.

## Primary Files

- `master_combined_issues.xlsx` — Master database (Excel format)
- `master_combined.json` — Master database (JSON format for scripts)

## Copilot Export Files

Place new Copilot exports here before running `combine_excel_files.py`:
- `*_Tech_Assistance_*.xlsx`
- `*_Categorized_*.xlsx`
- Other Copilot export formats

## Archive Folder

Processed files are moved to `archive/` after being combined into the master database.

## Workflow

1. Export data from Outlook using prompts in `docs/COPILOT_PROMPTS.md`
2. Save Excel files to this folder
3. Run `python scripts/combine_excel_files.py` to merge into master
4. Run `python scripts/excel_to_json.py` to update JSON for reporting scripts
