# SAP Control Systems Equipment Master Data - Project Handoff

> **Purpose**: This document is for AI assistants continuing work on this project.
> **For human-friendly docs**: See `README.md`

**Last Updated:** January 30, 2026  
**Project Owner:** Tony Chiu  
**Status:** Planning Phase Complete - Ready for Stakeholder Review  
**Version:** 1.1

---

## Executive Summary

This project implements SAP Equipment Master Data for 382+ control systems across Marathon Petroleum LAR (Los Angeles Refinery) sites. The functional location structure separates control systems from physical plant locations, creating a logical hierarchy for DCS, PLC, SIS, VMS, TCS, NET, and AUX systems.

**Key Metrics:**
- **Equipment Records:** 3,000-5,700 estimated
- **Control Systems:** 382+ (from Asset Hierarchy analysis)
- **Implementation Time:** 20-30 weeks
- **Estimated Cost:** $233k (LSMW) to $329k (manual)
- **Recommended Approach:** LSMW (saves $97k, 10-16 weeks faster)

---

## Project Objectives

1. Create SAP functional location structure for control systems independent of physical locations
2. Define equipment categories and classification characteristics for all system types
3. Import existing control system equipment into SAP from Asset Hierarchy data
4. Enable preventive maintenance, work orders, and spare parts management in SAP PM module
5. Establish governance for ongoing maintenance and updates

---

## Deliverables Status

### ✅ Complete - Ready for Review

1. **Control_Systems_Functional_Location_Structure.md**
   - 7 system types defined: DCS, PLC, SIS, VMS, TCS, NET, AUX
   - 30+ equipment categories following CTRL-[SYSTEM]-[TYPE] pattern
   - Classification characteristics identified for each category
   - Formatted with page breaks for PDF conversion
   - Location: `SAP/Control_Systems_Functional_Location_Structure.md`

2. **Control_Systems_Implementation_Resource_Estimate_REVISED.md**
   - 5-phase implementation plan (1,660 hours / 1,092 hours with LSMW)
   - Cost analysis: Manual ($329k) vs LSMW ($233k)
   - Equipment count breakdown by site
   - Staffing plan (2-3 FTE peak)
   - LSMW explanation and benefits
   - Formatted with page breaks for PDF conversion
   - Location: `SAP/Control_Systems_Implementation_Resource_Estimate_REVISED.md`

3. **Control_Systems_Functional_Location_Implementation_Checklist.md**
   - 7-section validation checklist
   - Covers structure, categories, data quality, documentation, maintenance integration, upload, governance
   - Location: `SAP/Control_Systems_Functional_Location_Implementation_Checklist.md`

### 📊 Source Data

**15.-Assets-Hierarchy.xlsx**
- Contains 382+ control systems across LAR sites
- Multiple sheets: Assets, Look Table, Selections
- Drives equipment count estimates (3,000-5,700 records)
- **Critical:** Must validate accuracy before Phase 3 data upload
- Location: `SAP/15.-Assets-Hierarchy.xlsx`

---

## Technical Architecture

### Functional Location Hierarchy

```
[SITE]-16 (Top Level: "A16 Control Systems")
├── [SITE]-16-DCS (DCS Systems)
├── [SITE]-16-PLC (PLC Systems)
├── [SITE]-16-SIS (Safety Instrumented Systems)
├── [SITE]-16-VMS (Vibration Monitoring Systems)
├── [SITE]-16-TCS (Turbomachinery Control Systems)
├── [SITE]-16-NET (Network Infrastructure)
└── [SITE]-16-AUX (Auxiliary Systems)
```

**Sites:**
- **LA-C** (Carson) - 40% of equipment (~1,200-2,250 records)
- **LA-L** (Logistics) - 21% of equipment (~630-1,197 records)
- **LA-W** (Wilmington) - 26% of equipment (~780-1,482 records)
- **WC** (Watson Cogen) - 13% of equipment (~390-741 records)

### System Types & Equipment Breakdown

| System Type | Description | Equipment per System | Key Vendors/Examples |
|-------------|-------------|---------------------|----------------------|
| DCS | Distributed Control System | 15-25 items | Honeywell EPKS, APC |
| PLC | Programmable Logic Controller | 8-12 items | Allen-Bradley ControlLogix |
| SIS | Safety Instrumented System | 10-15 items | Triconex, Honeywell Safety Manager |
| VMS | Vibration Monitoring System | 5-8 items | Bently Nevada |
| TCS | Turbomachinery Control System | 5-8 items | GE Mark VIe, Woodward GAP |
| NET | Network Infrastructure | 6-10 items | Switches, routers, firewalls |
| AUX | Auxiliary Systems | 3-5 items | UPS, racks, PDUs |

### Equipment Categories (Examples)

**DCS:** CTRL-DCS-CTL (Controllers), CTRL-DCS-IOM (I/O Modules), CTRL-DCS-OWS (Operator Workstations), CTRL-DCS-SRV (Servers), CTRL-DCS-NET (Network Equipment)

