# Experion License Aggregator v2.0

A tool to aggregate Honeywell Experion PKS licensing data from XML files into a comprehensive Excel report with cost estimates, change tracking, and actionable recommendations.

## What's New in v2.0

- **Standalone EXE** - No Python installation required
- **SQLite Database** - 3-year historical tracking
- **Change Detection** - See what changed since last run
- **Cost Estimates** - Based on configurable pricing catalog
- **Executive Summary** - Key metrics and Top 5 action items
- **Transfer Candidates** - Identify systems with excess capacity
- **Conditional Formatting** - Color-coded flags for issues

## System Requirements

- Windows 10/11 or Windows Server 2016+
- Microsoft Excel 2016+ or compatible viewer (for viewing output)
- (Python option only) Python 3.7+
- 50 MB disk space
- Network access to license server folders (for direct XML reading)

## Quick Start

### Option 1: Standalone EXE (Recommended)

1. Extract the distribution package
2. Place XML license files in `data/raw/Carson/` and `data/raw/Wilmington/`
3. Double-click `experion-license-tool.exe`
4. Open the generated Excel file in `data/output/`

### Option 2: Python Script

```powershell
# Requires Python 3.7+
pip install -r requirements.txt
python main.py
```

**requirements.txt:**
```
openpyxl>=3.0.0
python-dateutil>=2.8.0
```

## Command Line Options

```
experion-license-tool.exe [options]

  -v, --verbose       Show detailed progress
  -i, --input-dir     Custom input directory (default: data/raw)
  -o, --output-dir    Custom output directory (default: data/output)
  -c, --clusters      Process specific clusters only
  --diff              Show changes since last run
  --no-history        Skip saving to database
  --config            Custom config file path
  --help              Show all options
```

**Examples:**
```powershell
# Standard run
experion-license-tool.exe

# Verbose with change summary
experion-license-tool.exe --verbose --diff

# Process only Carson cluster
experion-license-tool.exe --clusters Carson
```

## Output

### Excel Sheets

| Sheet | Description |
|-------|-------------|
| **Executive Summary** | Key metrics, cost by cluster, Top 5 action items |
| **PKS** | All PKS systems with conditional formatting |
| **HS** | Experion HS (High Security) systems |
| **EAS** | Enterprise Application Servers |
| **Summary** | Totals by cluster including cost estimates |
| **Transfer Candidates** | Systems with excess capacity available for transfer |
| **Changes** | Differences from previous run (if any) |
| **Errors** | Files that couldn't be parsed |

### Color Legend

| Color | Meaning |
|-------|---------|
| **Green** | Transfer candidate (excess capacity) |
| **Red** | Stale license (>2 years old) |
| **Orange** | Invalid customer name (not Marathon/MPC) |
| **Yellow** | Changed since last run |

## Configuration

### config/settings.json

```json
{
  "clusters": ["Carson", "Wilmington"],
  "exclude_folders": ["Emerson", "EXELE", "GE", "MAXUM", "Hot Spare"],
  "thresholds": {
    "license_age_warning_days": 730,
    "excess_points_absolute": 500,
    "excess_points_percent": 25,
    "placeholder_cost": 100.00
  },
  "valid_customer_patterns": ["Marathon", "MPC"],
  "tracked_fields": ["PROCESSPOINTS", "SCADAPOINTS", "STATIONS", "DUAL", "DAS", "API"]
}
```

### config/cost_catalog.json

Pricing for license options (update with actual Honeywell PO values):

```json
{
  "PROCESSPOINTS": {
    "unit_cost": 45.00,
    "per": 50,
    "category": "Points",
    "description": "Process I/O points"
  },
  "DUAL": {
    "unit_cost": 15000.00,
    "per": 1,
    "category": "Redundancy",
    "description": "Server redundancy"
  }
}
```

### config/system_names.json

Maps system identifiers to friendly names:

```json
{
  "Carson|M0614|60806": "ESVT0",
  "Carson|M0922|50215": "ESVT1",
  "Wilmington|M13985-EX04|66533": "ALKY"
}
```

Key format: `{Cluster}|{MSID}|{SystemNumber}`

## Input Data

### Folder Structure

```
data/raw/
├── Carson/
│   ├── ESVT0 M0614 60806/
│   │   └── M0614_Experion_PKS_R52X_x_60806_40.xml
│   └── ESVT1 M0922 50215/
│       └── M0922_Experion_PKS_R52X_x_50215_26.xml
└── Wilmington/
    └── ALKY M13985-EX04 66533/
        └── M13985-EX04_Experion_PKS_R52X_x_66533_25.xml
```

### Filename Pattern

`{MSID}_Experion_{Product}_R{Release}X_x_{Number}_{Version}.xml`

