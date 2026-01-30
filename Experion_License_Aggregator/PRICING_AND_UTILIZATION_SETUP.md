# Pricing Override & Utilization Data Setup Guide

## Overview

This guide explains how to use the new MPC 2026 pricing override system and integrate actual utilization data from your Experion servers.

---

## Part 1: MPC 2026 Pricing Override System

### Purpose
Override baseline Honeywell 2021-2022 pricing with confirmed 2026 MPC PO pricing for accurate cost estimates.

### Pricing Priority Order
1. **MPC 2026 Override** - `config/cost_catalog_mpc_2026.json` (highest priority)
2. **Honeywell 2021-2022 Baseline** - `config/cost_catalog.json`
3. **Placeholder** - Default cost from `settings.json` (unknown items)

### Setup Instructions

#### 1. Review Current Override Catalog
File: `config/cost_catalog_mpc_2026.json`

**Current MPC 2026 pricing entries:**
- PROCESSPOINTS: $45 per 50 points
- SCADAPOINTS: $35 per 50 points
- STATIONS: $2,500 per station
- DUAL: $15,000 per redundancy
- TPS: $12,000 per interface
- OPC_DA: $3,500 per server

#### 2. Add New MPC 2026 Pricing
When you receive a new 2026 MPC PO with pricing, add entries to `cost_catalog_mpc_2026.json`:

```json
{
  "DAS": {
    "unit_cost": 8500.00,
    "per": 1,
    "category": "Features",
    "description": "Data Acquisition Service - MPC 2026 pricing",
    "source": "2026 MPC PO #12345",
    "effective_date": "2026-01-01"
  }
}
```

**Key fields:**
- `unit_cost`: Cost per `per` units
- `per`: Number of units per pricing increment (e.g., 50 for points, 1 for features)
- `source`: PO number or source document
- `effective_date`: When pricing became effective

#### 3. Verify Pricing Source in Reports
After running the tool, check the Excel output. Each cost line item now includes:
- **pricing_source**: Shows whether using MPC 2026 override or baseline

### Example Cost Comparison

**Scenario:** System with 5000 PROCESSPOINTS

**Using Honeywell 2021-2022 baseline:**
```
Cost = (5000 ÷ 50) × $45 = $4,500
Source: Honeywell 2021-2022 Baseline
```

**Using MPC 2026 override:**
```
Cost = (5000 ÷ 50) × $50 = $5,000
Source: MPC 2026 Override
```

### Maintenance

**When to update:**
- Received new 2026 MPC PO with updated pricing
- Negotiated pricing changes with Honeywell
- Need to adjust estimates based on actuals

**Best practices:**
1. **Document source**: Always include PO number in `source` field
2. **Date tracking**: Use `effective_date` for audit trail
3. **Backup**: Keep copy of baseline `cost_catalog.json` for comparison
4. **Version control**: Consider git history for pricing changes

---

## Part 2: Utilization Data Integration

### Purpose
Compare actual usage vs licensed capacity to identify over/under-licensed systems and calculate true cost savings from license transfers.

### Collected Data Location
Your collected CSV files are in: `data/raw/Usage/`

**Systems found (29 files):**
- Carson: ESVT0-6, CPD, CRU, DCU, CALK, CHCU, WHCU, REF1, LARCACM, LARCEMDB01
- Wilmington: WALK, SPW, SHB, SCR, SA, RPS, NA, HTU, ETD, LARWACM, LARWEMDB01
- Other: SRPESVT, SRPSRV

### Step-by-Step Setup

#### Step 1: Parse Utilization CSVs
Run the parser script to convert Station Manager exports to the format needed by the license aggregator:

```powershell
cd C:\Users\GF99\Documentation\Experion_License_Aggregator\scripts
python parse_utilization_csvs.py
```

**What this does:**
1. Reads all CSV files from `data/raw/Usage/`
2. Extracts license usage values (Process points, SCADA points, Stations, etc.)
3. Maps systems to clusters (Carson, Wilmington, etc.)
4. Creates `data/utilization_input.csv` in the correct format

**Expected output:**
```
Found 29 CSV files to process...
  Parsing ESVT0.csv... ✓ (MSID: M0614, System: 60806)
  Parsing ESVT1.csv... ✓ (MSID: M0922, System: 50215)
  ...

✓ Successfully created data/utilization_input.csv
  Processed 29 systems

  Systems by cluster:
    Carson: 14 systems
    Wilmington: 11 systems
    Salt Lake City: 2 systems
    Unknown: 2 systems
```

#### Step 2: Review and Adjust Cluster Mappings
If any systems show as "Unknown" cluster, edit the mapping function:

**File:** `scripts/parse_utilization_csvs.py`  
**Function:** `map_to_cluster()`

```python
def map_to_cluster(system_name: str, msid: str) -> str:
    """Map system name or MSID to cluster."""
    carson_systems = ['ESVT0', 'ESVT1', ...]  # Add your systems here
    wilmington_systems = ['WALK', 'SPW', ...]
    
    # Add custom logic here
    if system_name in carson_systems:
        return 'Carson'
    # ... etc
```

#### Step 3: Verify Utilization Data
Open `data/utilization_input.csv` and verify:

- [ ] MSID and System Number match XML filenames
- [ ] Cluster assignments are correct
- [ ] as_of_date is current (2026-01-27)
- [ ] Point counts look reasonable (not all zeros)
- [ ] Station counts match actual deployed stations

