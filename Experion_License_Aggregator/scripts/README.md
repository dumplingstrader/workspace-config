# Experion License Aggregator - Python Scripts

## Overview

These Python scripts parse Honeywell Experion license XML files, track changes over time, calculate costs, and generate comprehensive Excel reports. The tool automates the aggregation of license data from multiple Experion systems across multiple sites (clusters), providing cost analysis, change detection, and transfer candidate identification.

**What This Tool Does:**
- Scans folders for Experion license XML files
- Automatically selects the highest version per system
- Extracts 30+ license parameters (points, stations, features, interfaces)
- Stores historical snapshots in SQLite for change tracking
- Calculates estimated costs based on configurable pricing catalog
- Identifies systems with excess capacity for license transfers
- Generates comprehensive Excel reports with conditional formatting

## Requirements

```bash
pip install -r requirements.txt
```

**Dependencies:**
- Python 3.7+ (tested on 3.10, 3.11, 3.12)
- openpyxl >= 3.0.0 (Excel file creation and formatting)
- python-dateutil >= 2.8.0 (date parsing from XML files)

**System Requirements:**
- Windows 10/11 or Windows Server 2016+ (or Linux/Mac with Python)
- 50 MB disk space
- Network access to license XML file locations

## Complete Script Suite

### 1. main.py (200 lines)
**Entry point that orchestrates the entire process.**

**5-Step Execution Flow:**
1. **Parse XML files** - Scans data/raw/ for license XML files
2. **Calculate costs** - Applies pricing from cost_catalog.json
3. **Database operations** - Saves snapshot and detects changes
4. **Identify candidates** - Finds systems with excess capacity
5. **Generate Excel** - Creates formatted multi-sheet report

**Command-Line Arguments:**
```bash
python main.py                      # Standard run
python main.py --verbose            # Show detailed progress
python main.py --diff               # Show changes since last run
python main.py --clusters Carson    # Process specific cluster only
python main.py -i C:\MyXMLs         # Custom input directory
python main.py -o C:\Reports        # Custom output directory
python main.py --no-history         # Skip database operations
python main.py --config custom.json # Custom config file
python main.py --help               # Show all options
```

**Features:**
- Loads configuration from settings.json
- Command-line argument parsing with defaults
- Progress reporting for each step
- Error handling with verbose mode for debugging
- Generates timestamped output files
- Creates Top 5 action items based on findings

### 2. xml_parser.py (290 lines)
**Parses Experion license XML files and extracts license information.**

**Core Functionality:**
- **Auto-discovery**: Recursively scans cluster folders for XML files
- **Version selection**: Automatically picks highest version per system
- **Folder exclusion**: Skips non-Experion folders (Emerson, GE, Hot Spare, etc.)
- **Error tracking**: Records unparseable files for troubleshooting

**Key Functions:**
- `parse_xml_file(xml_path)` → Dict - Parse single XML file
- `scan_directory(base_path, cluster_name)` → List[Dict] - Scan folder, select highest version
- `parse_all_licenses(data_dir, clusters, exclude_folders)` → Tuple[List, List] - Parse all clusters
- `_extract_msid(filename)` - Extract MSID from filename pattern
- `_extract_system_number(filename)` - Extract system number from filename
- `_extract_license_options(root)` - Extract all 30+ license parameters

**Extracted System Info:**
- `cluster` - Site name (Carson, Wilmington)
- `msid` - Master System ID (e.g., M0614, M0922)
- `system_number` - System number (e.g., 60806, 50215)
- `product` - Product type (PKS, HS, EAS)
- `release` - Experion release (e.g., R520, R510)
- `customer` - Customer name from license
- `license_date` - License issue date (YYYY-MM-DD)
- `version` - License file version number

**Extracted License Options (30+ fields):**
- **Points**: PROCESSPOINTS, SCADAPOINTS, CDA_IO_ANA, CDA_IO_DIG
- **Stations**: STATIONS, MULTISTATIONS, DIRECTSTATIONS, DIRECTCLIENTS
- **Redundancy**: DUAL, MULTI_SERVER, MULTI_COUNT
- **Features**: DAS, API, SQL, LAS, DSPBLD
- **Interfaces**: CDA, TPS, FSC, MODICON, AB, AB_ETH, DNP3, OPC_DA, OPC_UA_CLIENT, OPC_UA_SERVER
- **Virtualization**: VIRTUALIZATION, VIRTUALIZATION_CLIENT

