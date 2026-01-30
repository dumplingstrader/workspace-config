# LA Refinery Process Control Spend Tracker
## Technical Handoff Document

**Version:** 1.1
**Last Updated:** January 2026
**Author:** Process Control Team (developed with AI assistance)
**Classification:** Internal Use - Marathon Petroleum

---

## Document Purpose

This technical handoff document is intended for:
- Future maintainers of this automation
- IT support personnel
- Other refinery Process Control teams considering adoption
- Budget analysts who need to understand the data flow

---

## Executive Summary

### Business Problem

Process Control budget owners at LA Refinery (Carson, Wilmington, Watson Cogen) were manually tracking spend by:
1. Logging into SAP ME23N to view individual POs
2. Transcribing data into an Excel spreadsheet
3. Manually reconciling against Finance's reports
4. Experiencing "mystery charges" from cross-charges and allocations

This consumed significant time weekly and led to reconciliation gaps with Finance.

### Solution

An automated Python-based tool that:
1. Imports ME2K exports (PO commitments)
2. Imports TS Actuals (GL postings - same source as Finance)
3. Identifies and flags cross-charges
4. Generates consolidated Excel workbook with multiple views
5. Provides dedicated tracking for Watson Cogen

### Key Metrics

| Metric | Before | After |
|--------|--------|-------|
| Weekly time investment | 2-4 hours | 15-30 minutes |
| Cross-charge visibility | None | 100% |
| Reconciliation accuracy | ~85% | ~98% |
| Data sources unified | No | Yes |

---

## System Architecture

### Data Flow Diagram

```
+------------------+     +------------------+
|   SAP System     |     |   Finance Team   |
+------------------+     +------------------+
         |                        |
         | ME2K Export            | TS Actuals Export
         | (Manual)               | (Monthly)
         v                        v
+------------------+     +------------------+
|   data\ folder   |     |   data\ folder   |
+------------------+     +------------------+
         |                        |
         +----------+  +----------+
                    |  |
                    v  v
           +------------------+
           |  spend_tracker.py |
           |  (Python Script)  |
           +------------------+
                    |
                    v
           +------------------+
           |  output\ folder  |
           |  (.xlsx files)   |
           +------------------+
                    |
                    v
           +------------------+
           |  Excel / User    |
           |  Review          |
           +------------------+
```

### Technology Stack

| Component | Technology | Version |
|-----------|------------|---------|
| Language | Python | 3.8+ |
| Data Processing | pandas | Latest |
| Excel I/O | openpyxl | Latest |
| IDE (recommended) | VSCode | Latest |
| AI Assistance | Any coding assistant | Optional |

### File Structure

```
SpendTracker\
├── scripts\
│   └── spend_tracker.py      # Main automation script
├── docs\
│   ├── USER_GUIDE.md         # End-user documentation
│   └── TECHNICAL_HANDOFF.md  # This document
├── data\                     # Input files go here
│   ├── EXPORT_20260126.xlsx
│   └── ts_actual_jan2026.xlsx
├── output\                   # Generated reports
│   ├── SpendTracker_Output_20260126_143052.xlsx
│   └── ...
├── run_tracker.ps1           # Run script
├── setup.ps1                 # Setup script
├── requirements.txt          # Python dependencies
└── QUICK_START.txt           # Quick reference
```

---

## Data Sources

### ME2K Export (PO Commitments)

**SAP Transaction:** ME2K - Purchase Orders by Account Assignment

**How Obtained:** Manual export by budget owner

**Frequency:** Weekly or as needed

**File Pattern:** `EXPORT_*.xlsx`

**Key Columns:**

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| Order | String | Internal Order number (e.g., "9909815") |
| Purchasing Document | String | PO number |
| Document Date | Date | PO creation date |
| Supplier/Supplying Plant | String | Vendor number + name |
| Short Text | String | Line item description |
| Net Price | Numeric | Unit price |
| Net Order Value | Numeric | Total line value |
| Still to be invoiced (qty) | Numeric | Open quantity |
| Still to be invoiced (val.) | Numeric | Open value |
| Name of Supplier | String | Vendor name |
| Plant | String | R180 for LA Refinery |

**Known Issues:**
- Column names may vary by SAP configuration
- "Still to be invoiced" may not be reliable for all PO types
- Need to run separately for each Internal Order (or use variant)

### TS Actuals (GL Postings)

**Source:** Finance team SAP extract

**How Obtained:** Provided by supervisor monthly

**Frequency:** Monthly (can be more frequent if requested)

**File Pattern:** `*ts_actual*.xlsx` (case insensitive)

