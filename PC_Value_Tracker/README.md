# PC Value Tracker V2.0

**Drive actionable change through targeted issue tracking.**

**Author:** Tony Chiu
**Version:** 2.0
**Updated:** January 2026

---

## What's Different in V2.0

| Before | After |
|--------|-------|
| 12+ fields per issue | 6 core fields |
| 7 different prompts | 1 unified prompt |
| "Prove we're busy" | "Demand specific changes" |
| Generic reports | Stream-specific scorecards |

---

## The Five Streams

| Stream | Focus | The Ask |
|--------|-------|---------|
| **Project** | Capital project handoff failures | Require PC acceptance gate |
| **Day-to-Day** | Routine support work | Resource planning data |
| **Legacy** | Obsolete equipment issues | Fund obsolescence backlog |
| **Diagnostic** | Work diagnosing non-PC issues | Restore troubleshooting capability |
| **After-Hours** | Off-hours calls and emergencies | Fair on-call compensation |

---

## Quick Start

### Step 1: Setup (One Time)

```powershell
.\setup_environment.ps1
```

### Step 2: Weekly Data Collection (10 min)

1. Open Copilot in Outlook
2. Copy prompt from `docs/COPILOT_PROMPT.md`
3. Review results, save to `data/raw/`

### Step 3: Aggregate Data

```powershell
# Aggregate and archive in one step (recommended)
python scripts/collect/aggregate_raw_data.py --archive --verbose
```

**Data Persistence**: This command preserves all existing data in `master.json` and only adds NEW records. With `--archive` flag, processed files are automatically moved to organized archive folders.

### Step 4: Generate Reports

```powershell
# Monthly summary
python scripts/report/generate_monthly_report.py --month 2026-01

# Quarterly summary
python scripts/report/generate_quarterly_report.py --quarter 2026-Q1

# Quick data overview
python scripts/util/show_summary.py
```

---

## Key Commands

| Command | Purpose |
|---------|---------|
| `python scripts/collect/aggregate_raw_data.py --verbose` | Add new data to master.json (preserves existing) || `python scripts/util/archive_raw_files.py --verbose` | Archive processed files to data/archive/YYYY-MM/ || `python scripts/report/generate_monthly_report.py --month YYYY-MM` | Monthly summary report |
| `python scripts/report/generate_quarterly_report.py --quarter YYYY-QN` | Quarterly summary with trends |
| `python scripts/util/show_summary.py` | Quick data overview |

---

## Folder Structure

```
PC_Value_Tracker/
├── data/
│   ├── master.json           # **PERMANENT DATABASE** - All tracked issues
│   ├── raw/                   # Excel source files (can be archived)
│   └── archive/               # Processed files (optional)
│
├── output/
│   ├── monthly/               # Monthly report spreadsheets
│   └── quarterly/             # Quarterly report spreadsheets
│
├── scripts/
│   ├── collect/               # Data collection
│   ├── report/                # Report generation
│   └── util/                  # Utilities
│
├── config/
│   ├── streams.json           # Stream definitions
│   └── settings.json          # Configuration
│
├── templates/
│   ├── quick_log.xlsx         # Tier 1 capture template
│   └── PC_Value_Template.xlsx
│
├── docs/                      # Documentation
│
└── archive/v1.0/              # Previous version (reference)
```

---

## Documentation

| Document | Purpose |
|----------|---------|
| `docs/METHODOLOGY.md` | Full V2.0 methodology |
| `docs/QUICK_START.md` | 5-minute getting started |
| `docs/STREAM_DEFINITIONS.md` | Detailed stream guide |
| `docs/COPILOT_PROMPT.md` | Unified extraction prompt |
| `docs/SUPERVISOR_BRIEFING.md` | Supervisor buy-in |
| `docs/DISTRIBUTION_GUIDE.md` | Creating zip packages |

---

## Current Data

- **215 entries** migrated from V1.0
- Date range: 2024-2026
- Stream distribution:
  - Day-to-Day: 176 (82%)
  - Project: 26 (12%)
  - Legacy: 6 (3%)
  - Diagnostic: 6 (3%)
  - After-Hours: 1 (<1%)

---

## Data Management Best Practices

| Practice | Details |
|----------|---------|-----|
| **Backup master.json** | Your permanent database - back up regularly |
| **Archive raw files** | After processing, move to `data/archive/YYYY-MM/` |
| **Reports are disposable** | Can be regenerated anytime from master.json |
| **Never edit master.json manually** | Always use aggregation script |

---

## Troubleshooting

### "Python not found"
Install Python from [python.org](https://www.python.org/downloads/) with "Add to PATH" checked.

### "Script cannot be loaded"
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### "Module not found"
```powershell
.\.venv\Scripts\activate
pip install -r requirements.txt
```

---

## Version History

### V2.0 (January 2026)
- Complete redesign: 5-stream model
- Simplified schema (6 core fields)
- Unified Copilot prompt
- Stream-specific scorecards
- Action-oriented outputs

### V1.0 (January 2026)
- Initial implementation
- Archived in `archive/v1.0/`

---

## Requirements

- Python 3.10+
- pandas, openpyxl

```bash
pip install -r requirements.txt
```

---

*V2.0 — Less tracking, more changing.*
