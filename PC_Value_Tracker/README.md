# Process Controls Value Tracker

**Purpose:** Track and demonstrate the value of Process Controls team work through systematic issue documentation and analysis.

**Author:** Tony Chiu  
**Version:** 1.1  
**Date:** January 2026

---

## Quick Start (Solo Use)

1. **See [SETUP.md](SETUP.md)** for business laptop installation
2. **Extract data:** Run Copilot prompts in Outlook, save exports to `data\` folder
3. **Combine into persistent database:** `python scripts\combine_excel_files.py --output data\master_combined_issues.xlsx`
   - 💾 **Master file preserves all historical data** - loads existing entries first, then adds new files
   - ✅ **Safe to delete individual Excel files** after combining - data is permanently saved in master
4. **Convert to JSON:** `python scripts\excel_to_json.py --input data\master_combined_issues.xlsx --output data\master_combined.json`
5. **Export tracker:** `python scripts\export_simple_tracker.py --input data\master_combined.json --output output\pc_value_tracker.xlsx`
6. **Clean up (optional):** `Remove-Item data\*.xlsx -Exclude master_combined_issues.xlsx` - deletes individual files, keeps master database

---

## Team Rollout (Get Others Contributing)

### For Supervisors
1. Review **docs/SUPERVISOR_BRIEFING.md** — explains the pilot and asks for support
2. Share **docs/DATA_COLLECTION_PROCEDURE.md** — step-by-step guide for contributors
3. Distribute **templates/PC_Value_Template.xlsx** — standardized submission format

### For Contributors
1. Follow **docs/DATA_COLLECTION_PROCEDURE.md**
2. Run Copilot prompts weekly (10-15 min)
3. Submit Excel files to shared location

### For Aggregation
1. Collect submissions in `submissions/` folder
2. Run: `python scripts/aggregate_submissions.py --input submissions/ --output output/aggregated_data.xlsx`
3. Review aggregated report

---

## Folder Structure

```
pc-value-tracker\
├── SETUP.md                     ← Installation guide
├── README.md                    ← This file
├── requirements.txt             ← Python dependencies
│
├── config\
│   ├── keywords.json            ← Keyword mappings (customize)
│   └── settings.json            ← Path configuration
│
├── scripts\
│   ├── combine_excel_files.py   ← Combine Copilot exports
│   ├── excel_to_json.py         ← Convert Excel to JSON
│   ├── export_simple_tracker.py ← Generate Excel tracker
│   ├── archive_processed_files.py ← Clean up data folder
│   ├── create_template.py       ← Generate contributor template
│   ├── aggregate_submissions.py ← Combine team submissions
│   └── archive\                 ← Unused legacy scripts
│
├── templates\
│   └── PC_Value_Template.xlsx   ← Blank template for contributors
│
├── submissions\                 ← Team submissions go here
│   └── README.md
│
├── data\                        ← Your personal data
│   ├── master_combined_issues.xlsx  ← 💾 PERSISTENT DATABASE (never delete!)
│   ├── master_combined.json         ← JSON version of database
│   └── (new Copilot exports here)   ← Add new files, run combine script
│
├── output\                      ← Generated reports
│   └── (pc_value_tracker.xlsx, aggregated_data.xlsx)
│
└── docs\
    ├── METHODOLOGY.md           ← ✅ Share with leadership
    ├── COPILOT_PROMPTS.md       ← ✅ Share - data extraction prompts
    ├── DATA_COLLECTION_PROCEDURE.md  ← ✅ Share - contributor guide
    ├── SUPERVISOR_BRIEFING.md   ← ✅ Share - supervisor overview
    └── HANDOFF_INTERNAL.md      ← ❌ PRIVATE - AI context
```

---

## Document Guide

| Document | Audience | Purpose |
|----------|----------|---------|
| **METHODOLOGY.md** | Leadership, anyone | Professional methodology explanation |
| **SUPERVISOR_BRIEFING.md** | Supervisors | Request for support, pilot overview |
| **DATA_COLLECTION_PROCEDURE.md** | All contributors | How to extract and submit data |
| **COPILOT_PROMPTS.md** | All contributors | Ready-to-use extraction prompts |
| **HANDOFF_INTERNAL.md** | Tony only | AI continuation context (private) |

---

## Workflow Options

### Option 1: Solo Pilot
You track your own issues, generate reports, share with supervisor.

### Option 2: Team Pilot
Multiple engineers contribute, you aggregate, generate team reports.

### Option 3: Supervisor-Led
Supervisors run prompts on their own email, model participation for team.

---

## Requirements

- Python 3.8+
- pandas
- openpyxl

Install with: `pip install -r requirements.txt`

---

## Customization

**Data Analysis:**
- Use Excel filters on `All_Data` sheet to find patterns
- Add custom columns for manual categorization
- Create pivot tables for specific metrics

**Copilot Prompts:**
- Edit `docs/COPILOT_PROMPTS_LEAD_ENGINEER.md` to add new extraction queries
- Customize date ranges, keywords, and fields as needed

---

## Support

For AI-assisted continuation, upload `docs/HANDOFF_INTERNAL.md` to Claude or similar.
