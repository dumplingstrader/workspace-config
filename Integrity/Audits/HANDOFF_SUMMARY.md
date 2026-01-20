# Enhanced Integrity Deployment Readiness Checklist - Handoff Summary

**Date Created**: January 16, 2026  
**Last Updated**: January 20, 2026  
**Project Owner**: Marathon Petroleum - Keith Mazy, Don Clark (lar-integrityrequests@marathonpetroleum.com)  
**Purpose**: Deployment guidance for Hexagon Integrity implementations at Marathon refinery sites

---

## Executive Summary

This project produces a comprehensive deployment readiness checklist for Hexagon Integrity (PTC asset management system) implementations. It was created based on lessons learned from actual Marathon Petroleum deployments at ROB, LAR, GBR, and SPP sites where issues included:
- **Budget overruns**: CPI 0.62 (spending $1.00 to get $0.62 worth of work)
- **Scope creep**: GBR added 1,614 assets after OSW sign-off
- **Data collection delays**: 60% of delays due to incomplete L1 inventories
- **Cost waste**: $10K-$30K in idle consultant time due to missing prerequisites

The checklist provides 148 specific tasks across 5 deployment phases to prevent these issues at future sites.

---

## Deliverable

### Primary File
**`Enhanced_Integrity_Deployment_Readiness_Checklist.xlsx`** (148 KB)

Multi-sheet Excel workbook containing:

1. **Executive Summary** - Lessons learned, financial metrics, critical success factors
2. **Phase 1: Pre-Planning (Items 1-29)** - Stakeholder engagement, L1 inventory, program accessibility, installation decision
3. **Phase 2: OSW Completion (Items 30-49)** - Onsite Scoping Workbook data entry, external references, sign-off
4. **Phase 3: Deployment Readiness (Items 50-85)** - Server setup, accounts/permissions, vendor software, onsite readiness
5. **Phase 4: Data Collection (Items 86-120)** - DCS, PLC, safety, reliability, historian imports
6. **Phase 5: Validation & Go-Live (Items 121-148)** - SAT, training, go-live prep, post-go-live support

### Key Features
- **Continuous numbering**: Items 1-148 across all phases (no gaps, no restarting)
- **Color-coded owners**: Orange (Site), Green (Hexagon), Blue (IT/OT)
- **Prerequisites column**: References specific item numbers for task dependencies
- **Status tracking**: Empty Status and Notes columns for site teams to fill in
- **Professional formatting**: Borders, text wrapping, aligned columns, section headers

---

## Source Files

### Generation Script
**`regenerate_checklist.py`** (Python 3.13+)

**Purpose**: Complete regeneration of Excel workbook from scratch  
**Libraries**: `openpyxl` (Excel manipulation)  
**Run Command**: `C:/Users/GF99/Documentation/.venv/Scripts/python.exe Integrity/Audits/regenerate_checklist.py`

**Key Functions**:
- `create_checklist_sheet(wb, sheet_name, checklist_data, start_num=1)` - Generates formatted worksheet
  - Takes starting item number, returns next item number for continuous numbering
  - Applies color coding based on Owner field ('Site', 'Hexagon', 'IT/OT')
  - Formats borders, alignment, text wrapping
  - Sets column widths: Item#(8), Task(50), Owner(12), Status(12), Notes(30), Prerequisites(25)

**Data Structures**:
- `phaseN_data = [('Section Name', [(task, owner, prereqs), ...]), ...]`
- Each phase is a list of tuples: (section_name, list_of_items)
- Each item is a tuple: (task_description, owner, prerequisites_string)

**Color Definitions**:
```python
SITE_FILL = PatternFill(start_color='FFC000', end_color='FFC000', fill_type='solid')      # Orange
HEXAGON_FILL = PatternFill(start_color='92D050', end_color='92D050', fill_type='solid')   # Green
IT_FILL = PatternFill(start_color='00B0F0', end_color='00B0F0', fill_type='solid')        # Blue
```

### Archived Scripts (Historical)
- `add_executive_summary.py` - Earlier attempt to add summary to existing file (superseded)
- `create_enhanced_checklist.py` - First version of checklist generator (superseded)
- `fix_it_owners.py` - One-time script to update IT→IT/OT (no longer needed)

### Reference File
**`LAR Readiness Checklist Hexagon Integrity.xlsx`** - Original simple checklist that was enhanced

---

## How to Modify the Checklist

### Adding a New Task

1. Open `regenerate_checklist.py` in editor
2. Find the appropriate phase data structure (e.g., `phase3_data`)
3. Add tuple to the relevant section:
   ```python
   ('Task description here', 'Owner', 'prerequisite item numbers'),
   ```
4. Run regeneration script
5. Verify item numbers and prerequisites are correct

**Owner values**: `'Site'`, `'Hexagon'`, or `'IT/OT'`  
**Prerequisites**: Comma-separated item numbers or descriptive text like `'Phase 2'` or `'All above'`

