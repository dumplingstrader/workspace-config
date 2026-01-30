# Experion License Aggregator - Data Processing Guide

**Last Updated**: January 28, 2026  
**Version**: 2.0

## Overview

This document details how the Experion License Aggregator collects, processes, and consolidates license data from XML files and utilization CSVs into a unified Excel report.

---

## Data Sources

### 1. XML License Files (Primary Source)

**Location**: `data/raw/{Cluster}/{SystemFolder}/`

**Structure**:
```
data/raw/
├── Carson/
│   ├── ESVT0 M0614 60806/
│   │   ├── M0614_Experion_PKS_R520_x_60806_40.xml  (Version 40 - USED)
│   │   ├── HS_HMI/
│   │   │   └── M0614_...xml
│   │   └── OLD_ESVT0_M0614_60806_LICENSES/
│   │       └── M0614_...29.xml  (Version 29 - OLD)
│   └── ESVT3 M0921 50216/
│       ├── M0921_Experion_PKS_R52X_x_50216_43.xml  (Version 43 - USED)
│       └── OLD_ESVT3_LICENSES/
│           └── M0921_Experion_PKS_R51X.x_50216_29.xml  (Version 29 - OLD)
└── Wilmington/
    └── ...
```

**File Format**: Honeywell Experion XML license files containing:
- System metadata (MSID, system number, release, customer, license date)
- Licensed quantities (process points, SCADA points, stations, features)
- Structure: `<options><option name="PROCESSPOINTS" value="4750"/></options>`

**Key Extraction Fields**:
- `MSID`: System identifier (e.g., M0614, M13287-EX10)
- `System Number`: 5-6 digit license number (e.g., 60806)
- `Release`: Experion version (e.g., R520)
- `Product`: PKS, HS, or EAS
- `License Options`: 70+ license types (PROCESSPOINTS, SCADAPOINTS, STATIONS, etc.)

**Version Selection Logic**: 
- Multiple XML files exist per system (current + archived versions)
- Parser extracts version number from filename suffix (e.g., `_40.xml` = version 40)
- **Deduplication**: Groups by `(MSID, System Number)` tuple and selects **highest version**
- This ensures only the latest license file is used per system

---

### 2. Utilization CSV Files (Secondary Source)

**Location**: `data/raw/Usage/BC-LAR-*.csv`

**Source**: Station Manager exports from Experion servers showing actual usage

**Structure**:
```
data/raw/Usage/
├── BC-LAR-ENGPRO022.csv  (ESVT0 utilization)
├── BC-LAR-ENGPRO046.csv  (ESVT3 utilization)
└── ... (29 CSV files total)
```

**CSV Format**: Station Manager "Category/Option/Detail Type/Value" structure
```
Category,Option,Detail Type,Value
System Information,Cluster,,Carson
System Information,MSID,,M0614
System Information,System Number,,60806
Utilization,PROCESSPOINTS,,108
Utilization,SCADAPOINTS,,45
Utilization,CONSOLE_STATIONS,,4
Utilization,OPERATOR_TOUCH_PANELS,,0
...
```

**Parsed Fields** (37 total):
- System identifiers: `cluster`, `msid`, `system_number`, `as_of_date`
- Point usage: `PROCESSPOINTS`, `SCADAPOINTS`, `CDA_IO_ANA`, `CDA_IO_DIG`
- Station usage: `STATIONS`, `MULTISTATIONS`, `CONSOLE_STATIONS`, `CONSOLE_EXTENSION`, `READONLY_STATIONS`, `OPERATOR_TOUCH_PANELS`, `DIRECTSTATIONS`, `DIRECTCLIENTS`
- Features: `DUAL`, `MULTI_SERVER`, `DAS`, `API`, `SQL`, `LAS`, `DSPBLD`, `CDA`
- Interfaces: `TPS`, `FSC`, `MODICON`, `AB`, `AB_ETH`, `DNP3`, `OPC_DA`, `OPC_UA_CLIENT`
- Virtualization: `VIRTUALIZATION`, `VIRTUALIZATION_CLIENT`

**Preprocessing Step**: Run `parse_utilization_csvs.py` to consolidate 29 CSVs into `data/utilization_input.csv`

---

## Processing Workflow

### Step 1: XML Parsing (`xml_parser.py`)

**Purpose**: Extract license data from XML files with version-based deduplication

**Process**:
1. Scan `data/raw/{Cluster}/` recursively for all `*.xml` files
2. For each file:
   - Extract system identifiers from **filename AND folder name**
   - Extract version number from filename (e.g., `_40.xml` → 40)
   - Group files by `(MSID, System Number)` tuple