**Filename Pattern Recognition:**
```
{MSID}_Experion_{Product}_R{Release}X_x_{SystemNumber}_{Version}.xml
Example: M0614_Experion_PKS_R520X_x_60806_40.xml
         └─MSID  └─Product └Release  └─System# └Ver
```

**Auto-Version Selection Example:**
```
System Folder: ESVT0 M0614 60806/
  M0614_Experion_PKS_R520X_x_60806_38.xml  ← Older
  M0614_Experion_PKS_R520X_x_60806_40.xml  ← Selected (highest)
  M0614_Experion_PKS_R520X_x_60806_39.xml  ← Older
```

### 3. database.py (180 lines)
**SQLite database management for license history tracking.**

**Purpose:**
Stores historical snapshots of license data to enable change detection between runs. Each run saves a snapshot with run_date, allowing comparison against previous states.

**Key Functions:**
- `save_snapshot(run_date, licenses)` - Store current snapshot with date
- `get_previous_snapshot(current_date)` - Retrieve most recent snapshot before current date
- `detect_changes(current, previous)` - Compare snapshots and identify changes
- `purge_old_data(days_to_keep=1095)` - Remove snapshots older than 3 years
- `get_snapshot_dates()` - List all snapshot dates in database

**Database Schema:**
```sql
CREATE TABLE license_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_date TEXT NOT NULL,                    -- Snapshot date (YYYY-MM-DD)
    cluster TEXT NOT NULL,                     -- Carson, Wilmington
    msid TEXT NOT NULL,                        -- M0614, M0922, etc.
    system_number TEXT NOT NULL,               -- 60806, 50215, etc.
    product TEXT,                              -- PKS, HS, EAS
    release TEXT,                              -- R520, R510
    customer TEXT,                             -- Customer name
    license_date TEXT,                         -- License issue date
    license_data TEXT NOT NULL,                -- Full JSON of all license options
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(run_date, cluster, msid, system_number)
);

CREATE INDEX idx_cluster_msid ON license_snapshots(cluster, msid, system_number);
CREATE INDEX idx_run_date ON license_snapshots(run_date DESC);
```

**Change Detection:**
Compares tracked fields between current and previous snapshots:
- **NEW**: System added since last run
- **MODIFIED**: License parameter changed (shows old → new, delta)

**Tracked Fields for Changes:**
- PROCESSPOINTS, SCADAPOINTS, STATIONS, MULTISTATIONS
- DIRECTSTATIONS, DUAL, DAS, API, SQL, TPS

**Example Change Record:**
```python
{
    'cluster': 'Carson',
    'msid': 'M0614',
    'system_number': '60806',
    'change_type': 'MODIFIED',
    'field': 'PROCESSPOINTS',
    'old_value': 5000,
    'new_value': 5500,
    'delta': 500
}
```

**Auto-Purge:**
Removes snapshots older than 3 years (1095 days) to prevent database bloat.

**Database Location:**
- Standalone EXE: Same folder as `experion-license-tool.exe`
- Python script: Project root (`license_history.db`)

### 4. cost_calculator.py (165 lines)
**Calculate estimated costs based on cost catalog.**

**Purpose:**
Loads pricing from `cost_catalog.json` and calculates estimated license costs for individual systems and aggregated totals by cluster and category.

**Key Functions:**
- `calculate_item_cost(option_name, quantity)` → Dict - Cost for single license option
- `calculate_system_cost(license_data)` → Dict - Total cost breakdown for one system
- `calculate_all_systems(licenses)` → Dict - Summary with cluster/category totals
- `identify_transfer_candidates(licenses)` → List[Dict] - Find systems with excess capacity

**Cost Calculation Formula:**
```python
units = (quantity + per - 1) // per  # Round up to next unit
total_cost = units * unit_cost

# Example: 5000 PROCESSPOINTS @ $45 per 50
# units = (5000 + 50 - 1) // 50 = 100 units
# total_cost = 100 × $45 = $4,500
```

**Detailed Example:**
```python
# Cost catalog entry
{
  "PROCESSPOINTS": {
    "unit_cost": 45.00,
    "per": 50,
    "category": "Points",
    "description": "Process I/O points"
  }
}

# License data: 5250 PROCESSPOINTS
calculate_item_cost('PROCESSPOINTS', 5250)
# Returns:
{
  'option': 'PROCESSPOINTS',
  'quantity': 5250,
  'unit_cost': 45.00,
  'per': 50,
  'units': 105,              # Rounds up: (5250 + 50 - 1) // 50
  'total_cost': 4725.00,     # 105 × $45
  'category': 'Points',
  'description': 'Process I/O points',
  'is_placeholder': False
}
```