### Changing Task Order

1. Cut/paste task tuples within the data structure
2. Regenerate - item numbers will auto-update
3. **Important**: Review and update prerequisites that reference moved items

### Updating Executive Summary

1. Find `summary_content = [...]` around line 120
2. Modify tuples: `(text, style_name)`
3. Available styles: `'header'`, `'subheader'`, `'section'`, `'subsection'`, `'normal'`, `'impact'`, `'metric'`, `'success'`, `'quote'`, `'quote_attribution'`, `'version'`

### Modifying Color Scheme

1. Change hex colors in color definitions (lines 10-13)
2. Regenerate

---

## Critical Design Decisions

### Why Continuous Numbering?
**Problem**: Original design restarted numbering on each tab (1-29, 1-20, 1-36, etc.)  
**Issue**: Prerequisites like "38" on Phase 2 were confusing - there was no item 38 on that tab  
**Solution**: Continuous numbering 1-148 across all tabs  
**Implementation**: Function returns next item number; each phase starts where previous ended

### Why IT/OT Instead of Separate IT?
**Rationale**: IT and OT teams collaborate on infrastructure tasks (servers, network, data movement)  
**Simplification**: Merged "IT" and "IT/OT" into single "IT/OT" category  
**Color**: Blue for all IT/OT tasks

### Why Section Headers Don't Get Item Numbers?
**Design**: Section headers (e.g., "1. Server & Infrastructure Setup") are visual organizers  
**Numbering**: Only actual tasks get item numbers for prerequisite referencing

---

## Data Sources & Lessons Learned

### Marathon Deployment Analysis
**Source Document**: `Hexagon Implementation 1.pdf` (extracted to audit folder)

**Key Insights**:
- **Financial**: 43.8% budget spent, 27.4% work complete → CPI 0.62
- **Scope Issues**: GBR +1,614 assets, "we were not informed about this project"
- **Delay Causes**: 60% incomplete data, 30% scope changes, 20% infrastructure gaps
- **Cost Drivers**: Rework ($900/hr), pre-work ($275/hr), deviations ($275-900/hr)
- **Success Factors**: Remote deployment saves $15K-$25K travel, complete OSW before sign-off

### Integrity System Documentation
**Sources**: INT-101 (user manual), INT-500 (admin manual), Address Reservation instructions

**Architecture**:
- **L1**: Field devices (controllers, PLCs, safety systems)
- **L2**: Site staging workstations (program backups, exports)
- **L4**: IntegrityDataCollector2 service (import processing, SQL database)
- **L5**: IIS web server (enterprise dashboard, user access)

**External References**: ControlLogix, Triconex, Bently Nevada, Relays (import vs manual entry decisions)

---

## Deployment Workflow Context

### Typical Timeline
- **Week -4 to -1**: Phase 1 Pre-Planning
- **Week 1-3**: Phase 2 OSW Completion
- **Week 4-5**: Phase 3 Deployment Readiness
- **Week 6-8**: Phase 4 Data Collection
- **Week 9-10**: Phase 5 Validation & Go-Live