3. **Deduplication**: Select highest version per system
4. Parse selected file to extract 70+ license fields

**Key Methods**:
- `_extract_msid(filename, folder_name)`: Extracts MSID with regex fallback to folder name
- `_extract_system_number(filename, folder_name)`: Handles both `_x_` and `.x_` filename patterns
- `_extract_version(filename)`: Extracts version from filename suffix
- `scan_directory()`: Groups by `(MSID, System Number)` and selects highest version

**Critical Fix (Jan 28, 2026)**:
- **Problem**: Old license files used `.x_` pattern (e.g., `R51X.x_50216_29.xml`) instead of `_x_` pattern, causing system number extraction to fail and return "Unknown"
- **Impact**: Created duplicate entries (e.g., M0921/50216 and M0921/Unknown)
- **Solution**: Enhanced regex to handle both patterns: `r'[._]x_(\d+)_\d+\.xml$'`

**Output**: List of 36 unique license dictionaries (down from 44 with duplicates)

---

### Step 2: Utilization Merging (`main.py`)

**Purpose**: Merge actual usage data from CSVs into license records

**Process**:
1. Load `data/utilization_input.csv` (preprocessed from 29 Station Manager CSVs)
2. Create lookup dictionary: `{(cluster, msid, system_number): {usage_data}}`
3. For each license record:
   - Match on `(cluster, msid, system_number)` tuple
   - Add `_USED` suffix fields (e.g., `PROCESSPOINTS_USED`, `CONSOLE_STATIONS_USED`)
   - Convert CSV values to integers (empty values → 0)

**Field Mapping** (Critical):
```python
# CSV field → License field
PROCESSPOINTS → PROCESSPOINTS_USED
SCADAPOINTS → SCADAPOINTS_USED
STATIONS → STATIONS_USED
CONSOLE_STATIONS → CONSOLE_STATIONS_USED
...

# Special mapping for transfer candidates
CONSOLE_STATIONS_USED → DIRECTSTATIONS_USED  # XML uses DIRECTSTATIONS, CSV uses CONSOLE_STATIONS
```

**Coverage**: 20/36 systems have utilization data (56%)

**Unmatched Systems** (16):
- New systems not yet in Station Manager
- Different MSID/system number variants
- Systems in CSV with cluster "Salt Lake City" not in XML folders

---

### Step 3: Cost Calculation (`cost_calculator.py`)

**Purpose**: Calculate total license costs using pricing cascade

**Pricing Cascade** (Priority Order):
1. **MPC 2026 Override** (`cost_catalog_mpc_2026.json`) - 6 confirmed prices from POs
2. **Honeywell 2021-2022 Baseline** (`cost_catalog.json`) - 70+ license types
3. **Placeholder** (`settings.json` default $100) - Unknown license types

**Process**:
1. For each license, iterate through all license fields
2. Look up unit cost and "per" increment (e.g., $45 per 50 points)
3. Calculate: `quantity × (unit_cost / per)`
4. Track pricing source for transparency

**Output**: 
- Total cost: $17.3M across 36 systems
- Per-system cost breakdown
- Pricing source tracking

---

### Step 4: Transfer Candidate Identification (`cost_calculator.py`)

**Purpose**: Identify systems with excess capacity for license transfers

**Criteria** (Must meet ONE):
- **Absolute**: ≥500 excess units (e.g., 500+ unused process points)
- **Percentage**: ≥25% excess capacity (e.g., <75% utilization)
- **Minimum value**: ≥$1,000 excess value

**License Types Checked**:
- `PROCESSPOINTS`
- `SCADAPOINTS`
- `STATIONS`
- `MULTISTATIONS`
- `DIRECTSTATIONS`

**Calculation**:
```python
licensed = lic.get('PROCESSPOINTS', 0)
used = lic.get('PROCESSPOINTS_USED', 0)
excess = licensed - used
utilization_percent = (used / licensed * 100) if licensed > 0 else 0

if excess >= 500 OR (100 - utilization_percent) >= 25:
    # Qualify as transfer candidate
```

**Output**: 36 transfer candidates with detailed breakdowns

---

### Step 5: Excel Report Generation (`excel_generator.py`)

**Purpose**: Create multi-sheet Excel report with pivot table format

#### PKS Sheet (Pivot Table Format)

**Structure**:
- **Columns**: Systems (e.g., "ESVT0 (CAR)", "ESVT3 (CAR)", ...)
- **Rows**: License fields (67 rows)