**PLC:** CTRL-PLC-CPU (Processors), CTRL-PLC-IO (I/O Modules), CTRL-PLC-PSU (Power Supplies), CTRL-PLC-COM (Communication Modules)

**SIS:** CTRL-SIS-CTL (Logic Solvers), CTRL-SIS-IO (Safety I/O), CTRL-SIS-OWS (Engineering Stations), CTRL-SIS-PSU (Power Supplies)

*(See Control_Systems_Functional_Location_Structure.md for complete list)*

---

## Key Technical Decisions

### 1. Separate Functional Location Hierarchy
**Decision:** Create control systems hierarchy separate from physical plant locations (LA-C, LA-L, LA-W, WC)  
**Rationale:** Control systems often span multiple process units or serve plant-wide functions. Logical hierarchy supports better reporting and maintenance planning.  
**Impact:** Requires clear governance for when to use physical vs control system hierarchy.

### 2. LSMW vs Manual Entry
**Decision:** **STRONGLY RECOMMEND LSMW** for Phase 3 (Equipment Master Data)  
**Rationale:** 
- 3,000-5,700 records too large for manual entry (15-25 min/record = 1,322 hours)
- LSMW reduces to 492 hours (6× faster)
- Saves $97k in labor costs
- Reduces data entry errors through validation rules
- Standard SAP tool with industry-proven success

**Impact:** Requires SAP Technical Consultant hire (included in resource estimate)

### 3. System Type Exclusions
**Decision:** Focus on 7 system types actually installed at LAR  
**Excluded Systems:** Symphony DCS, DeltaV DCS, Siemens S7 PLC (not present at LAR)  
**Rationale:** Documentation must reflect actual installed base, not industry-wide possibilities.

### 4. APC Integration
**Decision:** Merge APC (Advanced Process Control) into DCS category  
**Rationale:** APC applications run on DCS infrastructure (Honeywell EPKS), share same equipment (controllers, I/O, workstations). Separate category would cause confusion.

---

## Implementation Phases

### Phase 1: Planning & Configuration (140 hours, 3-4 weeks)
- Validate functional location structure with stakeholders
- Configure SAP SPRO (equipment categories, classification system, number ranges)
- Define data collection templates
- **Deliverable:** Configured SAP DEV environment

### Phase 2: Functional Location Creation (120 hours, 2-3 weeks)
- Create top-level functional locations ([SITE]-16) in SAP
- Create system-type sub-levels (DCS, PLC, SIS, VMS, TCS, NET, AUX)
- Configure authorization roles
- **Deliverable:** Complete functional location structure in SAP

### Phase 3: Equipment Master Data (492 hours with LSMW, 4-6 weeks)
- **CRITICAL:** Validate Asset Hierarchy data accuracy
- Hire SAP Technical Consultant for LSMW development
- Map Asset Hierarchy data to SAP equipment master format
- Configure LSMW project (mappings, validations, error handling)
- **Pilot:** Upload LA-C equipment (1,200-2,250 records), validate 10% sample
- **Rollout:** LA-W → LA-L → WC sequential uploads
- **Deliverable:** 3,000-5,700 equipment master records in SAP Production

### Phase 4: Testing & Validation (140 hours, 2-3 weeks)
- Validate equipment records against Asset Hierarchy
- Test classification system queries
- Verify preventive maintenance plan linkages
- Test work order creation for control system equipment
- **Deliverable:** Test results and sign-off

### Phase 5: Training & Go-Live (200 hours, 1-2 weeks)
- Train maintenance planners on equipment search and work orders
- Train controls engineers on equipment creation and updates
- Document ongoing governance processes
- **Deliverable:** Trained users and production go-live

---

## Critical Dependencies

### Data Sources
1. **15.-Assets-Hierarchy.xlsx** - Source of truth for existing control systems
   - **Risk:** Data may be incomplete or outdated
   - **Mitigation:** Phase 1 validation with site controls engineers

2. **Site Controls Engineers** - Domain experts for equipment details
   - LA-C, LA-L, LA-W, WC controls teams must review and approve
   - Required for data validation and testing

3. **SAP Administrator** - Technical configuration and authorization
   - SPRO configuration in Phase 1
   - LSMW authorization and production access
   - User role configuration

### External Resources
1. **SAP Technical Consultant** - LSMW development (if recommended approach selected)
   - Estimated 6-8 weeks, $15k-$20k
   - Required for Phase 3 if LSMW approach chosen

---

## Risks & Mitigation

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Asset Hierarchy data incomplete/inaccurate | High | Medium | Phase 1 validation with site engineers |
| Manual entry chosen over LSMW | High (cost/time) | Low | Resource estimate clearly shows LSMW benefits |
| SAP authorizations delayed | Medium | Medium | Request access in Phase 1, escalate if needed |
| Stakeholder disagreement on structure | Medium | Low | Early review in Phase 1, checklist validation |
| LSMW consultant unavailable | Medium | Low | Identify backup consultants, plan 2-week buffer |
| Pilot data quality issues | Medium | Medium | 10% sample validation, correction process before rollout |