**Key Columns:**

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| Cost Center | String | SAP cost center |
| Cost Center Name | String | Cost center description |
| Order | String | Internal Order number |
| Order Desc | String | IO description |
| Vendor | String | Vendor number |
| Vendor Name | String | Vendor name |
| Purchase Order | String | PO number (if applicable) |
| Posting Date | Date | GL posting date |
| Actuals | Numeric | Dollar amount |
| Month | Integer | Fiscal month (1-12) |
| Fiscal Year | Integer | Fiscal year |
| Acctg Doc Type | String | Document type (critical for cross-charge detection) |
| Doc Header Text | String | Document description |
| Line Item Text | String | Line item description |

**Document Types (Acctg Doc Type):**

| Type | Description | PO-Related? |
|------|-------------|-------------|
| Invoice receipt | Standard PO invoice | Yes |
| Goods receipt | PO goods receipt | Yes |
| Concur to SAP | Expense reports | No |
| G/L Accrual Posting | Month-end accruals | Sometimes |
| G/L account document | Allocations, cross-charges | No |
| CO Posting | Cost object postings | No |
| Account Maintenance | Adjustments | No |
| S&U Tax Adjustment | Sales/use tax | Yes |

---

## Internal Order Mapping

### LA Refinery Process Control Orders

| Unify Order # | Legacy Order # | Description | Budget Owner |
|---------------|----------------|-------------|--------------|
| 9909811 | 99001110 | PC - Software & Contracts | Process Control |
| 9909813 | 99001108 | PC - Outside Support (Contractors) | Process Control |
| 9909815 | 99001106 | PC - Hardware & Materials | Process Control |
| 9909818 | 99001103 | PC - APC Work & Maint | Process Control |
| 9912360 | N/A | PC - Dept Misc Exp & Travel | Process Control |
| 9913117 | N/A | Watson Cogen | Process Control |

### Site Codes

| Code | Description |
|------|-------------|
| R180 | LA Refinery (combined) |
| R190 | Watson Cogen (separate plant code) |
| LARC | Los Angeles Refining Complex |
| LARC-C | Carson |
| LARC-W | Wilmington |
| RWCC | Watson Cogen |

### Controlling Areas

| Code | Description |
|------|-------------|
| R021 | CA-Carson Refinery |
| R020 | CA-Wilmington Refinery |

---

## Script Technical Details

### Configuration Section

Location in script: Lines 38-65 (approximately)

```python
# Determine base folder (parent of scripts folder)
SCRIPT_DIR = Path(__file__).resolve().parent
BASE_FOLDER = SCRIPT_DIR.parent

# Folder structure
DATA_FOLDER = BASE_FOLDER / "data"
OUTPUT_FOLDER = BASE_FOLDER / "output"

# Internal Order mapping
INTERNAL_ORDERS = {
    "9909811": "PC - Software & Contracts",
    "9909813": "PC - Outside Support (Contractors)",
    "9909815": "PC - Hardware & Materials",
    "9909818": "PC - APC Work & Maint",
    "9912360": "PC - Dept Misc Exp & Travel",
    "9913117": "Watson Cogen",
}

# Watson Cogen specific order
WATSON_COGEN_ORDER = "9913117"

# File naming patterns
ME2K_PATTERN = "EXPORT_*.xlsx"
TS_ACTUALS_PATTERN = "*ts_actual*.xlsx"
```

### Cross-Charge Detection Logic

The script identifies cross-charges by document type:

```python
cross_charge_types = [
    'G/L account document',
    'G/L Accrual Posting',
    'CO Posting',
    'Account Maintenance'
]
```

Additionally, it flags entries where `Doc Header Text` contains:
- "ALLOCATION"
- "ALLOC"
- "CROSS"

### Error Handling

The script handles:
- Missing input files (warns and continues with available data)
- Missing columns (warns and skips affected calculations)
- Unicode/encoding issues (converts to ASCII with replacement)
- Permission errors (fails gracefully with message)

### Output File Naming

Format: `SpendTracker_Output_YYYYMMDD_HHMMSS.xlsx`

Example: `SpendTracker_Output_20260126_143052.xlsx`

---

## Customization for Other Refineries

### Step 1: Update Internal Orders

Edit the `INTERNAL_ORDERS` dictionary to match your refinery's orders:

```python
INTERNAL_ORDERS = {
    "YOUR_ORDER_1": "Description 1",
    "YOUR_ORDER_2": "Description 2",
    # etc.
}
```

### Step 2: Update Site Codes

If your refinery uses different plant codes, update references to "R180".

### Step 3: Update Controlling Area

If using KOB1/KSB1 directly, update controlling area codes.

### Step 4: Verify Column Names

ME2K exports may have different column names depending on SAP configuration. Verify and update the `load_me2k_export` function if needed.

### Step 5: Test with Sample Data

Run with a small dataset first to verify mappings are correct.

---

## Known Limitations

### Current Limitations

1. **Single ME2K file processing** - Script uses the most recent file only. Multiple exports must be manually combined.

