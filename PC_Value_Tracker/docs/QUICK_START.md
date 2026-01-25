# PC Value Tracker V2.1 — Quick Start

Get up and running in 5 minutes.

---

## What This Is

A tracking system that organizes Process Controls work into **six streams**, each with a specific audience and action.

| Stream | What It Tracks | The Ask |
|--------|----------------|---------|
| **Project** | Capital project handoff failures | Require PC acceptance gate |
| **Day-to-Day** | Routine support, unit support, troubleshooting | Resource planning |
| **Legacy Modernization** | Obsolete equipment issues | Fund obsolescence |
| **Diagnostic** | Work diagnosing non-PC issues | Restore Maintenance capability |
| **After-Hours** | Off-hours calls and emergencies | Fair on-call compensation |
| **Applications** | DynAMo, Integrity, Historian support | Recognize application expertise |

---

## Weekly Workflow (10 minutes)

### Step 1: Run the Copilot Prompt

1. Open Copilot in Outlook or Teams
2. Copy the prompt from `docs/COPILOT_PROMPT.md`
3. Paste and run

### Step 2: Review and Adjust

- Check that streams are correctly assigned
- Add any phone calls or walk-ups that weren't in email
- Adjust complexity if the estimate is off

### Step 3: Save

Save the Excel file to: `data/raw/Weekly_[YYYY-MM-DD]_[Name].xlsx`

---

## Monthly Workflow (15 minutes)

### Step 1: Aggregate Data

```bash
# Aggregate and archive in one step (recommended)
python scripts/collect/aggregate_raw_data.py --archive --verbose

# Or aggregate only (no archiving)
python scripts/collect/aggregate_raw_data.py --verbose
```

**Note**: This preserves all existing data in `master.json` and only adds NEW records from raw files.

### Step 2: Archive Processed Files (Optional - if not done above)

If you didn't use `--archive` flag:

```bash
# Automatic archival (organizes by YYYY-MM)
python scripts/util/archive_raw_files.py --verbose

# Or preview first (dry run)
python scripts/util/archive_raw_files.py --dry-run
```

**Important**: `master.json` is your permanent database. Raw files are just source files.

### Step 3: Generate Reports

```bash
# Monthly summary
python scripts/report/generate_monthly_report.py --month 2026-01

# Quarterly summary
python scripts/report/generate_quarterly_report.py --quarter 2026-Q1
```

### Step 4: Review

Open reports in `output/monthly/` or `output/quarterly/`

---

## Key Files

| File | Purpose |
|------|---------|
| `data/master.json` | **Permanent database** - All tracked issues (never deleted) |
| `data/raw/` | **Source files** - Excel exports (can be archived after processing) |
| `config/streams.json` | Stream definitions and keywords |
| `docs/COPILOT_PROMPT.md` | The unified extraction prompt |
| `docs/METHODOLOGY.md` | Full methodology explanation |

---

## Stream Quick Reference

**Project:** AMP, cutover, commissioning, contractor, MOC

**Day-to-Day:** Support request, troubleshooting, configuration, unit support

**Legacy Modernization:** PLC-5, SLC-500, TDC, obsolete, end-of-life

**Diagnostic:** "Not ours", handed off to Electrical/Mechanical

**After-Hours:** Weekend, evening, emergency, call-out

**Applications:** DynAMo, ACM, Integrity, PHD, PI, alarm rationalization

---

## Resolution Tracking

The system automatically infers resolution status from summary keywords:
- **Closed**: "fixed", "resolved", "completed", "confirmed"
- **Pending**: "pending", "waiting", "investigating"
- **Escalated**: "escalated", "vendor", "SR opened"
- **Handed Off**: "handed off", "transferred to"
- **Workaround**: "workaround", "temporary fix"

If resolution can't be inferred, it shows as **Unknown**.

---

## Need Help?

- Full methodology: `docs/METHODOLOGY.md`
- Stream details: `docs/STREAM_DEFINITIONS.md`
- Copilot tips: `docs/COPILOT_PROMPT.md`
- **Supervisor after-hours**: `docs/COPILOT_PROMPT_AFTER_HOURS.md`
- Data management: `docs/DATA_MANAGEMENT.md`

---

*V2.1 — Six streams, resolution tracking, actionable data.*
