# Process Controls Value Tracker — Business Laptop Setup Guide

**Purpose:** Get this project running on your MPC business laptop.

---

## Prerequisites

You mentioned you have:
- ✅ VSCode installed
- ✅ Python available
- ✅ pip install capability
- ✅ GitHub Copilot (local only)
- ✅ Jupyter capability (optional)

---

## Step 1: Choose Your Folder Location ✅ COMPLETE

**Your chosen location:**

```
C:\Users\GF99\Documentation\
└── PC_Value_Tracker\          ← This project (current location)
    ├── SETUP.md               ← This file
    ├── README.md
    ├── requirements.txt
    ├── config\
    │   ├── keywords.json
    │   └── settings.json
    ├── scripts\
    │   ├── enrich_entries.py
    │   └── export_to_excel.py
    ├── data\                  ← Your JSON data goes here
    │   └── work-history-entries.json
    ├── output\                ← Generated files appear here
    ├── submissions\           ← Submission tracking
    └── docs\
        ├── METHODOLOGY.md     ← Shareable with leadership
        ├── COPILOT_PROMPTS.md ← Shareable
        └── HANDOFF_INTERNAL.md ← PRIVATE - do not share
```

---

## Step 2: Transfer Files from USB ✅ COMPLETE

Files successfully transferred to `C:\Users\GF99\Documentation\PC_Value_Tracker\`

---

## Step 3: Set Up Python Environment ✅ COMPLETE

**Installed dependencies:**
- ✅ pandas (data manipulation)
- ✅ openpyxl (Excel file creation)
- ✅ matplotlib (charts, optional)
- ✅ seaborn (visualizations, optional)

Installation completed on: January 24, 2026

---

## Step 4: Understand the Persistent Database

**Your data is stored in a persistent master file:**

```
data\
├── master_combined_issues.xlsx  ← 💾 PERSISTENT DATABASE (never delete!)
├── master_combined.json         ← JSON version
└── (new Copilot exports here)   ← Drop new Excel files here
```

**How it works:**
1. **Master file is your database** - Contains ALL historical entries (currently 215 entries)
2. **Combine script loads master FIRST** - Preserves existing data
3. **New files are merged in** - Added to master, duplicates removed
4. **Safe to delete individual files** - After combining, data is in master forever

**This means:**
- ✅ Run Copilot prompt → Save to `data/` folder → Run combine script → Master updated
- ✅ Individual Excel files can be deleted after combining
- ✅ Your history is cumulative and never lost

---

## Step 5: Generate Excel Tracker ✅ COMPLETE

**Your PERSISTENT DATABASE workflow:**

```cmd
# 1. Combine new exports into persistent master (loads existing data first!)
python scripts\combine_excel_files.py --output data\master_combined_issues.xlsx

# 2. Convert master to JSON
python scripts\excel_to_json.py --input data\master_combined_issues.xlsx --output data\master_combined.json

# 3. Export to final tracker
python scripts\export_simple_tracker.py --input data\master_combined.json --output output\pc_value_tracker.xlsx