### Stakeholders
- **Site Lead**: 20% FTE, 6-8 weeks (designated in item #1)
- **Process Control**: DCS data, control strategies, alarms
- **Reliability**: Vibration monitoring, equipment hierarchy
- **Electrical**: Relays, MCCs, single-line diagrams
- **IT/OT**: Servers, network, accounts, data movement
- **Hexagon PM**: Assigned during kickoff, provides import/deployment services

### Critical Handoffs
- **Pre-Planning → OSW**: L1 inventory complete, programs accessible
- **OSW → Deployment**: Scope locked (no additions), executive sign-off, budget confirmed
- **Deployment → Data Collection**: Onsite readiness 100%, L1→L4 data flow tested
- **Data Collection → Validation**: All imports complete, data quality verified
- **Validation → Go-Live**: SAT passed, training complete, support contacts established

---

## Python Environment

### Setup
```bash
cd c:/Users/GF99/Documentation
python -m venv .venv
.venv\Scripts\activate
pip install openpyxl
```

### Run Script
```bash
C:/Users/GF99/Documentation/.venv/Scripts/python.exe Integrity/Audits/regenerate_checklist.py
```

### Dependencies
- **Python**: 3.13.4 (or 3.10+)
- **openpyxl**: 3.1.5+ (Excel file manipulation)
- **Virtual environment**: `.venv` in Documentation root

---

## Git Repository

### Commit History
**Initial commit**: `e09b2bb` (January 16, 2026)
- 6 files added: Excel workbook, Python scripts, reference checklist
- 1,038 insertions

### File Locations
```
Integrity/
  Audits/
    Enhanced_Integrity_Deployment_Readiness_Checklist.xlsx  # Deliverable
    regenerate_checklist.py                                  # Active generator
    LAR Readiness Checklist Hexagon Integrity.xlsx          # Original reference
    add_executive_summary.py                                 # Archived
    create_enhanced_checklist.py                             # Archived
    fix_it_owners.py                                         # Archived
    HANDOFF_SUMMARY.md                                       # This file
```

---

## Known Issues & Limitations

### None Currently
All identified issues have been resolved:
- ✅ Continuous numbering implemented (no gaps)
- ✅ IT/OT consolidation complete (no white boxes)
- ✅ Marathon contacts added (Keith Mazy, Don Clark)
- ✅ Prerequisites use absolute item numbers across all phases

### Future Enhancements (Optional)
- **Hyperlinks**: Add hyperlinks in Prerequisites column to jump to referenced items
- **Conditional Formatting**: Status column could use data validation dropdown (Not Started, In Progress, Complete, Blocked)
- **Progress Tracking**: Add summary sheet with phase completion percentages
- **Site-Specific Versions**: Clone script to generate site-specific checklists with pre-filled data

---

## Testing & Validation

### Manual Verification Checklist
- [ ] Excel file opens without errors
- [ ] All 148 items numbered sequentially (no gaps: 1, 2, 3... 146, 147, 148)
- [ ] Color coding: Orange (Site), Green (Hexagon), Blue (IT/OT) - no white boxes
- [ ] Prerequisites reference valid item numbers
- [ ] Executive Summary displays correctly with formatting
- [ ] All section headers visible and properly merged
- [ ] Column widths appropriate for content
- [ ] Text wrapping enabled where needed

### Regeneration Test
```bash
# Backup current file
copy Enhanced_Integrity_Deployment_Readiness_Checklist.xlsx Enhanced_Integrity_Deployment_Readiness_Checklist_backup.xlsx

# Regenerate
C:/Users/GF99/Documentation/.venv/Scripts/python.exe Integrity/Audits/regenerate_checklist.py

# Compare file sizes (should be similar)
dir Enhanced_Integrity_Deployment_Readiness_Checklist*.xlsx

# Open and verify manually
```

---

## AI Agent Prompt Template

When asking an AI agent to modify this checklist, use this template:

```
Context: I have an Enhanced Integrity Deployment Readiness Checklist for Hexagon Integrity deployments at Marathon Petroleum sites. The checklist is generated from a Python script (regenerate_checklist.py) using openpyxl.

Current structure:
- 148 items across 5 phases with continuous numbering (1-148)
- Color-coded owners: Orange (Site), Green (Hexagon), Blue (IT/OT)
- Prerequisites column references specific item numbers

Task: [Your modification request here]

Examples:
- "Add a new task to Phase 3 for testing SQL backup jobs"
- "Update the Executive Summary with new financial data"
- "Change the order of items in Phase 2"
- "Add a new section to Phase 4 for analyzer configuration"

Files to read:
1. Integrity/Audits/HANDOFF_SUMMARY.md (this file)
2. Integrity/Audits/regenerate_checklist.py (generator script)

After making changes, regenerate the Excel file and verify item numbers are continuous.
```

---

## Contact Information

### Marathon Petroleum
- **Primary Contacts**: Keith Mazy, Don Clark
- **Email**: lar-integrityrequests@marathonpetroleum.com
- **Purpose**: Integrity project requests, site coordination, deployment issues

### Hexagon
- **PM Assignment**: Assigned during project kickoff
- **Role**: Import processing, data collection support, training, go-live assistance

### Corporate IT
- **Team**: Infrastructure team
- **Role**: Server provisioning, network architecture, accounts/permissions, data movement setup

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2026-01-16 | Initial creation with 148 items, tab-relative prerequisites | AI Agent |
| 1.1 | 2026-01-16 | IT/OT consolidation, Marathon contacts added | AI Agent |
| 1.2 | 2026-01-16 | Continuous numbering (1-148) implemented | AI Agent |
| 2.0 | 2026-01-20 | Handoff summary created for knowledge preservation | AI Agent |

---

## References

### Microsoft Documentation
- Dataverse SDK for Python: https://learn.microsoft.com/en-us/power-apps/developer/data-platform/sdk-python/
- Hexagon Integrity: PTC/Hexagon asset management platform (v5.x)

### Internal Documentation
- INT-101: Integrity User Manual (84 pages, basic operations)
- INT-500: Integrity Administrator Manual (61 pages, database/imports)
- Hexagon Implementation 1.pdf: Marathon deployment status (GBR, ROB, LAR, SPP lessons learned)
- Integrity Reference and Connections Examples.docx: External reference configurations

### Project Context
This checklist was created after reviewing all Marathon Integrity deployment documentation and extracting lessons learned from real-world implementations. The goal is to provide new sites with a proven roadmap to avoid the costly mistakes encountered at earlier deployments.

---

**End of Handoff Summary**

*This document should be updated whenever significant changes are made to the checklist structure or generation process.*
