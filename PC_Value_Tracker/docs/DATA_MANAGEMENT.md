# Data Management Guide

**Understanding the PC Value Tracker data persistence model.**

---

## Data Architecture

### The Permanent Database

**File**: `data/master.json`

- ✅ **Permanent source of truth** - Never deleted or overwritten
- ✅ **Append-only** - New records are added, existing records preserved
- ✅ **Survives raw file deletion** - Reports can be generated even if raw files are gone
- ⚠️ **Never edit manually** - Always use scripts to modify

### Source Files (Temporary)

**Location**: `data/raw/`

- 📥 Excel files exported from Copilot
- 🔄 Processed into master.json via aggregation script
- 📦 Can be archived or deleted after processing
- 💾 Optional to keep for audit trail

---

## Workflow

### 1. Add New Data

When you have new Excel exports from Copilot:

```powershell
# Place files in data/raw/
# Example: data/raw/LastMonth_2026-01-24_TChiu.xlsx

# RECOMMENDED: Aggregate and archive in one step
.\.venv\Scripts\python.exe scripts\collect\aggregate_raw_data.py --archive --verbose

# OR: Aggregate only (keep raw files)
.\.venv\Scripts\python.exe scripts\collect\aggregate_raw_data.py --verbose
```

**What happens with --archive:**
1. Loads existing 63 records from master.json
2. Reads new data from Excel files in data/raw/
3. Adds only NEW records (deduplicates)
4. Saves updated master.json with all records
5. **Moves processed files to data/archive/YYYY-MM/**

### 2. Archive Raw Files (Optional)

After successful aggregation:

```powershell
# Automatic archival (organizes by YYYY-MM)
.\.venv\Scripts\python.exe scripts\util\archive_raw_files.py --verbose

# Preview what would be archived (dry run)
.\.venv\Scripts\python.exe scripts\util\archive_raw_files.py --dry-run

# Or manually move files
mkdir data\archive\2026-01 -Force
Move-Item data\raw\*.xlsx data\archive\2026-01\

# Or delete them (data is safe in master.json)
Remove-Item data\raw\*.xlsx
```

**Why archive?**
- Keep audit trail of source files
- Reprocess if needed
- Attach to performance reviews

**Why delete?**
- Save disk space
- Keep workspace clean
- Data is already in master.json

### 3. Generate Reports

Reports are generated FROM master.json (not from raw files):

```powershell
# Monthly report
.\.venv\Scripts\python.exe scripts\report\generate_monthly_report.py --month 2026-01

# Quarterly report
.\.venv\Scripts\python.exe scripts\report\generate_quarterly_report.py --quarter 2026-Q1

# Quick overview
.\.venv\Scripts\python.exe scripts\util\show_summary.py
```

**Reports work even if raw files are deleted!**

---

## Data Safety Features

### Deduplication

Records are identified by: `(date, first 100 chars of summary)`

If you accidentally re-process the same Excel file:
- ✅ No duplicates created
- ✅ Existing records preserved
- ℹ️ Script reports "0 new records added"

### Preservation

The aggregation script:
- ✅ Always loads existing master.json first
- ✅ Appends new records to existing data
- ✅ Never overwrites or deletes existing records
- ✅ Works even if data/raw/ is empty

### Recovery

If you accidentally delete master.json:
1. Restore from backup (highly recommended!)
2. Or re-aggregate from archived raw files:
   ```powershell
   # Copy archived files back to raw/
   Copy-Item data\archive\*\*.xlsx data\raw\
   
   # Re-aggregate
   .\.venv\Scripts\python.exe scripts\collect\aggregate_raw_data.py --verbose
   ```

---

## Best Practices

### ✅ DO

- **Back up master.json regularly** (weekly or monthly)
- **Run aggregation before archiving** raw files
- **Verify record count** after aggregation (`show_summary.py`)
- **Archive by month** for organization: `data/archive/YYYY-MM/`
- **Use --verbose flag** to see what's happening

### ❌ DON'T

- **Don't edit master.json manually** - Use scripts
- **Don't delete master.json** - It's your only permanent database
- **Don't rely on raw files** - They're temporary source files
- **Don't worry about re-processing** - Deduplication prevents duplicates

---

## File Naming Conventions

### Raw Files (data/raw/)

**Format**: `[Description]_[Date]_[Name].xlsx`

Examples:
- `LastMonth_2026-01-24_TChiu.xlsx` (V2.0 format)
- `TonyChiu_2025_Sent_Support_Emails_inferred_impact.xlsx` (historical)

### Archive Structure (data/archive/)

**By Month**:
```
data/archive/
├── 2024-12/
│   └── LastMonth_2024-12-31_TChiu.xlsx
├── 2025-01/
│   └── LastMonth_2025-01-31_TChiu.xlsx
└── 2026-01/
    └── LastMonth_2026-01-24_TChiu.xlsx
```

---

## Backup Strategy

### Critical Backups

**master.json** - Back up before:
- Major updates
- End of month
- Performance review prep

**Backup locations**:
```powershell
# Local backup
Copy-Item data\master.json data\master_backup_2026-01-24.json

# Cloud backup (OneDrive, SharePoint, etc.)
Copy-Item data\master.json "C:\Users\[User]\OneDrive\PC_Value_Tracker_Backup\"
```

### Optional Backups

- Raw files (if keeping audit trail)
- Generated reports (can be regenerated)
- Config files (if customized)

---

## Troubleshooting

### "0 new records added" - Expected

This happens when:
- ✅ Files were already processed
- ✅ Deduplication working correctly
- ℹ️ No action needed

### "Keeping X existing records" - Good

This happens when:
- ✅ No raw files found
- ✅ master.json preserved correctly
- ℹ️ Reports still work

### "Error loading master.json" - Problem

This happens when:
- ⚠️ master.json is corrupted
- ⚠️ master.json was deleted
- 🔧 Restore from backup or re-aggregate from archived files

---

## Quick Reference

| Scenario | Command | Safe? |
|----------|---------|-------|
| Add new data | `aggregate_raw_data.py --verbose` | ✅ Yes |
| Archive raw files | `Move-Item data\raw\*.xlsx data\archive\YYYY-MM\` | ✅ Yes |
| Delete raw files | `Remove-Item data\raw\*.xlsx` | ✅ Yes (after aggregation) |
| Generate reports | `generate_monthly_report.py --month YYYY-MM` | ✅ Yes |
| Re-process files | Run aggregation again | ✅ Yes (no duplicates) |
| Delete master.json | **DON'T** | ❌ **NO** |

---

## See Also

- [QUICK_START.md](QUICK_START.md) - Getting started guide
- [METHODOLOGY.md](METHODOLOGY.md) - Full methodology
- [README.md](../README.md) - Project overview

---

*Last Updated: January 2026*