---

## Success Criteria

1. ✅ All 382+ control systems from Asset Hierarchy imported into SAP
2. ✅ Equipment records searchable by system type, site, classification characteristics
3. ✅ Preventive maintenance plans linked to control system equipment
4. ✅ Work orders can be created against control system functional locations
5. ✅ <2% error rate in final data validation
6. ✅ Training completed for 15+ maintenance planners and controls engineers
7. ✅ Governance process documented and approved

---

## Next Actions

### Immediate (Weeks 1-2)
1. **Stakeholder Review:** Distribute Control_Systems_Functional_Location_Structure.md and Resource_Estimate_REVISED.md to:
   - LA-C/LA-L/LA-W/WC Controls Supervisors
   - SAP Administrator
   - Maintenance Planning Manager
   - Request feedback by [DATE + 2 weeks]

2. **Management Approval:** Present resource estimate to management
   - Emphasize LSMW cost savings ($97k)
   - Request budget approval for SAP Technical Consultant

3. **Asset Hierarchy Validation:** Assign controls engineer from each site to:
   - Review Asset Hierarchy data for their site
   - Identify missing/incorrect systems
   - Provide corrections by [DATE + 3 weeks]

### Phase 1 Kickoff (Week 3)
1. Schedule kickoff meeting with stakeholders
2. Request SAP DEV environment access for configuration
3. Begin SPRO configuration (equipment categories, classification system)

---

## File Locations

```
SAP/
├── Control_Systems_Functional_Location_Structure.md (FINAL - PDF Ready)
├── Control_Systems_Implementation_Resource_Estimate_REVISED.md (FINAL - PDF Ready)
├── Control_Systems_Functional_Location_Implementation_Checklist.md (FINAL)
├── 15.-Assets-Hierarchy.xlsx (Source Data - Requires Validation)
├── HANDOFF.md (This Document)
├── README.md (Human-friendly overview)
├── _TODO.md (Tasks and ideas)
└── [Additional Excel files with functional location designs]
```

---

## Contact Information

**Project Owner:** Tony Chiu  
**Role:** Controls Engineer, Marathon Petroleum LAR  
**Responsibilities:** Functional location design, stakeholder coordination, implementation oversight

**Key Stakeholders:**
- **Controls Supervisors** (LA-C, LA-L, LA-W, WC) - Data validation, testing
- **SAP Administrator** - Technical configuration, LSMW support, production access
- **Maintenance Planning Manager** - PM plan integration, work order processes
- **SAP Technical Consultant** (TBD) - LSMW development if selected

---

## Agent Continuation Instructions

### Context Preservation
If resuming this project with a new agent or after time gap:

1. **Read in this order:**
   - This handoff document (overview)
   - Control_Systems_Functional_Location_Structure.md (technical details)
   - Control_Systems_Implementation_Resource_Estimate_REVISED.md (implementation plan)
   - 15.-Assets-Hierarchy.xlsx (source data - use Python/pandas to analyze)

2. **Critical knowledge to preserve:**
   - 382+ control systems drive 3,000-5,700 equipment records estimate
   - LSMW is **MANDATORY** given scale (manual not viable)
   - Functional location structure: [SITE]-16 → [SITE]-16-[SYSTEM] (7 types)
   - Equipment categories follow CTRL-[SYSTEM]-[TYPE] pattern
   - Tony Chiu is author/owner of all documents
   - Documents formatted with page breaks for PDF conversion

3. **Do NOT:**
   - Suggest returning to generic "Controls Systems Team" authorship
   - Recommend manual entry for Phase 3 (scale requires LSMW)
   - Add vendor examples not present at LAR (no Symphony, DeltaV, S7)
   - Create separate APC category (merged into DCS)

### Common User Requests
- **"Update resource estimate"** → Reanalyze 15.-Assets-Hierarchy.xlsx, adjust Phase 3 hours
- **"Add new system type"** → Update all 3 documents + checklist consistently
- **"Create data templates"** → Excel templates with Asset Hierarchy cross-reference
- **"PDF formatting"** → Add `<div style="page-break-after: always;"></div>` before major sections
- **"LSMW development plan"** → Reference Phase 3 section, recommend SAP Technical Consultant

### Technical Tools Available
- **Python Environment:** `.venv` activated, pandas/openpyxl installed
- **Excel Analysis:** Use pandas to read 15.-Assets-Hierarchy.xlsx sheets
- **Document Skills:** DOCX, XLSX, PDF, PPTX skills available in `.github/skills/`
- **SAP Instructions:** dataverse-python-*.instructions.md (though this is SAP ECC/PM, not Dataverse)

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | January 20, 2026 | Tony Chiu | Initial project handoff |
| 1.1 | January 30, 2026 | System | Consolidated PROJECT_HANDOFF.md into HANDOFF.md per workspace standards |

---

**End of Handoff Document**