# 4. (Optional) Delete individual Excel files - data is safe in master!
Remove-Item data\*.xlsx -Exclude master_combined_issues.xlsx
```

**Results:** Excel workbook with 9 analysis sheets:
- All_Data (complete 215 entries from persistent database)
- Summary (statistics)
- By_System, By_Area, By_Year, By_Complexity
- High_Complexity, Cross_Site, Training (filtered views)

**Key behavior:**
- 💾 Master file preserves ALL historical data (cumulative)
- ✅ New Copilot exports are added without losing old entries
- ✅ Duplicates removed automatically
- ✅ Safe to delete individual Excel files after combining

---

## Step 6: Review and Refine

Open `output\pc_value_tracker.xlsx` and review:
- **Summary** - Key metrics
- **High_Complexity** - Major/Significant issues (23 entries)
- **Cross_Site** - Multi-site/Corporate work (24 entries)
- **Training** - Mentorship/Consulting (15 entries)
- **All_Data** - Complete dataset for filtering

Add manual notes, estimate time spent, flag items for leadership presentation.

---

## Step 7: Open in VSCode

1. Open VSCode
2. File → Open Folder → Select `pc-value-tracker`
3. You can now:
   - Edit scripts with Copilot assistance
   - Run Python files directly
   - View/edit Markdown docs

---

## Folder Permissions Note

Since you don't have admin access, make sure you're working in a folder you have write access to:
- ✅ `C:\Users\[YourUsername]\...` — You have access
- ❌ `C:\Program Files\...` — Requires admin

---

## Quick Command Reference

| Task | Command |
|------|---------|
| Install dependencies | `pip install -r requirements.txt` |
| **Combine into persistent DB** | `python scripts\combine_excel_files.py --output data\master_combined_issues.xlsx` |
| Convert to JSON | `python scripts\excel_to_json.py --input data\master_combined_issues.xlsx --output data\master_combined.json` |
| Export tracker | `python scripts\export_simple_tracker.py --input data\master_combined.json --output output\pc_value_tracker.xlsx` |
| **Delete individual files** | `Remove-Item data\*.xlsx -Exclude master_combined_issues.xlsx` |

**💾 Database Note:** The combine script now loads the existing master file FIRST, then adds new files. This means your historical data is NEVER lost - it's cumulative and persistent!

---

## Updating Keyword Mappings

To improve categorization, edit `config\keywords.json`:

1. Open in VSCode
2. Add keywords to relevant sections
3. Re-run enrichment script
4. Re-export to Excel

Example — adding AMP-related keywords:
```json
"amp_related": {
  "keywords": [
    "AMP",
    "console upgrade",
    "YOUR_NEW_KEYWORD_HERE"
  ]
}
```

---

## Using Copilot Prompts

1. Open `docs\COPILOT_PROMPTS.md`
2. Copy the prompt you want to use
3. Open Outlook or Teams Copilot
4. Paste and run
5. Review results and export to your tracker

---

## Troubleshooting

### "Python not found"
Make sure Python is in your PATH. Try:
```cmd
python --version
```
If not found, you may need to use the full path or add Python to PATH.

### "Module not found" errors
Run:
```cmd
pip install -r requirements.txt
```

### Permission denied errors
Make sure you're working in your user folder, not a system folder.

### JSON file not found
Check the path in your command matches where your data actually is.

---

## File Security Reminders

| File | Contains | Keep Private? |
|------|----------|---------------|
| `data\*.json` | Your extracted email data | ✅ Yes — company data |
| `output\*.xlsx` | Processed results | ⚠️ Review before sharing |
| `docs\HANDOFF_INTERNAL.md` | Personal notes, opinions | ✅ Yes — do not share |
| `docs\METHODOLOGY.md` | Professional methodology | ✅ Safe to share |
| `docs\COPILOT_PROMPTS.md` | Extraction prompts | ✅ Safe to share |

---

## Next Steps After Setup

1. ✅ Initial database created (215 entries in master_combined_issues.xlsx)
2. ✅ Review the Excel tracker (output/pc_value_tracker.xlsx)
3. ⬜ Run Copilot prompts weekly to extract new data (see docs/COPILOT_PROMPTS_QUICKSTART.md)
4. ⬜ Drop new exports in data/ folder, run combine script (data is cumulative!)
5. ⬜ Review high-complexity entries and add time estimates
6. ⬜ Extract leadership impact stories for promotion case

---

## Getting Help

### With Code (GitHub Copilot)
- Open a script in VSCode
- Copilot can help you modify/debug
- Ask it to explain what code does

### With Strategy (Claude/AI)
- Upload `docs\HANDOFF_INTERNAL.md` to a new chat
- AI will have full context to continue helping

---

*Setup guide created January 2026*