2. **No direct SAP integration** - Requires manual export. Future enhancement could use SAP RFC if IT approves.

3. **TS Actuals dependency** - Requires supervisor to provide file monthly. Cannot self-service.

4. **No budget integration** - Budget numbers must be added manually or in a separate process.

5. **Static IO mapping** - Adding/removing Internal Orders requires script edit.

### Future Enhancement Opportunities

1. **SAP RFC integration** - Direct pull from SAP if IT approves API access
2. **Budget file integration** - Auto-import Finance budget template
3. **Email automation** - Auto-send summary to stakeholders
4. **Web dashboard** - Real-time visibility via intranet
5. **Multi-refinery consolidation** - Corporate-level rollup
6. **Forecasting module** - Predict spend based on open POs and historical patterns

---

## Troubleshooting Guide (Technical)

### Debug Mode

To enable verbose output, add this at the start of the script:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Common Issues

**Issue:** `UnicodeDecodeError`

**Cause:** Non-ASCII characters in SAP data

**Solution:** The script uses `safe_string()` function to handle this. If still occurring:
```python
# Force ASCII encoding on problematic column
df['Column'] = df['Column'].apply(lambda x: str(x).encode('ascii', 'replace').decode('ascii'))
```

**Issue:** `KeyError: 'Column Name'`

**Cause:** SAP export has different column names

**Solution:** Print actual columns and update script:
```python
print(df.columns.tolist())
```

**Issue:** Numbers importing as text

**Cause:** SAP formatting

**Solution:** Force numeric conversion:
```python
df['Amount'] = pd.to_numeric(df['Amount'].str.replace(',', ''), errors='coerce')
```

**Issue:** Date parsing failures

**Cause:** Inconsistent date formats

**Solution:** Specify format explicitly:
```python
df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y', errors='coerce')
```

---

## Security Considerations

### Data Sensitivity

- This tool processes financial data
- Output files should be treated as confidential
- Do not store in shared/public folders
- Follow MPC data handling policies

### Access Control

- Script runs with user's permissions
- No elevated privileges required
- SAP access controlled by existing roles

### Audit Trail

- Each output file is timestamped
- Input files should be archived for reference
- Consider adding logging for compliance

---

## Maintenance Schedule

### Weekly

- Run script after ME2K export
- Review cross-charges tab
- Archive input files

### Monthly

- Obtain fresh TS Actuals from supervisor
- Run full reconciliation
- Compare to Finance reports
- Update forecast as needed

### Quarterly

- Review Internal Order mappings
- Check for new allocations or charge patterns
- Update script if needed

### Annually

- Review with Finance for process changes
- Update budget integration
- Consider enhancements based on user feedback

---

## Contact Information

### Primary Support

- **Role:** Process Control Budget Owner
- **Scope:** Day-to-day usage, data questions

### Secondary Support

- **Role:** Process Control Supervisor
- **Scope:** TS Actuals access, Finance liaison

### Technical Support

- **Role:** MPC IT Service Desk
- **Scope:** Python installation, SAP access issues

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | Jan 2026 | Process Control Team | Initial release |
| 1.1 | Jan 2026 | Process Control Team | Reorganized folder structure |

---

## Appendix A: Complete Column Mapping Reference

### ME2K Export Columns (Expected)

```
Item
Seq. No. of Account Assgt
WBS Element
Order
Asset
Sub-number
SD Document
Item
Network
Activity
Purchasing Doc. Type
Purch. Doc. Category
Purchasing Group
PO history/release documentation
Document Date
Supplier/Supplying Plant
Material
Short Text
Material Group
Item Category
Acct Assignment Cat.
Plant
Storage Location
Order Quantity
Order Unit
Net Price
Currency
Acc. assgt quantity
Price unit
Purchasing Document
Purch. Organization
Item Category
Req. Tracking Number
Quantity in SKU
Outline agreement
Still to be invoiced (qty)
Still to be invoiced (val.)
Name of Supplier
Net Order Value
Profit Center
```

### TS Actuals Columns (Expected)

```
Cost Center
Cost Center Name
Order
Order Desc
Order Expense Class
Order Type
Order Revision
ProjectID
ProjectID Desc
WBS Element
WBS Element Desc
Proj Type
Proj Type Desc
Stat Order
Stat Order Desc
Cost Element
Cost Element Name
Vendor
Vendor Name
Purchase Order
Material Group
Material Group Desc
Material
Material Desc
Acctg Doc Type
CO Doc Type
Doc Header Text
Line Item Text
Ref Key 1
Ref Key 2
Ref Key 3
CO Doc Number
Ref Doc Number
Partner Object
Posting Date
PCF Category
Actuals
Month
Fiscal Year
PCF Major
PCF Minor
Refinery Forecast Category
Major Expense Category
Minor Expense Category
Mapping
Sub Dept
```

---

*End of Technical Handoff Document*