**Example row:**
```csv
cluster,msid,system_number,as_of_date,PROCESSPOINTS,SCADAPOINTS,...
Carson,M0614,60806,2026-01-27,108,45,0,0,,,,,1,,,,,,,1,0,,,,,,,
```

#### Step 4: Run License Aggregator with Utilization
```powershell
cd scripts
python main.py --verbose
```

**New output includes:**
- Utilization % for each license type
- "Under-licensed" warnings (usage approaching/exceeding capacity)
- Enhanced transfer candidate identification (now based on actual excess vs used)

#### Step 5: Review Enhanced Excel Report
**New sheets in output:**
- **Utilization Summary**: Usage % by system and license type
- **Under-Licensed Systems**: Systems nearing capacity (warning threshold)
- **Transfer Candidates** (enhanced): Now shows actual excess capacity available for transfer

**New columns in PKS sheet:**
- `PROCESSPOINTS_Used`: Actual usage
- `PROCESSPOINTS_Avail`: Available capacity
- `PROCESSPOINTS_Util%`: Utilization percentage

**Color coding:**
- 🟢 Green: Transfer candidate (significant excess capacity)
- 🟡 Yellow: Approaching capacity (>80% utilized)
- 🔴 Red: At/over capacity (>95% utilized)

### Utilization Data Format Reference

**CSV Structure:**
```csv
cluster,msid,system_number,as_of_date,PROCESSPOINTS,SCADAPOINTS,STATIONS,...
```

**Key Fields:**
- **PROCESSPOINTS**: Process I/O points actually in use
- **SCADAPOINTS**: SCADA points actually in use
- **STATIONS**: Number of deployed flex stations
- **DUAL**: 1 if redundant, 0 if simplex
- **DAS, API, SQL, etc.**: 1 if used, 0 if not used, blank if not licensed

**Feature Flags (0/1):**
- `1` = Feature is actively used/deployed
- `0` = Feature is licensed but not configured/used
- blank = Feature is not licensed

---

## Part 3: Complete Workflow

### Initial Setup (One-Time)
```powershell
# 1. Parse utilization CSVs
cd C:\Users\GF99\Documentation\Experion_License_Aggregator\scripts
python parse_utilization_csvs.py

# 2. Review utilization_input.csv
notepad ..\data\utilization_input.csv

# 3. Adjust cluster mappings if needed (edit parse_utilization_csvs.py)

# 4. Update MPC 2026 pricing (edit config/cost_catalog_mpc_2026.json)
notepad ..\config\cost_catalog_mpc_2026.json
```

### Regular Updates (Monthly/Quarterly)
```powershell
# 1. Collect new utilization CSVs from servers
# Place in: data/raw/Usage/

# 2. Re-parse utilization data
python parse_utilization_csvs.py

# 3. Run license aggregator
python main.py --verbose --diff

# 4. Review Excel report
start ..\data\output\Experion_License_Report_*.xlsx
```

### Adding New MPC 2026 Pricing
```json
// config/cost_catalog_mpc_2026.json
{
  "NEW_OPTION": {
    "unit_cost": 1200.00,
    "per": 1,
    "category": "Features",
    "description": "New feature - MPC 2026 pricing",
    "source": "2026 MPC PO #67890",
    "effective_date": "2026-02-01"
  }
}
```

Then run: `python main.py` (override applied automatically)

---

## Troubleshooting

### Issue: Parser Can't Find Usage CSVs
**Solution:** Verify files are in `data/raw/Usage/` (not `data/Usage/`)

### Issue: Wrong Cluster Assignments
**Solution:** Edit `map_to_cluster()` in `parse_utilization_csvs.py` and re-run parser

### Issue: Utilization Values Seem Wrong
**Check:**
1. CSV export format matches expected structure (Category, License Option, Detail Type, Value)
2. Using "Used" values, not "Licensed" or "Available"
3. Date collected is recent (<30 days old)

### Issue: MPC 2026 Pricing Not Applied
**Check:**
1. File exists: `config/cost_catalog_mpc_2026.json`
2. JSON syntax is valid (no trailing commas, proper quotes)
3. Option name matches exactly (case-sensitive)

### Issue: Missing Utilization Fields
**Solution:** CSV parser may need adjustment for your Experion version's export format. Edit field extraction logic in `parse_experion_csv()` function.

---

## Benefits of This Setup

### With Pricing Override:
✅ Accurate 2026 cost estimates  
✅ Compare baseline vs actual pricing  
✅ Audit trail of pricing changes  
✅ Easy updates as new POs arrive  

### With Utilization Data:
✅ Identify truly under-utilized systems  
✅ Quantify actual cost savings from transfers  
✅ Plan capacity for future growth  
✅ Justify license purchase decisions  
✅ Monitor license compliance (at/over capacity)  

### Combined Power:
✅ **True ROI calculation**: Transfer 500 excess PROCESSPOINTS from ESVT0 → ESVT3 saves $2,250 (at MPC 2026 pricing)  
✅ **Capacity planning**: ESVT2 at 92% utilization → budget for expansion  
✅ **License optimization**: 15 systems with >30% excess capacity → $150K+ in transfer opportunities  

---

## Next Steps

1. **Run parser**: `python parse_utilization_csvs.py`
2. **Review output**: Check `data/utilization_input.csv`
3. **Update pricing**: Add any known 2026 MPC pricing to override catalog
4. **Generate report**: `python main.py --verbose`
5. **Analyze results**: Look for transfer candidates and under-licensed systems

For questions or issues, refer to the main README.md or USER_GUIDE.md.

---

**Last Updated:** January 28, 2026  
**Version:** 2.0 with Pricing Override & Utilization Support