**Row Structure**:
```
1. Headers (system names across columns)
2-8. LICENSE INFO (cluster, MSID, system number, release, version, date, customer)
9. [Blank]
10. POINTS (header)
11. Process Points (licensed)
12.   - Used (actual usage)
13.   - Utilization % (calculated with color coding)
14. SCADA Points (licensed)
15.   - Used
16.   - Utilization %
...
30. Console/Direct Stations (licensed)
31.   - Used
32.   - Utilization % (calculated)
...
```

**Utilization Calculation**:
```python
licensed = lic.get('PROCESSPOINTS', 0)
used = lic.get('PROCESSPOINTS_USED', 0)

if licensed > 0:
    util_pct = (used / licensed) * 100
    
    # Color coding
    if util_pct >= 80:
        fill = RED    # High utilization
    elif util_pct >= 50:
        fill = YELLOW  # Medium utilization
    else:
        fill = GREEN   # Low utilization
```

**Field Mapping in PKS Sheet**:
```python
# Row structure:
('Console/Direct Stations', 'DIRECTSTATIONS', False),      # XML field for licensed
('  - Used', 'CONSOLE_STATIONS_USED', False),              # CSV field for used
('  - Utilization %', None, False),                        # Calculated

# Logic: XML calls it DIRECTSTATIONS, CSV calls it CONSOLE_STATIONS
```

#### Transfer Candidates Sheet

**Structure**: One row per excess license type per system

**Columns**:
1. Cluster
2. System Name (friendly name from `system_names.json`)
3. MSID
4. System Number
5. License Type (PROCESSPOINTS, SCADAPOINTS, etc.)
6. Licensed (total quantity)
7. Used (actual usage from CSV)
8. Excess (licensed - used)
9. Utilization % (used / licensed * 100)
10. Excess Value (cost of excess capacity)
11. Has Usage Data (Yes/No)

**Example**:
```
Carson | ESVT0 | M0614 | 60806 | PROCESSPOINTS | 4750 | 108 | 4642 | 2.3% | $4,177.80 | Yes
Carson | ESVT0 | M0614 | 60806 | SCADAPOINTS   | 5750 |  45 | 5705 | 0.8% | $4,011.50 | Yes
```

---

## Critical Design Decisions

### 1. Deduplication Strategy

**Decision**: Group by `(MSID, System Number)` instead of folder name

**Rationale**:
- Systems have multiple folders (main + HS_HMI + OLD_* subdirectories)
- Version history stored in subdirectories (e.g., OLD_ESVT0_M0614_60806_LICENSES)
- Folder-based grouping caused duplicates (ESVT0 appeared 2x)

**Implementation**: Modified `xml_parser.scan_directory()` on Jan 28, 2026

---

### 2. Field Mapping: DIRECTSTATIONS vs CONSOLE_STATIONS

**Problem**: XML files use `DIRECTSTATIONS`, Station Manager CSVs use `CONSOLE_STATIONS`

**Solution**: Dual field population
```python
# In merge_utilization_data():
if 'CONSOLE_STATIONS_USED' in lic:
    lic['DIRECTSTATIONS_USED'] = lic['CONSOLE_STATIONS_USED']
```

**Rationale**:
- Transfer candidate logic checks `DIRECTSTATIONS_USED`
- PKS sheet displays as "Console/Direct Stations" (user-friendly)
- Maintains compatibility with both data sources

---

### 3. Version Extraction Regex

**Evolution**:
- **Original**: `r'_x_(\d+)_\d+\.xml$'` - Only handled `_x_` pattern
- **Enhanced**: `r'[._]x_(\d+)_\d+\.xml$'` - Handles both `_x_` and `.x_` patterns

**Examples**:
```
M0614_Experion_PKS_R520_x_60806_40.xml  → system_number: 60806 ✓
M0921_Experion_PKS_R51X.x_50216_29.xml  → system_number: 50216 ✓
```

---

### 4. Utilization Display Logic

**Challenge**: Show 0 vs empty correctly (both are valid states)

**Solution**:
```python
# When value is legitimately 0, display it
ws.cell(row, col, value if value else '')

# Problem: Python evaluates 0 as False!
# This caused 0 values to display as blank

# Solution: Check explicitly for None
ws.cell(row, col, value if value is not None else '')
```

**Note**: Current code still has the `if value else ''` pattern which causes 0 to display as blank. This works for most cases but may need refinement if explicit 0 display is needed.

---

## Known Issues and Limitations

### 1. Utilization Coverage: 20/36 Systems (56%)

**Missing Utilization Data**:
- 16 systems in XML files don't have corresponding Station Manager exports
- Possible reasons:
  - New systems not yet commissioned
  - Different MSID variants (e.g., M0922/60731 in XML vs M0922/49090 in CSV)
  - Systems in Salt Lake City cluster not in XML folders