**System Cost Breakdown:**
```python
calculate_system_cost(license_data)
# Returns:
{
  'system': 'Carson - M0614',
  'msid': 'M0614',
  'system_number': '60806',
  'line_items': [
    {'option': 'PROCESSPOINTS', 'total_cost': 4725.00, ...},
    {'option': 'STATIONS', 'total_cost': 25000.00, ...},
    {'option': 'DUAL', 'total_cost': 15000.00, ...}
  ],
  'costs_by_category': {
    'Points': 4725.00,
    'Stations': 25000.00,
    'Redundancy': 15000.00
  },
  'total_cost': 44725.00
}
```

**Transfer Candidate Identification:**
Identifies systems with excess capacity based on configurable thresholds:
- `excess_points_absolute`: Minimum excess points (default: 500)
- `excess_points_percent`: Minimum excess percentage (default: 25%)

**Note:** Actual usage data comes from `utilization_input.csv`. Without usage data, systems with large licensed capacity are flagged as potential candidates.

**Placeholder Costs:**
Items marked with `"is_placeholder": true` in cost_catalog.json use estimated costs and should be updated with actual PO pricing.

### 5. excel_generator.py (330 lines)
**Generate formatted Excel reports with multiple sheets and conditional formatting.**

**Purpose:**
Creates comprehensive Excel workbooks with professionally formatted sheets, color-coded highlights, and automatic column sizing.

**Generated Sheets (in order):**

1. **Executive Summary**
   - Report generation date and time
   - Total systems processed
   - Total estimated cost (grand total)
   - Cost breakdown by cluster (Carson, Wilmington)
   - **Top 5 Action Items** (auto-generated based on findings):
     - Files with parsing errors
     - Changed license parameters requiring review
     - Systems available for license transfers
     - Stale licenses needing updates
     - Missing utilization data

2. **PKS** (Primary Systems Sheet)
   - All PKS systems with full license details
   - Columns: Cluster, System Name, MSID, System #, Product, Release, Customer, License Date
   - License options: PROCESSPOINTS, SCADAPOINTS, STATIONS, MULTISTATIONS, DUAL, DAS, API, TPS
   - Estimated Cost per system
   - **Conditional formatting applied** (see color legend below)

3. **HS** (Experion High Security)
   - HS systems only (if any exist)
   - Same structure as PKS sheet

4. **EAS** (Enterprise Application Servers)
   - EAS systems only (if any exist)
   - Same structure as PKS sheet

5. **Summary**
   - Totals by cluster (system count + total cost)
   - Grand total row (bold)

6. **Transfer Candidates**
   - Systems with excess licensed capacity
   - Columns: Cluster, MSID, System #, Licensed Points, Excess Points, Excess %, Cost Value
   - **Entire rows highlighted in green**

7. **Changes** (only if changes detected)
   - Differences from previous run
   - Columns: Cluster, MSID, System #, Field, Previous, Current, Change (delta)
   - Shows what changed and by how much

8. **Errors** (only if parsing errors occurred)
   - Files that couldn't be parsed
   - Columns: File path, Error message
   - Helps troubleshoot XML format issues

**Conditional Formatting (Color Legend):**

| Color | Hex Code | Meaning | Criteria |
|-------|----------|---------|----------|
| 🟢 **Green** | `C6EFCE` | Transfer candidate | System has excess capacity (>500 points or >25%) |
| 🔴 **Red** | `FFC7CE` | Stale license | License date >2 years old (>730 days) |
| 🟠 **Orange** | `FFEB9C` | Invalid customer | Customer name doesn't contain "Marathon" or "MPC" |
| 🟡 **Yellow** | `FFFF00` | Changed | Parameter changed since previous run |
| 🔵 **Blue** | `4472C4` | Header row | Column headers (white text on blue background) |

**Formatting Applied:**
- Headers: Bold white text on blue background, center-aligned, text wrap
- Auto-sized columns (max 50 characters wide)
- Currency formatting for cost columns ($X,XXX.XX)
- Entire rows highlighted when conditions met (highest priority wins)

**System Name Resolution:**
Loads `config/system_names.json` to display friendly names instead of MSID:
```json
{
  "Carson|M0614|60806": "ESVT0",
  "Carson|M0922|50215": "ESVT1"
}
```
Falls back to MSID if mapping not found.