The tool automatically selects the highest version number.

## Utilization Tracking (Optional)

To track actual usage vs licensed capacity, collect current point counts from your Experion servers:

### Data Collection Methods

**Method 1: From Experion System Manager (Recommended)**
1. Open Experion System Manager
2. Go to **Tools → License Manager**
3. Record values under "Points In Use" or "Current Usage"
4. Document date of collection

**Method 2: From Station Display**
1. Log into any Experion operator station
2. Navigate to **System → System Configuration → Licensing**
3. Note "Points in Use" for each license type
4. Record other feature usage (STATIONS, DUAL, DAS, API, etc.)

**Method 3: Automated Query (Contact Honeywell)**
- Honeywell support can provide SQL queries for specific Experion versions
- Query the system configuration database directly
- Export results to CSV for bulk processing

### Fields to Collect (30+ values per system)

**Required for all systems:**
- **PROCESSPOINTS** - Process I/O points in use
- **SCADAPOINTS** - SCADA/remote points in use
- **STATIONS** - Number of flex stations deployed
- **MULTISTATIONS** - Multi-window stations
- **DUAL** - Server redundancy (0 or 1)
- **as_of_date** - Date collected (YYYY-MM-DD)

**Optional (if licensed):**
- CDA_IO_ANA, CDA_IO_DIG (CDA I/O counts)
- DIRECTSTATIONS, DIRECTCLIENTS (Direct connect clients)
- DAS, API, SQL, LAS, DSPBLD (Feature usage)
- TPS, FSC, MODICON, AB, DNP3, OPC_DA (Interface usage)
- VIRTUALIZATION, VIRTUALIZATION_CLIENT (VM licensing)

### Using the Utilization Template

1. **Copy template**: `templates/utilization_input.csv` → `data/utilization_input.csv`
2. **Fill in data**: Open in Excel and populate actual usage values
3. **Run tool**: The tool will calculate utilization percentages and identify underutilized licenses

**Example entry:**
```csv
cluster,msid,system_number,as_of_date,PROCESSPOINTS,SCADAPOINTS,STATIONS,DUAL,DAS,API
Carson,M0614,60806,2026-01-27,2450,1200,8,1,1,0
```

**Output benefits:**
- Utilization % for each license type
- Identify over-licensed systems (transfer candidates)
- Identify under-licensed systems (expansion needed)
- ROI analysis for actual usage vs cost

## Database

`license_history.db` stores snapshots for change tracking:
- **EXE distribution**: Located in the same folder as `experion-license-tool.exe`
- **Python script**: Located in project root directory
- Automatically purges data older than 3 years
- First run creates baseline (no changes to compare)

## File Structure

```
Experion_License_Aggregator/
├── experion-license-tool.exe    # Standalone executable
├── license_history.db           # SQLite database (created on first run)
├── config/
│   ├── settings.json            # Clusters, thresholds, exclusions
│   ├── cost_catalog.json        # License pricing
│   └── system_names.json        # Friendly name mappings
├── data/
│   ├── raw/                     # Source XML files (by cluster)
│   └── output/                  # Generated Excel files
├── templates/
│   ├── utilization_input.csv    # Template for usage data (v2.1)
│   └── cost_import.csv          # Template for cost import
├── QUICK_START.txt              # Quick reference
├── README.md                    # This file
└── USER_GUIDE.md                # Refinery deployment guide
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "No license files found" | Check XML files exist in `data/raw/{Cluster}/{SystemFolder}/` |
| System shows MSID instead of name | Add entry to `system_names.json` with exact key format |
| Cost estimates seem wrong | Update `config/cost_catalog.json` with actual PO pricing |
| Changes not detected | First run creates baseline; check `license_history.db` exists |
| EXE won't run | Ensure `config/` folder exists; check antivirus isn't blocking |
| **Need automated usage extraction** | Contact Honeywell support for SQL query templates specific to your Experion version. Typical sources: `<br>`• Configuration database views (e.g., `SYSTEM_CONFIG` schema)`<br>`• License manager API exports`<br>`• System diagnostic reports from Station Manager`<br>` Request scripts for: point counts, station lists, feature flags |
| **Can't access System Manager** | Alternative: Generate **System Configuration Report** from any station:`<br>`1. Station → Reports → System Configuration`<br>`2. Export to CSV/Excel`<br>`3. Parse for license usage values |

## For Other Refineries

See **USER_GUIDE.md** for detailed instructions on deploying this tool at your site.

## Version History

- **v2.0** (January 2026) - SQLite history, change detection, cost estimates, EXE distribution
- **v1.0** (2025) - Initial release with Excel output

---

For developer/maintainer information, see **HANDOFF.md**.