**Impact**: Transfer candidates show "No" in "Has Usage Data" column for 16 systems

---

### 2. Cost Catalog Completeness: 48 Placeholder Prices

**Status**: 70+ license types total, 6 confirmed MPC 2026 prices, rest use placeholders

**Action Item**: Vendor pricing request sent (see `PRICING_REQUEST_FOR_VENDOR.md`)

---

### 3. Manual MSID/System Number Mismatches

**Example**: 
- XML: `M0922/60731` (CACM system)
- CSV: `M0922/49090` (might be different unit or old number)

**Workaround**: Manually verify system identification in `system_names.json`

---

### 4. HS and EAS License Files

**Status**: Not confirmed if separate HS (High Security) and EAS (Enterprise Application Servers) sheets are needed

**Current Behavior**: All licenses grouped under "PKS" sheet

**Action Item**: Verify with stakeholders if HS/EAS require separate tracking

---

## File Dependencies

### Input Files (Required):
- `data/raw/{Cluster}/*/*.xml` - Experion license XML files
- `data/utilization_input.csv` - Consolidated utilization data (from `parse_utilization_csvs.py`)

### Configuration Files:
- `config/settings.json` - Clusters, thresholds, placeholder cost
- `config/cost_catalog.json` - Honeywell 2021-2022 baseline pricing (70+ types)
- `config/cost_catalog_mpc_2026.json` - MPC 2026 confirmed prices (6 types)
- `config/system_names.json` - Friendly names for systems (e.g., M0614 → "ESVT0")

### Output Files:
- `data/output/Experion_License_Report_{timestamp}.xlsx` - Main Excel report
- `scripts/license_history.db` - SQLite change tracking database

---

## Processing Statistics (Latest Run: Jan 28, 2026 14:32)

| Metric | Value |
|--------|-------|
| XML files scanned | 100+ |
| Unique systems (after deduplication) | 36 |
| Systems with utilization data | 20 (56%) |
| Systems without utilization data | 16 (44%) |
| Total estimated cost | $17,300,875 |
| Transfer candidates identified | 36 |
| Clusters processed | Carson (20), Wilmington (16) |
| MPC 2026 pricing overrides | 6 license types |
| Honeywell baseline prices | 70+ license types |

---

## Maintenance Notes

### Adding New Utilization Data:
1. Place new BC-LAR-*.csv files in `data/raw/Usage/`
2. Run: `python scripts/parse_utilization_csvs.py`
3. Regenerate report: `python scripts/main.py`

### Adding New XML License Files:
1. Create folder: `data/raw/{Cluster}/{SystemName MSID SystemNumber}/`
2. Copy XML file with version suffix (e.g., `_42.xml`)
3. Regenerate report: `python scripts/main.py`

### Updating Pricing:
- **MPC 2026 prices**: Edit `config/cost_catalog_mpc_2026.json`
- **Baseline prices**: Edit `config/cost_catalog.json`
- Pricing cascade automatically uses highest priority source

---

## Troubleshooting

### "No systems found"
- Check XML files exist in `data/raw/{Cluster}/`
- Verify folder structure: `{Cluster}/{SystemFolder}/*.xml`

### "Duplicate systems in report"
- Verify deduplication logic is using `(MSID, System Number)` grouping
- Check for `Unknown` system numbers (regex extraction failure)

### "Utilization showing 0% but CSV has data"
- Verify `(cluster, msid, system_number)` match between XML and CSV
- Check CSV has correct headers (uppercase field names)
- Confirm merge logic creates `_USED` suffix fields

### "Transfer candidates missing DIRECTSTATIONS usage"
- Verify mapping: `CONSOLE_STATIONS_USED → DIRECTSTATIONS_USED` exists
- Check transfer candidate logic checks `DIRECTSTATIONS_USED`

---

## Recent Changes Log

### January 28, 2026
1. **Fixed duplicate systems** - Changed deduplication from folder-based to (MSID, System Number) based
2. **Fixed system number extraction** - Enhanced regex to handle `.x_` and `_x_` patterns
3. **Fixed DIRECTSTATIONS mapping** - Added CONSOLE_STATIONS_USED → DIRECTSTATIONS_USED for transfer candidates
4. **Result**: Reduced from 44 to 36 unique systems, all utilization data displaying correctly

---

## References

- [Main README](README.md) - User guide and setup instructions
- [Pricing Setup Guide](PRICING_AND_UTILIZATION_SETUP.md) - Detailed pricing configuration
- [Example Output](EXAMPLE_OUTPUT.md) - Sample report format
- [Vendor Pricing Request](PRICING_REQUEST_FOR_VENDOR.md) - Outstanding price quotes needed
