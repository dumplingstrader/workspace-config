# Experion License Aggregator - Refinery Deployment Guide

This guide is for Controls Engineers and IT staff at Marathon Petroleum refineries who want to deploy the Experion License Aggregator at their site.

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Getting Started](#getting-started)
4. [Gathering Your License Files](#gathering-your-license-files)
5. [Configuring for Your Site](#configuring-for-your-site)
6. [Running the Tool](#running-the-tool)
7. [Understanding the Output](#understanding-the-output)
8. [Recommended Workflow](#recommended-workflow)
9. [Sharing Results](#sharing-results)
10. [Maintenance](#maintenance)
11. [FAQ](#faq)

---

## Overview

### What This Tool Does

The Experion License Aggregator consolidates Honeywell Experion PKS licensing data from XML files into a single Excel report. It helps you:

- **See all licenses in one place** - No more opening individual XML files
- **Track changes over time** - Know when licenses were modified
- **Estimate costs** - Budget for license renewals and expansions
- **Find optimization opportunities** - Identify systems with excess capacity
- **Flag issues** - Stale licenses, incorrect customer names

### Who Should Use This

- **Controls Engineers** - Primary users for license visibility
- **Controls Managers** - Review summary and action items
- **Finance/Procurement** - Cost estimates for budgeting
- **IT** - Initial setup and maintenance

---

## Prerequisites

### What You Need

| Requirement | Details |
|-------------|---------|
| **Windows PC** | Windows 10 or later |
| **Experion License Files** | XML files from your Experion systems |
| **Network Access** | To copy license files from Experion servers (if applicable) |
| **Excel** | To view output (Excel 2016 or later recommended) |

### What You DON'T Need

- Python installation (the EXE is standalone)
- Database software (SQLite is embedded)
- Administrator privileges (runs in user space)

---

## Getting Started

### Step 1: Get the Distribution Package

Download the latest distribution ZIP from your internal SharePoint/Teams site:
- `Experion_License_Aggregator_v2.0_YYYYMMDD.zip`

### Step 2: Extract to a Local Folder

Extract the ZIP to a location you can write to:
- Recommended: `C:\Tools\Experion_License_Aggregator\`
- Avoid: Network drives (database performance), Program Files (permissions)

### Step 3: Verify Folder Structure

After extraction, you should see:

```
Experion_License_Aggregator/
├── experion-license-tool.exe
├── QUICK_START.txt
├── README.md
├── config/
│   ├── settings.json
│   ├── cost_catalog.json
│   └── system_names.json
├── data/
│   ├── raw/
│   │   ├── Carson/        <- Will rename for your site
│   │   └── Wilmington/    <- Will rename for your site
│   └── output/
└── templates/
```

---

## Gathering Your License Files

### Where to Find License Files

Experion license XML files are typically located on your Experion servers:

| Location | Path |
|----------|------|
| **Experion Server** | `C:\Honeywell\Experion PKS\Server\License\` |
| **Engineering Station** | `C:\Honeywell\Experion PKS\Engineering\License\` |
| **Backup Location** | Check with your Controls team for backup procedures |

### License File Format

License files follow this naming pattern:
```
{MSID}_Experion_{Product}_R{Release}X_x_{SystemNumber}_{Version}.xml
```

**Example:** `M0614_Experion_PKS_R52X_x_60806_40.xml`
- MSID: M0614
- Product: PKS
- Release: 520.x
- System Number: 60806
- Version: 40 (the tool picks the highest version)

### Organizing Your Files

Create a folder structure that matches your site organization:

```
data/raw/
├── {YourSiteName}/           <- e.g., "Galveston" or "Detroit"
│   ├── {SystemName} {MSID} {Number}/
│   │   └── {license_file}.xml
│   ├── HCU M12345 54321/
│   │   └── M12345_Experion_PKS_R52X_x_54321_15.xml
│   └── FCC M12346 54322/
│       └── M12346_Experion_PKS_R52X_x_54322_8.xml
```

**Folder naming convention:** `{FriendlyName} {MSID} {SystemNumber}`
- This helps you identify systems at a glance
- The tool extracts the MSID and System Number from the XML, not the folder name

### Copying Files from Experion Servers

**Option A: Manual Copy**
1. Log into each Experion server
2. Navigate to the license folder
3. Copy the XML file(s) to a USB drive or network share
4. Organize into the folder structure above

**Option B: Scripted Collection (Advanced)**
If you have many systems, create a PowerShell script:
```powershell
# Example - customize for your environment
$servers = @("ESVT0-SRV1", "HCU-SRV1", "FCC-SRV1")
$destBase = "C:\Tools\Experion_License_Aggregator\data\raw\Galveston"

foreach ($server in $servers) {
    $src = "\\$server\c$\Honeywell\Experion PKS\Server\License\*.xml"
    $dest = "$destBase\$server"
    New-Item -ItemType Directory -Path $dest -Force
    Copy-Item $src $dest -Force
}
```

---

## Configuring for Your Site

### Step 1: Update Cluster Names

Edit `config/settings.json` and replace the default clusters with your site:

**Before (default):**
```json
{
  "clusters": ["Carson", "Wilmington"],
  ...
}
```

**After (your site):**
```json
{
  "clusters": ["Galveston"],
  ...
}
```

**Multiple clusters example (if you have separate areas):**
```json
{
  "clusters": ["Galveston-North", "Galveston-South"],
  ...
}
```

Then rename the folders in `data/raw/` to match.

### Step 2: Configure System Names

Edit `config/system_names.json` to add friendly names for your systems:

```json
{
  "Galveston|M12345|54321": "HCU",
  "Galveston|M12346|54322": "FCC",
  "Galveston|M12347|54323": "Coker",
  "Galveston|M12348|54324": "Utilities"
}
```

**Key format:** `{Cluster}|{MSID}|{SystemNumber}`

**Finding MSID and System Number:**
- Open any license XML file
- Look for: `<detail name="msid" value="M12345" />`
- And: `<detail name="number" value="54321" />`

### Step 3: Update Customer Name Patterns

If your licenses should show a specific customer name, update the validation:

```json
{
  ...
  "valid_customer_patterns": ["Marathon", "MPC", "Your Company Name"],
  ...
}
```

Licenses with customer names not matching these patterns will be flagged orange.

### Step 4: Configure Cost Catalog (Optional)

Edit `config/cost_catalog.json` with your actual Honeywell pricing:

```json
{
  "PROCESSPOINTS": {
    "unit_cost": 45.00,
    "per": 50,
    "category": "Points",
    "description": "Process I/O points",
    "is_placeholder": false
  },
  ...
}
```

**Notes:**
- Set `is_placeholder: true` for estimated costs
- Set `is_placeholder: false` for confirmed PO pricing
- Cost formula: `(quantity / per) * unit_cost`
- Example: 500 process points = (500 / 50) * $45 = $450

### Step 5: Adjust Thresholds (Optional)

In `config/settings.json`, you can customize alert thresholds:

```json
{
  ...
  "thresholds": {
    "license_age_warning_days": 730,    // Flag licenses older than 2 years
    "excess_points_absolute": 500,       // Minimum excess to flag
    "excess_points_percent": 25,         // Or 25% above average
    "placeholder_cost": 100.00           // Default cost for unknown items
  },
  ...
}
```

---

## Running the Tool

### First Run

1. Double-click `experion-license-tool.exe`
2. A console window will open showing progress
3. Wait for "Complete" message
4. Check `data/output/` for the Excel file

**First run output:**
```
Experion License Aggregator v2.0
================================
Scanning Galveston...
  Found 12 license files
Processing licenses...
  Processed 12 systems
Writing Excel output...
  Created: License_Comparison_20260126.xlsx
Saving to database...
  Baseline snapshot created (no previous data for comparison)
Complete!
```

### Subsequent Runs

On later runs, the tool compares to the previous snapshot:

```
Experion License Aggregator v2.0
================================
...
Detecting changes...
  2 changes detected since last run
Complete!
```

### Command Line Options

Run from Command Prompt or PowerShell for additional options:

```powershell
# Show verbose progress
.\experion-license-tool.exe --verbose

# Show changes since last run
.\experion-license-tool.exe --diff

# Process only one cluster
.\experion-license-tool.exe --clusters Galveston-North

# Skip database (no history tracking)
.\experion-license-tool.exe --no-history

# Show all options
.\experion-license-tool.exe --help
```

---

## Understanding the Output

### Excel File Location

Output files are saved to: `data/output/License_Comparison_YYYYMMDD.xlsx`

### Sheet Descriptions

#### Executive Summary
- **Key Metrics:** Total systems, points, estimated cost, issues count
- **Cost by Cluster:** Breakdown if you have multiple clusters
- **Top 5 Action Items:** Prioritized issues requiring attention
- **Legend:** Color code reference

#### PKS / HS / EAS Sheets
Side-by-side comparison of all systems, with:
- License details (MSID, dates, customer)
- Points (Process, SCADA)
- Features (redundancy, integrations)
- Conditional formatting for issues

#### Summary Sheet
Totals by cluster:
- System counts by product type
- Point totals
- Estimated cost breakdown

#### Transfer Candidates
Systems with excess capacity that could potentially transfer points to other systems:
- Excess points above average
- Estimated value of excess
- Recommendation

#### Changes Sheet
What changed since the last run:
- Field name
- Old value
- New value
- Date detected

#### Errors Sheet
Files that couldn't be parsed:
- File path
- Error message

### Color Legend

| Color | Meaning | Action |
|-------|---------|--------|
| **Green** | Transfer candidate | Consider point reallocation |
| **Red** | Stale license (>2 years) | Update license file |
| **Orange** | Invalid customer name | Contact Honeywell to correct |
| **Yellow** | Changed since last run | Review change |

---

## Recommended Workflow

### Initial Setup (One-Time)

1. Gather all license XML files from your Experion systems
2. Configure `settings.json` with your cluster names
3. Add friendly names to `system_names.json`
4. Update `cost_catalog.json` with your pricing (if known)
5. Run the tool to create baseline

### Monthly Review

1. Collect any new/updated license files
2. Run: `experion-license-tool.exe --diff`
3. Review Executive Summary for action items
4. Check Changes sheet for unexpected modifications
5. Archive the Excel file for records

### Quarterly Deep Dive

1. Run full report
2. Review Transfer Candidates for optimization opportunities
3. Update cost catalog with any new PO pricing
4. Share summary with Finance/Procurement
5. Plan any license adjustments with Honeywell

### After License Changes

When Honeywell provides new license files:
1. Replace old XML files in `data/raw/`
2. Run tool immediately
3. Verify changes appear correctly
4. Keep old files archived (the tool handles versioning)

---

## Sharing Results

### With Controls Management

Share the Executive Summary sheet showing:
- Total license inventory
- Systems requiring attention
- Top 5 action items

### With Finance/Procurement

Share:
- Summary sheet with cost estimates
- Note which costs are placeholders vs. confirmed PO pricing
- Transfer Candidates sheet for optimization opportunities

### With Honeywell

Use the PKS/HS/EAS sheets to:
- Verify license accuracy
- Discuss point reallocation
- Plan for renewals

### Archiving

Keep historical Excel files for:
- Audit trails
- Year-over-year comparisons
- Contract negotiations

Recommended: Save to SharePoint with date-based naming:
`License_Report_Galveston_2026Q1.xlsx`

---

## Maintenance

### Updating License Files

When you receive new license files:
1. Copy to appropriate folder in `data/raw/`
2. Keep organized by system folder
3. No need to delete old versions (tool picks highest version)

### Adding New Systems

When a new Experion system is commissioned:
1. Create folder: `data/raw/{Cluster}/{SystemName} {MSID} {Number}/`
2. Copy license XML file
3. Add friendly name to `system_names.json`
4. Run the tool

### Removing Decommissioned Systems

When a system is decommissioned:
1. Move folder to `data/raw/{Cluster}/Decommissioned/` (or delete)
2. Add "Decommissioned" to `exclude_folders` in settings.json
3. Run the tool

### Database Management

The `license_history.db` file:
- Grows slowly over time
- Automatically purges data older than 3 years
- Can be deleted to reset history (tool recreates it)
- Located next to the EXE

### Updating the Tool

When a new version is released:
1. Backup your `config/` folder
2. Extract new distribution
3. Copy your config files back
4. Your `license_history.db` is compatible between versions

---

## FAQ

### Q: Can multiple people use the tool?

**A:** Yes, but each installation maintains its own database. For shared access:
- Run from a shared network location (may be slower)
- Or designate one person to run and share the Excel output

### Q: What if I have multiple sites?

**A:** Two options:
1. **Separate installations** - Each site runs independently
2. **Combined installation** - Use multiple clusters in settings.json

### Q: How do I handle Hot Spare licenses?

**A:** Add "Hot Spare" to `exclude_folders` in settings.json to skip them, or create a separate "HotSpare" cluster to track them separately.

### Q: The tool shows MSID instead of friendly name

**A:** The key in `system_names.json` must match exactly:
- Format: `{Cluster}|{MSID}|{SystemNumber}`
- Check for trailing spaces in the XML
- Run with `--verbose` to see the exact keys

### Q: Cost estimates don't match our actual costs

**A:** Update `config/cost_catalog.json` with your actual Honeywell PO pricing. The default values are estimates and may not reflect your negotiated rates.

### Q: Can I run this on a server?

**A:** Yes, the EXE runs anywhere. For scheduled runs:
```powershell
# Task Scheduler command
C:\Tools\Experion_License_Aggregator\experion-license-tool.exe --verbose
```

### Q: What about Experion HS vs PKS licenses?

**A:** The tool automatically detects the product type from the XML and creates separate sheets for PKS, HS, and EAS.

### Q: How far back does history go?

**A:** The database retains 3 years of snapshots. Older data is automatically purged.

### Q: Can I export to formats other than Excel?

**A:** Currently only Excel is supported. CSV export may be added in a future version.

---

## Getting Help

### Within Marathon

- Contact the Controls team that developed this tool
- Check SharePoint for the latest documentation
- Submit enhancement requests through normal channels

### Technical Issues

- Check the Errors sheet in the output for parsing problems
- Run with `--verbose` for detailed progress
- Check that config files are valid JSON

---

## Appendix: Sample Configuration Files

### settings.json (Single Site)

```json
{
  "clusters": ["Galveston"],
  "exclude_folders": ["Emerson", "EXELE", "GE", "MAXUM", "Hot Spare", "OLD_", "Archived", "Decommissioned"],
  "field_groups": {
    "LICENSE INFO": ["Cluster", "MSID", "System Number", "Release", "Activation Date", "Customer"],
    "POINTS": ["PROCESSPOINTS", "SCADAPOINTS"],
    "STATIONS": ["STATIONS", "MULTISTATIONS", "CONSOLESTATIONS"],
    "FEATURES": ["DUAL", "DAS", "API", "EIOC"]
  },
  "thresholds": {
    "license_age_warning_days": 730,
    "excess_points_absolute": 500,
    "excess_points_percent": 25,
    "placeholder_cost": 100.00
  },
  "valid_customer_patterns": ["Marathon", "MPC"],
  "tracked_fields": ["PROCESSPOINTS", "SCADAPOINTS", "STATIONS", "MULTISTATIONS", "DUAL", "DAS", "API"]
}
```

### system_names.json (Example)

```json
{
  "Galveston|M12345|54321": "HCU",
  "Galveston|M12346|54322": "FCC",
  "Galveston|M12347|54323": "Coker",
  "Galveston|M12348|54324": "Utilities",
  "Galveston|M12349|54325": "Sulfur Recovery",
  "Galveston|M12350|54326": "Crude Unit 1",
  "Galveston|M12351|54327": "Crude Unit 2"
}
```

---

**Document Version:** 2.0
**Last Updated:** January 2026
