# Experion License Utilization Data Collection Guide

## Overview

To enable utilization tracking and identify over/under-licensed systems, collect actual usage data from each Experion server. This guide covers **3 methods** for gathering the required values.

---

## Required Data Per System (30+ Fields)

### Core Fields (Always Collect)
| Field | Description | Where to Find |
|-------|-------------|---------------|
| **PROCESSPOINTS** | Process I/O points in use | System Manager → License Manager → Points In Use |
| **SCADAPOINTS** | SCADA/remote points in use | Same location as PROCESSPOINTS |
| **STATIONS** | Flex stations deployed | Count from Station Manager or config export |
| **MULTISTATIONS** | Multi-window stations | Station configuration |
| **DUAL** | Server redundancy (0/1) | System architecture (1=redundant, 0=simplex) |
| **as_of_date** | Collection date | Use format: YYYY-MM-DD |

### Optional Fields (Collect if Licensed)
| Category | Fields | Description |
|----------|--------|-------------|
| **CDA I/O** | CDA_IO_ANA, CDA_IO_DIG | CDA analog/digital I/O counts |
| **Direct Clients** | DIRECTSTATIONS, DIRECTCLIENTS | Direct connect stations/clients |
| **Features** | DAS, API, SQL, LAS, DSPBLD | Feature flags (0=not used, 1=in use) |
| **Interfaces** | TPS, FSC, MODICON, AB, AB_ETH, DNP3, OPC_DA, OPC_UA_CLIENT | Interface usage (0/1 or count) |
| **Virtualization** | VIRTUALIZATION, VIRTUALIZATION_CLIENT | VM licensing (count of virtualized instances) |

---

## Method 1: System Manager (GUI) - Recommended for Small Sites

**Best for:** 1-5 systems, occasional spot checks

### Steps:
1. **Open System Manager** on any engineering workstation
2. **Navigate to License Manager:**
   - **R510-R520**: Tools → License Manager
   - **R400-R500**: System → Licensing
3. **Record Point Counts:**
   - Look for "Points In Use" or "Current Usage" section
   - Note PROCESSPOINTS and SCADAPOINTS values
4. **Check Feature Usage:**
   - Features tab shows enabled options (DAS, API, SQL, etc.)
   - Record as 1 (enabled) or 0 (disabled)
5. **Station Count:**
   - Go to Station Manager or Stations view
   - Count total stations by type (Flex, Multi-window, Direct)
6. **Export (optional):**
   - Some versions allow "Export to CSV" from License Manager
   - If available, export and map columns to template

### Pros:
- No scripting required
- Visual confirmation of values
- Accessible to operators

### Cons:
- Manual data entry prone to errors
- Time-consuming for 10+ systems
- Must repeat for each cluster

---

## Method 2: Station System Configuration Report - For Medium Sites

**Best for:** 5-20 systems, monthly/quarterly reviews

### Steps:
1. **From Any Operator Station:**
   - Navigate: System → Reports → System Configuration
2. **Generate Report:**
   - Select "License Information" section
   - Choose "Export to Excel" or "Export to CSV"
3. **Parse Export:**
   - Open exported file
   - Look for rows with license types (PROCESSPOINTS, STATIONS, etc.)
   - Column typically shows: License Type | Licensed | In Use
4. **Map to Template:**
   - Copy "In Use" values to `utilization_input.csv`
   - Ensure MSID and System Number match your XML filenames

### Pros:
- Semi-automated
- Export includes most fields
- Can be scheduled from station

### Cons:
- Export format varies by Experion version
- May require parsing script for bulk processing
- Not all fields always included

---

## Method 3: Database Query (SQL) - For Large Sites & Automation

**Best for:** 20+ systems, continuous monitoring, automated reporting

### Overview:
Experion stores license usage in its configuration database. Honeywell can provide version-specific SQL queries.

### Prerequisites:
- **Database access credentials** (read-only sufficient)
- **SQL client** (SQL Server Management Studio, DBeaver, etc.)
- **Query templates** from Honeywell support (version-dependent)

### Example Query Structure (Generic - Request actual syntax from Honeywell):
```sql
-- Generic example - ACTUAL QUERY SYNTAX VARIES BY VERSION
SELECT 
    l.MSID,
    l.SystemNumber,
    l.LicenseType,
    l.PointsLicensed,
    l.PointsInUse,
    GETDATE() AS CollectionDate
FROM 
    SystemConfig.dbo.LicenseUsage l
WHERE 
    l.LicenseType IN ('PROCESSPOINTS', 'SCADAPOINTS', 'STATIONS')
ORDER BY 
    l.MSID, l.LicenseType;
```