**Key Functions:**
- `create_executive_summary(summary_data)` - Generate summary with metrics
- `create_pks_sheet(licenses, changes)` - Create PKS systems sheet
- `create_summary_sheet(summary_data)` - Create cluster totals
- `create_transfer_candidates_sheet(candidates)` - Create transfer sheet
- `create_changes_sheet(changes)` - Create changes comparison
- `create_errors_sheet(errors)` - Create error log
- `_apply_conditional_formatting(ws, row, lic, change_keys, num_cols)` - Apply color coding
- `_apply_header_style(ws, row, columns)` - Format header row
- `_auto_size_columns(ws)` - Auto-adjust column widths

## File Structure

```
Experion_License_Aggregator/
├── scripts/
│   ├── main.py              # Entry point
│   ├── xml_parser.py        # XML parsing logic
│   ├── database.py          # SQLite operations
│   ├── cost_calculator.py   # Cost calculations
│   └── excel_generator.py   # Excel report generation
├── config/
│   ├── settings.json        # Clusters, thresholds, exclusions
│   ├── cost_catalog.json    # License pricing
│   └── system_names.json    # Friendly name mappings
├── data/
│   ├── raw/                 # Input XML files (by cluster)
│   └── output/              # Generated Excel reports
├── requirements.txt         # Python dependencies
└── license_history.db       # SQLite database (created on first run)
```

## Configuration

### settings.json
```json
{
  "clusters": ["Carson", "Wilmington"],
  "exclude_folders": ["Emerson", "EXELE", "GE", "Hot Spare"],
  "thresholds": {
    "license_age_warning_days": 730,
    "excess_points_absolute": 500,
    "excess_points_percent": 25,
    "placeholder_cost": 100.00
  }
}
```

### cost_catalog.json
Update with actual Honeywell PO pricing:
```json
{
  "PROCESSPOINTS": {
    "unit_cost": 45.00,
    "per": 50,
    "category": "Points",
    "description": "Process I/O points"
  }
}
```

### system_names.json
Map system IDs to friendly names:
```json
{
  "Carson|M0614|60806": "ESVT0",
  "Carson|M0922|50215": "ESVT1"
}
```

Key format: `{Cluster}|{MSID}|{SystemNumber}`

## Running from Source

### First-time setup:
```bash
cd Experion_License_Aggregator
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### Regular usage:
```bash
cd scripts
python main.py
```

### With options:
```bash
# Verbose output with change detection
python main.py --verbose --diff

# Process only Carson cluster
python main.py --clusters Carson

# Custom paths
python main.py -i C:\MyXMLFiles -o C:\Reports

