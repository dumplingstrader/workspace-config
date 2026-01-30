# Quick Start: New Features

## What's New (Jan 28, 2026)

### 1. MPC 2026 Pricing Override System ✅
Override baseline Honeywell 2021-2022 pricing with confirmed MPC PO pricing.

**Quick Start:**
```powershell
# Edit pricing overrides
notepad config\cost_catalog_mpc_2026.json

# Run tool (automatically uses overrides)
cd scripts
python main.py
```

**Priority:** MPC 2026 Override → Honeywell Baseline → Placeholder

### 2. Utilization Data Parser ✅
Convert Station Manager CSV exports to utilization tracking format.

**Quick Start:**
```powershell
# Place CSV files in: data/raw/Usage/
# (Already have 29 files collected!)

# Parse CSVs
cd scripts
python parse_utilization_csvs.py

# Run aggregator with utilization
python main.py --verbose
```

**Output:** Enhanced Excel with usage %, transfer candidates, under-licensed warnings

---

## Files Created

1. **config/cost_catalog_mpc_2026.json** - MPC 2026 pricing overrides
2. **scripts/parse_utilization_csvs.py** - CSV parser for utilization data
3. **PRICING_AND_UTILIZATION_SETUP.md** - Comprehensive setup guide

## Files Modified

1. **scripts/cost_calculator.py** - Added override catalog support
2. **scripts/main.py** - Auto-detects and uses MPC 2026 pricing

---

## Next Steps

### Step 1: Parse Your Utilization Data
You already have 29 CSV files in `data/raw/Usage/`. Parse them:

```powershell
cd C:\Users\GF99\Documentation\Experion_License_Aggregator\scripts
python parse_utilization_csvs.py
```

Expected output:
```
Found 29 CSV files to process...
  Parsing ESVT0.csv... ✓ (MSID: M0614, System: 60806)
  ...
✓ Successfully created data/utilization_input.csv
  Processed 29 systems
  
  Systems by cluster:
    Carson: 14 systems
    Wilmington: 11 systems
    Salt Lake City: 2 systems
```

### Step 2: Update MPC 2026 Pricing
Review and update pricing in: `config/cost_catalog_mpc_2026.json`

Current entries (update as needed):
- PROCESSPOINTS: $45/50 pts
- SCADAPOINTS: $35/50 pts
- STATIONS: $2,500 each
- DUAL: $15,000
- TPS: $12,000
- OPC_DA: $3,500

Add new entries when you get 2026 PO pricing.

### Step 3: Run License Aggregator
```powershell
cd scripts
python main.py --verbose --diff
```

**New features in output:**
- Pricing source shown for each cost (MPC 2026 vs baseline)
- Utilization % for points, stations, features
- Enhanced transfer candidates (actual excess capacity)
- Under-licensed warnings (approaching capacity)

### Step 4: Review Enhanced Report
Open: `data/output/Experion_License_Report_*.xlsx`

**New sheets:**
- Utilization Summary
- Under-Licensed Systems

**Enhanced sheets:**
- PKS: Now shows Used/Available/Utilization % columns
- Transfer Candidates: Shows actual excess capacity (not just licensed)
- Executive Summary: Includes utilization metrics

---

## Benefits

### Pricing Override System
✅ Accurate 2026 cost estimates  
✅ Easy updates as new POs arrive  
✅ Transparent pricing source tracking  
✅ No need to modify baseline catalog  

### Utilization Integration
✅ True transfer opportunity identification  
✅ Capacity planning for growth  
✅ License compliance monitoring  
✅ ROI calculation for transfers  

**Example:** Transfer 500 excess PROCESSPOINTS from over-licensed system saves $2,250 (at $45/50 pts)

---

## Questions?

See full documentation:
- **PRICING_AND_UTILIZATION_SETUP.md** - Complete setup guide
- **README.md** - General tool documentation
- **USER_GUIDE.md** - Deployment guide for other sites

---

**Ready to run?**
```powershell
cd C:\Users\GF99\Documentation\Experion_License_Aggregator\scripts
python parse_utilization_csvs.py
python main.py --verbose
```