### Steps:
1. **Request Query from Honeywell:**
   - Contact: Your Honeywell Field Service Engineer or TAC
   - Provide: Experion version (e.g., R520.3)
   - Request: SQL query for license usage extraction
2. **Connect to Database:**
   - Use provided credentials (typically read-only service account)
   - Database name: Often `SystemConfig` or `ExperionDB`
3. **Execute Query:**
   - Run query for each cluster/server
   - Export results to CSV
4. **Transform to Template:**
   - Pivot data: Rows → Columns for each system
   - Map LicenseType names to template column names
   - Merge with `utilization_input.csv` template

### Automation Option:
Create PowerShell/Python script to:
```powershell
# Pseudo-code example
foreach ($server in $servers) {
    $result = Invoke-SqlCmd -Server $server -Query $query
    Export-Csv -Path "utilization_$server.csv"
}
# Merge all CSVs into utilization_input.csv
```

### Pros:
- **Fully automated** - Run on schedule
- **Bulk extraction** - All systems at once
- **Accurate** - Direct from source database
- **Scriptable** - Integrate with other tools

### Cons:
- Requires database access (may need approval)
- Query syntax varies by Experion version
- Initial setup effort

---

## Field Collection Tips

### For Point Counts:
- **PROCESSPOINTS**: Look for "Process I/O", "AI/AO/DI/DO", or "Controller Points"
- **SCADAPOINTS**: May be labeled "Remote I/O", "Network Points", or "SCADA"
- Values should be whole numbers (e.g., 2450, not 2450.5)

### For Feature Flags (DAS, API, SQL, etc.):
- Use **1** if feature is actively used (enabled in config)
- Use **0** if feature is licensed but not configured/used
- Leave **blank** if feature is not licensed at all

### For Station Counts:
- **STATIONS**: Regular flex stations (count actual deployed, not licensed max)
- **MULTISTATIONS**: Stations with multi-window capability
- **DIRECTSTATIONS**: Direct-connect engineering stations
- Count only **active/deployed** stations, not hot spares

### For Redundancy:
- **DUAL**: Use 1 if system has redundant servers, 0 for simplex
- **MULTI_SERVER**: Advanced redundancy (3+ servers) - use count

### Date Format:
- Always use **YYYY-MM-DD** (e.g., 2026-01-27)
- Collect all systems on same day if possible for consistency

---

## Troubleshooting Data Collection

| Issue | Solution |
|-------|----------|
| "License Manager shows 0 points" | Check if viewing correct server; may need admin privileges |
| "Station count doesn't match" | Exclude decommissioned/hot spare stations from count |
| "Feature flag unclear" | Check System Configuration → Enabled Features list |
| "Database access denied" | Request read-only credentials from IT; query only needs SELECT |
| "Export missing some fields" | Combine multiple reports (License + Station + Features); supplement with System Manager |
| "Values change frequently" | Normal for point counts as I/O is added/removed; collect monthly average |

---

## Validation Checklist

Before submitting `utilization_input.csv`:

- [ ] **MSID and System Number match XML filenames exactly**
- [ ] **as_of_date is current (within last 30 days)**
- [ ] **Point counts are reasonable** (not 0 unless truly unused)
- [ ] **Station counts include only active stations**
- [ ] **Feature flags are 0 or 1** (not blank if licensed)
- [ ] **All required systems have entries** (match clusters in XML files)
- [ ] **CSV format is valid** (no extra commas, quotes properly escaped)

---

## Next Steps

After collecting data:

1. **Save to:** `data/utilization_input.csv` (not templates/ folder)
2. **Run tool:** Execute `experion-license-tool.exe` (utilization automatically processed)
3. **Review output:** Check new sheets in Excel output:
   - **Utilization Summary**: Overall usage percentages
   - **Transfer Candidates**: Systems with excess capacity
   - **Under-Licensed**: Systems nearing/exceeding capacity

---

## Contact for Automated Extraction

**Honeywell Support Contacts:**
- **Field Service Engineer (FSE)**: Your assigned FSE can provide queries
- **Technical Assistance Center (TAC)**: 1-800-XXX-XXXX (insert actual number)
- **Request**: "SQL query template for license usage extraction - Experion R5XX"

**Include in request:**
- Experion version (e.g., R520.3 Update 4)
- Database type (SQL Server, Oracle, etc.)
- Desired output format (CSV preferred)
- Fields needed (reference `utilization_input.csv` template)

---

**Last Updated:** January 2026  
**Version:** 2.0