# Skip database (no history tracking)
python main.py --no-history
```

## Key Features Summary

### ✅ Automated XML Discovery
- Recursively scans cluster folders for XML files
- Automatically selects highest version per system
- Skips excluded folders (Emerson, GE, Hot Spare, etc.)
- Processes multiple clusters in single run

### ✅ Comprehensive Data Extraction
- Extracts 30+ license parameters per system
- Parses system info: MSID, product, release, customer, dates
- Handles all license types: Points, Stations, Features, Interfaces, Virtualization
- Error tracking for unparseable files

### ✅ Historical Change Tracking
- SQLite database stores snapshots with run dates
- Compares current vs previous run
- Identifies NEW systems and MODIFIED parameters
- Shows old → new values with deltas
- Auto-purges data older than 3 years

### ✅ Cost Analysis
- Calculates costs from configurable pricing catalog
- Per-item, per-system, and aggregate calculations
- Breakdown by cluster and category
- Handles unit-based pricing (e.g., $45 per 50 points)
- Supports placeholder costs for unknown items

### ✅ Transfer Candidate Identification
- Identifies systems with excess licensed capacity
- Configurable thresholds (absolute points and percentage)
- Calculates potential cost savings from transfers
- Highlights candidates in green in Excel report

### ✅ Professional Excel Reports
- Multi-sheet workbooks with formatted headers
- **Conditional formatting** with color-coded highlights
- Auto-sized columns for readability
- Friendly system names from configuration
- Currency formatting for costs
- Top 5 action items auto-generated

### ✅ Command-Line Flexibility
- Verbose mode for detailed progress
- Process specific clusters only
- Custom input/output directories
- Skip database operations if needed
- Change detection on demand

## Output

### Excel Report Structure
File generated in `data/output/` with timestamp:
```
Experion_License_Report_20260127_143022.xlsx
```

**Sample Report Structure:**
```
📊 Experion_License_Report_20260127_143022.xlsx
├── 📄 Executive Summary (Key metrics + Top 5 actions)
├── 📄 PKS (All PKS systems with colors)
├── 📄 HS (High Security systems, if any)
├── 📄 EAS (Enterprise App Servers, if any)
├── 📄 Summary (Totals by cluster)
├── 📄 Transfer Candidates (Green highlighted)
├── 📄 Changes (Yellow highlighted, if any)
└── 📄 Errors (Unparseable files, if any)
```

### Database File
```
license_history.db
```
SQLite database with historical snapshots (auto-created on first run).

## Troubleshooting

| Issue | Solution |
|-------|----------|
| **ModuleNotFoundError: No module named 'openpyxl'** | Run `pip install -r requirements.txt` in activated virtual environment |
| **No license files found** | • Check XML files exist in `data/raw/{Cluster}/{SystemFolder}/`<br>• Verify folder structure matches expected pattern<br>• Check cluster names in `config/settings.json` |
| **Database locked** | Close any other process using `license_history.db` (check Task Manager) |
| **Permission error on Excel** | • Close Excel file if open<br>• Check write permissions on `data/output/` folder<br>• Run as administrator if needed |
| **Parsing errors** | • Check XML files are valid Experion format<br>• Review Errors sheet in Excel for details<br>• Verify XML structure matches expected tags<br>• Check for corrupted files |
| **Wrong version selected** | Tool selects highest version by number. Check filename pattern: `*_x_{SystemNumber}_{Version}.xml` |
| **MSID shows Guide

### Adding New License Fields

To track additional license parameters:

1. **Add to settings.json** (`tracked_fields` array):
```json
{
  "tracked_fields": [
    "PROCESSPOINTS",
    "SCADAPOINTS",
    "NEW_FIELD_NAME"  // Add here
  ]
}
```

2. **Add to cost_catalog.json** with pricing:
```json
{
  "NEW_FIELD_NAME": {
    "unit_cost": 1000.00,
    "per": 1,
    "category": "Features",
    "description": "New feature description"
  }
}
```

3. **Update xml_parser.py** (`option_tags` list in `_extract_license_options`):
```python
option_tags = [
    'PROCESSPOINTS', 'SCADAPOINTS',
    'NEW_FIELD_NAME',  # Add here
    # ... rest of fields
]
```

4. **Update excel_generator.py** (headers in `create_pks_sheet`):
```python
headers = [
    'Cluster', 'System Name', 'MSID',
    # ... existing headers
    'NEW_FIELD_NAME',  # Add here
    'Estimated Cost'
]
```

5. **Update column population** in same function:
```python
ws.cell(row=row, column=17, value=lic.get('NEW_FIELD_NAME', 0))
```

### Testing Individual Scripts

Each script has a `__main__` block for standalone testing:

```bash
# Test XML parsing
python xml_parser.py
# Output: Sample parsed license data in JSON format

# Test database operations
python database.py
# Output: Creates test_licenses.db, saves/retrieves snapshot

# Test cost calculations
python cost_calculator.py
# Output: Calculates costs for sample license data

# Test Excel generation
python excel_generator.py
# Output: Creates test_report.xlsx with sample data
```

### Debugging Tips

**Enable verbose output:**
```bash
python main.py --verbose
```

**Check parsed data:**
```python
from xml_parser import parse_all_licenses
from pathlib import Path

licenses, errors = parse_all_licenses(
    Path('../data/raw'),
    ['Carson'],
    []
)

import json
print(json.dumps(licenses[0], indent=2))
```

**Inspect database:**
```bash
# Using SQLite command line
sqlite3 license_history.db
.tables
SELECT * FROM license_snapshots ORDER BY run_date DESC LIMIT 5;
.quit
```

**Test cost calculations:**
```python
from cost_calculator import CostCalculator

calc = CostCalculator('../config/cost_catalog.json')
cost = calc.calculate_item_cost('PROCESSPOINTS', 5000)
print(f"Cost: ${cost['total_cost']:,.2f}")
Each script has a `__main__` block for standalone testing:
```bash
python xml_parser.py    # Test XML parsing
python database.py      # Test database operations
python cost_calculator.py  # Test cost calculations
python excel_generator.py  # Test Excel generation
```

## Building Standalone EXE

To create the standalone `.exe` (using PyInstaller):
```bash
pip install pyinstaller
pyinstaller --onefile --name experion-license-tool ^
    --add-data "../config;config" ^
    --add-data "../templates;templates" ^
    main.py
```

The EXE will be in `dist/experion-license-tool.exe`

## License

Internal use only - Marathon Petroleum Corporation

---

**Last Updated:** January 2026  
**Version:** 2.0
