# LA Refinery Process Control Spend Tracker
## User Guide

**Version:** 1.1
**Last Updated:** January 2026
**Author:** Process Control Team (developed with AI assistance)

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Initial Setup](#initial-setup)
4. [Weekly Workflow](#weekly-workflow)
5. [Understanding the Output](#understanding-the-output)
6. [Troubleshooting](#troubleshooting)
7. [FAQ](#faq)
8. [Appendix: SAP Transaction Reference](#appendix-sap-transaction-reference)

---

## Overview

### What This Tool Does

This automation tool consolidates your spend tracking by:

1. **Importing ME2K exports** - Your PO commitments from SAP
2. **Importing TS Actuals** - All GL postings including cross-charges
3. **Identifying cross-charges** - Flags allocations you did not initiate
4. **Creating summary views** - Budget vs Actual by Internal Order
5. **Tracking Watson Cogen separately** - Dedicated tab for IO# 9913117
6. **Generating monthly pivots** - Spend by month for trending

### What Problems It Solves

| Before | After |
|--------|-------|
| Manual entry from SAP into Excel | Automated import from exports |
| No visibility into cross-charges | Cross-charges flagged automatically |
| Reconciliation gaps with Finance | Same data source as Finance (TS Actuals) |
| Hours of manual work weekly | Minutes to run script |

### Internal Orders Tracked

| Order Number | Description |
|--------------|-------------|
| 9909811 | PC - Software & Contracts |
| 9909813 | PC - Outside Support (Contractors) |
| 9909815 | PC - Hardware & Materials |
| 9909818 | PC - APC Work & Maint |
| 9912360 | PC - Dept Misc Exp & Travel |
| 9913117 | Watson Cogen (dedicated tab) |

---

## Prerequisites

### Software Requirements

- Windows 10/11
- Python 3.8 or higher
- VSCode (recommended) or any text editor
- Microsoft Excel (for viewing output)
- AI coding assistant (optional, for modifications)

### SAP Access Requirements

- ME2K transaction access (Purchase Orders by Account Assignment)
- Ability to export to Excel (.xlsx)

### Files You Will Need

1. **ME2K Export** - You create this from SAP
2. **TS Actuals** - Your supervisor provides this monthly

---

## Initial Setup

### Step 1: Install Python (if not already installed)

1. Open a web browser and go to: https://www.python.org/downloads/
2. Download Python 3.11 or later
3. Run the installer
4. **IMPORTANT:** Check the box "Add Python to PATH"
5. Click "Install Now"

### Step 2: Extract the Package

Extract the Spend Tracker package to your desired location:
```
C:\Users\[YourUsername]\Documents\SpendTracker\
```

The folder structure should look like:
```
SpendTracker\
├── scripts\
│   └── spend_tracker.py
├── docs\
│   ├── USER_GUIDE.md
│   └── TECHNICAL_HANDOFF.md
├── data\           (place input files here)
├── output\         (reports generated here)
├── run_tracker.ps1
├── setup.ps1
└── QUICK_START.txt
```

### Step 3: Install Required Python Packages

Run the setup script (double-click or run in PowerShell):
```
.\setup.ps1
```

Or manually install:
```
pip install pandas openpyxl --break-system-packages
```

### Step 4: Verify Setup

1. Open PowerShell in the SpendTracker folder
2. Run:
   ```
   python scripts\spend_tracker.py
   ```
3. You should see a message about missing input files (this is expected)

---

## Weekly Workflow

### Step 1: Export ME2K Data from SAP

1. Log into SAP
2. Enter transaction: **ME2K**
3. Enter selection criteria:
   - **Order:** Enter your Internal Order number (e.g., 9909815)
   - **Plant:** R180
   - You may need to run multiple times for each IO, or use a range
4. Execute the report (F8)
5. Go to **List > Export > Spreadsheet**
6. Save as Excel format (.xlsx)
7. Move the file to the **data** folder
8. Ensure filename starts with "EXPORT_" (e.g., `EXPORT_20260126.xlsx`)

**Tip:** Run ME2K for each Internal Order you want to track, or ask your supervisor if there is a way to run it for all orders at once.

### Step 2: Obtain TS Actuals File

1. Request the TS Actuals export from your supervisor
2. This is typically provided monthly
3. Move the file to the **data** folder
4. Name it something containing "ts_actual" (e.g., `ts_actual_jan2026.xlsx`)

### Step 3: Run the Script

Double-click `run_tracker.ps1` or run from PowerShell:
```
.\run_tracker.ps1
```

Or run Python directly:
```
python scripts\spend_tracker.py
```

The script will:
- Find the latest ME2K and TS Actuals files in the data folder
- Process and combine the data
- Generate an output file in the output folder

### Step 4: Review the Output

1. Navigate to the `output\` folder
2. Open the latest `SpendTracker_Output_[timestamp].xlsx` file
3. Review each tab (see next section for details)

### Step 5: Archive Input Files (Optional)

After processing, you may want to move old input files to a dated archive folder to keep things organized.

---

## Understanding the Output

### Tab: Summary

**Purpose:** High-level view of spend by Internal Order

| Column | Description |
|--------|-------------|
| Internal_Order | The IO number |
| Description | IO name |
| PO_Commitments | Total value of all POs |
| Open_Commitments | Amount not yet invoiced |
| Actuals_YTD | What has actually hit the GL |
| Cross_Charges | Allocations/charges you did not initiate |
| Variance | Actuals minus PO Commitments (should explain differences) |

**What to look for:**
- Large variances may indicate cross-charges or missing POs
- Cross_Charges column shows "mystery" charges

### Tab: ME2K_Commitments

**Purpose:** Detail of all POs from ME2K export

| Column | Description |
|--------|-------------|
| Order | Internal Order number |
| Purchasing Document | PO number |
| Document Date | When PO was created |
| Name of Supplier | Vendor name |
| Short Text | Item description |
| Net Order Value | Total PO value |
| Still to be invoiced (val.) | Open amount per SAP |
| Open_Commitment | Calculated open amount |

### Tab: TS_Actuals

**Purpose:** All GL postings from Finance's data

| Column | Description |
|--------|-------------|
| Order | Internal Order number |
| Order Desc | IO description |
| Vendor Name | Who was paid |
| Purchase Order | PO number (if applicable) |
| Posting Date | When it hit the GL |
| Actuals | Dollar amount |
| Month | Fiscal month |
| Acctg Doc Type | Type of document (Invoice, Accrual, etc.) |
| Doc Header Text | Description |
| Line Item Text | Detail description |

### Tab: Cross_Charges

**Purpose:** Highlights charges that bypassed the PO process

**This is your "mystery charge" detector!**

These entries typically include:
- G/L account documents (corporate allocations)
- G/L Accrual Postings
- CO Postings
- Intercompany charges

**Action:** Review these monthly. If you see unexpected charges, discuss with Finance.

### Tab: Monthly_Pivot

**Purpose:** Spend by Internal Order by Month

Use this to:
- Identify spending trends
- Compare month-over-month
- Support forecasting discussions

### Tab: Watson_Cogen

**Purpose:** Dedicated tracking for IO# 9913117

Shows:
- All PO commitments for Watson Cogen
- All actuals posted to Watson Cogen
- Total spend

### Tab: IO_Reference

**Purpose:** Quick reference of Internal Order numbers and descriptions

---

## Troubleshooting

### Problem: "No module named pandas"

**Cause:** Python packages not installed

**Solution:**
```
pip install pandas openpyxl --break-system-packages
```

### Problem: "No ME2K export found"

**Cause:** Script cannot find the file

**Solutions:**
1. Ensure the file is in the `data\` folder
2. Ensure the filename starts with "EXPORT_"
3. Ensure it is an .xlsx file (not .xls or .csv)

### Problem: "No TS Actuals found"

**Cause:** Script cannot find the file

**Solutions:**
1. Ensure the file is in the `data\` folder
2. Ensure the filename contains "ts_actual" (case insensitive)
3. Ensure it is an .xlsx file

### Problem: Script shows Unicode/encoding errors

**Cause:** Special characters in data

**Solution:** The script is designed to handle this by converting to ASCII. If you still see errors:
1. Open the problematic Excel file
2. Save it as a new file (this sometimes cleans up encoding)
3. Re-run the script

### Problem: "Permission denied" when saving output

**Cause:** Output file is open in Excel

**Solution:** Close the previous output file in Excel, then re-run the script

### Problem: ME2K export has different column names

**Cause:** SAP configuration may vary

**Solution:**
1. Open the ME2K export and note the exact column names
2. Edit the script's `load_me2k_export` function to match
3. Or contact your SAP admin to standardize the export

### Problem: Numbers look wrong or are zero

**Cause:** Column mapping issue

**Solution:**
1. Open the raw ME2K or TS Actuals file
2. Verify the column names match what the script expects
3. Check if numbers are formatted as text (common SAP issue)

### Problem: Watson Cogen tab is empty

**Cause:** No data for IO# 9913117

**Solution:**
1. Verify 9913117 is the correct order number for Watson Cogen
2. Ensure you included it in your ME2K export
3. Check if it exists in the TS Actuals file

---

## FAQ

### Q: How often should I run this?

**A:** Weekly is recommended, plus at month-end when Finance starts asking questions.

### Q: Can I add more Internal Orders?

**A:** Yes! Edit the `INTERNAL_ORDERS` dictionary in the script:
```python
INTERNAL_ORDERS = {
    "9909811": "PC - Software & Contracts",
    # Add new ones here:
    "1234567": "New Order Description",
}
```

### Q: Can I change the file locations?

**A:** Yes! Edit these variables at the top of the script:
```python
DATA_FOLDER = BASE_FOLDER / "data"
OUTPUT_FOLDER = BASE_FOLDER / "output"
```

### Q: What if I have multiple ME2K exports?

**A:** The script uses the most recently modified file. If you need to combine multiple exports:
1. Run ME2K for all orders
2. Copy/paste all results into one Excel file
3. Save with a name starting with "EXPORT_"
4. Run the script

### Q: Can my supervisor use this too?

**A:** Yes! Share the distribution package. They will need:
- Python installed
- The same folder structure (provided in package)
- Access to the same input files

### Q: How do I compare to Finance's numbers?

**A:**
1. Look at the TS_Actuals tab - this is the same source Finance uses
2. Sum by Internal Order and compare to Finance's report
3. Any differences should be in timing or categorization

### Q: What are "accrual reversals"?

**A:** Accruals are estimates Finance posts at month-end for expected invoices. Reversals back them out the next month when the real invoice hits. The net effect should be zero over time, but they can cause month-to-month confusion.

---

## Appendix: SAP Transaction Reference

### ME2K - Purchase Orders by Account Assignment

**Purpose:** List all POs charged to a specific Internal Order or Cost Center

**Key Fields:**
- Order: Internal Order number
- Plant: R180 for LA Refinery
- Purchasing Group: Optional filter

**Export Steps:**
1. Execute report
2. List > Export > Spreadsheet
3. Choose "Excel" format
4. Save to data folder

### KOB1 - Order Line Items

**Purpose:** All postings to an Internal Order (alternative to TS Actuals)

**Key Fields:**
- Order: Your Internal Order number
- Controlling Area: R021 (Carson) or R020 (Wilmington)
- Fiscal Year: Current year

### KSB1 - Cost Center Line Items

**Purpose:** All postings to a Cost Center

**Key Fields:**
- Cost Center: Your cost center number
- Controlling Area: R021 or R020
- Fiscal Year: Current year

### ME23N - Display Purchase Order

**Purpose:** View details of a single PO

**Use for:** Researching specific PO questions

---

## Support

For questions about this tool:
- Review this guide first
- Check the Troubleshooting section
- Contact your Process Control budget team

For SAP access issues:
- Contact MPC IT Service Desk

---

*This tool was developed to support LA Refinery Process Control budget management. It may be adapted for other refineries with appropriate modifications to Internal Order mappings.*
