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

## Reporting and Analysis

### Monthly Reports

Generate standardized monthly summaries with metrics and issue breakdowns:

```bash
python scripts/generate_monthly_report.py --input data/master_combined.json --month 2026-01 --output output/monthly_report_2026-01.xlsx
```

**Output includes:**
- Summary sheet with key metrics (total issues, by system, by area, by complexity)
- Complete issue list for the month
- System breakdown showing workload distribution
- High complexity issues requiring detailed attention

**When to use:** End of each month for documentation, quarterly reviews, annual performance review prep

---

### Quarterly Insights

Generate strategic trend analysis and improvement recommendations:

```bash
python scripts/generate_quarterly_insights.py --input data/master_combined.json --quarter 2026-Q1 --output output/quarterly_insights_2026-Q1.xlsx
```

**Output includes:**
- Executive summary of key findings
- Monthly trends (volume trajectory)
- Recurring issues (systemic problem identification)
- Training needs (knowledge gap detection)
- Equipment reliability concerns (high-burden systems)

**When to use:** End of quarter for strategic planning, budget justification, leadership presentations

---

### Report Templates

Pre-formatted templates for custom presentations:

**Generate templates** (one-time):
```bash
python scripts/create_monthly_report_template.py
python scripts/create_leadership_presentation_template.py
```

**Excel Template** (`templates/Monthly_Report_Template.xlsx`):
- Executive summary with metric placeholders
- Issue detail table
- System breakdown with chart area
- Action items and recommendations
- Notes section for observations

**PowerPoint Template** (`templates/Leadership_Presentation_Template.pptx`):
- 7-slide professional deck (teal and coral design)
- Title, executive summary, metrics dashboard, system breakdown, success stories, recommendations, Q&A
- All placeholders marked with [brackets]

**How to use:**
1. Run automated scripts to get raw metrics
2. Copy key numbers into template placeholders
3. Add narrative context and success stories
4. Insert charts and customize for audience

---

### Complete Reporting Workflow

**Monthly Cycle:**
```bash
# 1. Weekly data capture (Copilot prompts)
# 2. Combine into master database
python scripts/combine_excel_files.py

# 3. Convert to JSON
python scripts/excel_to_json.py

# 4. Generate monthly report
python scripts/generate_monthly_report.py --month 2026-01

# 5. (Optional) Update Excel template with custom narrative
```

**Quarterly Cycle:**
```bash
# 1. Generate insights report
python scripts/generate_quarterly_insights.py --quarter 2026-Q1

# 2. Create leadership presentation from template
#    - Copy metrics from insights report
#    - Add success stories and recommendations
#    - Insert charts from Excel

# 3. Present to leadership or use for annual review
```

**Report Examples** (based on 215 entries):
- Average 25 issues per month
- DCS systems: 45% of workload
- High complexity: 10.7% (23 major/significant issues)
- Cross-site activities: 11% (24 issues)

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
│   ├── generate_monthly_report.py      ← ✨ NEW: Monthly summary reports
│   ├── generate_quarterly_insights.py  ← ✨ NEW: Quarterly trend analysis
│   ├── create_monthly_report_template.py     ← ✨ NEW: Excel template generator
│   ├── create_leadership_presentation_template.py  ← ✨ NEW: PowerPoint template generator
│   ├── archive_processed_files.py ← Clean up data folder
│   ├── create_template.py       ← Generate contributor template
│   ├── aggregate_submissions.py ← Combine team submissions
│   └── archive\                 ← Unused legacy scripts
│
├── templates\
│   ├── Monthly_Report_Template.xlsx  ← ✨ NEW: Pre-formatted Excel report
│   ├── Leadership_Presentation_Template.pptx  ← ✨ NEW: PowerPoint deck
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
│   ├── pc_value_tracker.xlsx        ← 9-sheet analysis workbook
│   ├── monthly_report_YYYY-MM.xlsx  ← ✨ NEW: Monthly summaries
│   ├── quarterly_insights_YYYY-QN.xlsx  ← ✨ NEW: Quarterly trends
│   └── aggregated_data.xlsx     ← Team rollout aggregation
│
└── docs\
    ├── METHODOLOGY.md           ← ✅ Share with leadership (UPDATED with reporting details)
    ├── COPILOT_PROMPTS.md       ← ✅ Share - data extraction prompts
    ├── COPILOT_PROMPTS_QUICKSTART.md  ← ✅ Share - 5-min weekly guide
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
