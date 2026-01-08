# Control Systems SAP Implementation - Resource & Hours Estimate
## Functional Location Structure & Equipment Master Data Setup

---

## Executive Summary

| **Metric** | **Estimate** |
|------------|--------------|
| **Total Project Duration** | 12-16 weeks |
| **Total Labor Hours** | 520-720 hours |
| **FTE Required** | 1.5-2.0 FTE (peak) |
| **Sites Covered** | 4 sites (LA-C, LA-L, LA-W, WC) |
| **Equipment Records (Est.)** | 800-1,500 equipment masters |

---

## Phase 1: Planning & Configuration (3-4 weeks)

### 1.1 Structure Validation & Stakeholder Review
**Duration:** 1 week  
**Effort:** 40 hours  
**Resources:** 1 Controls Engineer, 1 SAP Admin

| Task | Hours | Description |
|------|-------|-------------|
| Review functional location structure with site stakeholders | 8 | Validate LA-C-16 structure applies to all sites |
| Confirm equipment category definitions | 8 | Review 30+ equipment categories with controls team |
| Identify site-specific variations | 4 | Document any site differences (WC, LA-L logistics) |
| Define naming conventions for equipment numbers | 6 | Standardize equipment numbering scheme |
| Obtain SAP authorization/access for team | 4 | Coordinate with IT/SAP admin |
| Document approval and sign-off | 10 | Create formal design document with approvals |

**Deliverables:**
- Approved functional location design document
- Equipment category definitions
- Naming convention standards
- Authorization matrix

---

### 1.2 SAP Configuration (SPRO)
**Duration:** 1.5 weeks  
**Effort:** 60 hours  
**Resources:** 1 SAP Functional Consultant (or trained SAP Admin)

| Task | Hours | Description |
|------|-------|-------------|
| Configure functional location structure types | 6 | Set up structure levels, labeling, masks |
| Create equipment categories (30+ categories) | 12 | Define categories in SPRO with field selection |
| Configure field selection per category | 8 | Determine required/optional fields for each category |
| Set up authorization groups | 4 | Restrict access to Controls group |
| Configure number ranges | 4 | Equipment numbers, functional location numbers |
| Create planner groups | 4 | Map to Controls team members |
| Define maintenance planning parameters | 6 | Planning plant, work centers, maintenance strategies |
| User acceptance testing in DEV environment | 12 | Test create/change/display transactions |
| Document configuration settings | 4 | Screenshot and document all settings |

**Deliverables:**
- Configured SPRO settings (DEV environment)
- Equipment categories active in system
- Test functional locations created
- Configuration documentation

---

### 1.3 Classification System Setup
**Duration:** 1 week  
**Effort:** 40 hours  
**Resources:** 1 SAP Admin, 1 Controls Engineer

| Task | Hours | Description |
|------|-------|-------------|
| Define characteristic catalog | 12 | System ID, Process Unit, Cabinet Location, IP Address, etc. |
| Create class types for equipment | 8 | Define classes for DCS, PLC, SIS, NET, AUX |
| Assign characteristics to classes | 6 | Map 15-20 characteristics per class |
| Set up value lists/domains | 6 | Dropdown values (SIS-1, SIS-2, etc.) |
| Test classification assignment | 4 | Create test equipment and assign classifications |
| Document classification structure | 4 | Reference guide for data entry users |

**Deliverables:**
- Classification characteristics (CT04)
- Class definitions with assignments
- Value lists for controlled fields
- Classification user guide

---

## Phase 2: Functional Location Creation (2-3 weeks)

### 2.1 Functional Location Master Data Creation
**Duration:** 2 weeks  
**Effort:** 80 hours  
**Resources:** 1 Controls Data Specialist

| Task | Hours | Site/Count | Description |
|------|-------|------------|-------------|
| Create top-level functional locations | 4 | 4 sites × 1 location | LA-C-16, LA-L-16, LA-W-16, WC-16 |
| Create second-level functional locations | 12 | 4 sites × 5 systems | -DCS, -PLC, -SIS, -NET, -AUX per site |
| Add descriptions and attributes | 8 | 24 total locations | Planning plant, cost center, planner group |
| Test functional location hierarchy | 4 | All sites | Verify display, navigation, authorization |
| Validate with site personnel | 8 | Remote meetings | Confirm structure with site controls teams |
| Create functional location documentation | 8 | Reference guide | IL03 screenshots, hierarchy tree |

**Transaction Codes Used:** IL01 (Create), IL02 (Change), IL03 (Display)

**Deliverables:**
- 24 functional locations across 4 sites
- Functional location hierarchy report
- Site validation sign-off
- Reference guide

---

### 2.2 Data Collection Templates
**Duration:** 1 week  
**Effort:** 40 hours  
**Resources:** 1 Controls Engineer, 1 Business Analyst

| Task | Hours | Description |
|------|-------|-------------|
| Create Excel data collection templates | 12 | One template per system type (DCS, PLC, SIS, etc.) |
| Define required fields and validations | 8 | Mandatory fields, dropdown lists, data validation |
| Distribute templates to sites | 4 | Email/SharePoint distribution with instructions |
| Conduct training session for data collectors | 8 | 1-hour training × 4 sites |
| Provide template support and Q&A | 8 | Ongoing support during data collection period |

**Template Fields:**
- Equipment description
- Manufacturer
- Model/Part number
- Serial number
- Installation date
- Location (cabinet/rack)
- System assignment
- Process unit
- IP address (if applicable)
- Asset tag

**Deliverables:**
- Excel data collection templates (5 templates)
- Training materials
- Completed templates from sites (input for Phase 3)

---

## Phase 3: Equipment Master Data Creation (4-6 weeks)

### 3.1 Pilot Site Equipment Data Entry (LA-C)
**Duration:** 2 weeks  
**Effort:** 120 hours  
**Resources:** 1 Controls Data Specialist, 1 SAP Admin (support)

**Estimated Equipment Count - LA-C:** 300-400 equipment records

| System | Equipment Count | Hours | Notes |
|--------|----------------|-------|-------|
| DCS | 100-120 | 40 | Controllers, I/O, workstations, servers |
| PLC | 80-100 | 32 | Multiple PLC systems across units |
| SIS | 40-60 | 20 | FSC controllers, safety I/O |
| NET | 30-40 | 12 | Switches, routers, firewalls |
| AUX | 50-80 | 16 | UPS, racks, PDUs |
| **Total** | **300-400** | **120** | **Includes classification assignment** |

**Per-Equipment Effort:** ~15-20 minutes per equipment record (IK01 + classification)

**Activities:**
- Create equipment master records (IK01)
- Assign to functional locations
- Enter manufacturer, model, serial data
- Assign classifications with characteristics
- Add technical identifications (asset tags)
- Quality review and validation

**Deliverables:**
- 300-400 equipment records at LA-C
- Lessons learned document
- Refined process for remaining sites

---

### 3.2 Remaining Sites Equipment Data Entry
**Duration:** 3 weeks  
**Effort:** 240 hours  
**Resources:** 2 Controls Data Specialists (parallel effort)

**Estimated Equipment Count:**

| Site | DCS | PLC | SIS | NET | AUX | **Total** | Hours |
|------|-----|-----|-----|-----|-----|-----------|-------|
| LA-L | 60 | 40 | 20 | 20 | 40 | **180** | 60 |
| LA-W | 80 | 60 | 30 | 25 | 50 | **245** | 80 |
| WC | 50 | 40 | 25 | 20 | 35 | **170** | 55 |
| **Subtotal** | **190** | **140** | **75** | **65** | **125** | **595** | **195** |

**Additional Activities:** (45 hours)
- Cross-site data validation | 15 hours
- Equipment duplicate check | 10 hours
- Data quality audits | 10 hours
- Rework and corrections | 10 hours

**Total Phase 3.2 Effort:** 240 hours

**Deliverables:**
- 595 equipment records across LA-L, LA-W, WC
- Data quality audit report
- Complete equipment inventory

---

### 3.3 Mass Data Upload (Optional Alternative)
**Duration:** 2 weeks  
**Effort:** 80 hours (replaces 3.1 + 3.2 if used)  
**Resources:** 1 SAP Technical Consultant, 1 Controls Engineer

| Task | Hours | Description |
|------|-------|-------------|
| Prepare LSMW or BAPI upload program | 24 | Configure Legacy System Migration Workbench |
| Data cleansing and formatting | 16 | Standardize data from collection templates |
| Test upload in DEV environment | 12 | Upload 50 test records and validate |
| Production upload execution | 8 | Upload all equipment records |
| Post-upload validation and corrections | 12 | Review error logs, fix data issues |
| Classification mass assignment | 8 | Batch assign classifications if not in initial load |

**Note:** Mass upload is faster but requires more technical expertise. Manual entry provides better data quality control for initial implementation.

**Deliverables:**
- LSMW upload program
- Complete equipment inventory (all sites)
- Upload validation report

---

## Phase 4: Testing & Validation (2 weeks)

### 4.1 System Integration Testing
**Duration:** 1 week  
**Effort:** 40 hours  
**Resources:** 1 Controls Engineer, 1 SAP Admin

| Task | Hours | Description |
|------|-------|-------------|
| Equipment master data query testing | 8 | IK03, IH08, reports |
| Functional location navigation | 4 | Hierarchy display, drill-down |
| Work order creation against equipment | 8 | IW31 - test PM notifications and orders |
| Maintenance plan creation | 8 | IP01 - test preventive maintenance |
| Spare parts BOM linkage | 4 | CS02 - associate parts to equipment |
| Report generation and validation | 8 | Equipment lists, location lists, classification reports |

**Deliverables:**
- Test scripts
- Test results log
- Issue tracking and resolution

---

### 4.2 User Acceptance Testing (UAT)
**Duration:** 1 week  
**Effort:** 40 hours  
**Resources:** 4 Site Controls Engineers (10 hours each)

| Task | Hours per Site | Description |
|------|----------------|-------------|
| Review site equipment inventory | 4 | Validate accuracy and completeness |
| Test equipment search and display | 2 | Find equipment by various criteria |
| Create test work orders | 2 | Practice PM01, IW31 transactions |
| Provide feedback and corrections | 2 | Document issues or missing data |

**Deliverables:**
- UAT sign-off from all sites
- Defect log and resolution plan
- User feedback summary

---

## Phase 5: Training & Go-Live (1-2 weeks)

### 5.1 End-User Training
**Duration:** 1 week  
**Effort:** 60 hours  
**Resources:** 1 SAP Trainer, 1 Controls SME

| Task | Hours | Audience | Description |
|------|-------|----------|-------------|
| Develop training materials | 16 | N/A | User guides, quick reference cards, job aids |
| Equipment creation training | 12 | Data specialists | IK01, classification, best practices |
| Equipment search and display | 8 | All controls staff | IK03, IH08, equipment lists |
| Work order integration training | 12 | Planners/engineers | Link equipment to PM notifications, orders |
| Maintenance planning training | 8 | Maintenance planners | IP01, maintenance strategies |
| Q&A and support | 4 | All users | Open forum for questions |

**Training Delivery:**
- 2-hour sessions per topic
- Hands-on practice in training environment
- Recorded sessions for future reference

**Deliverables:**
- Training materials (guides, videos)
- Training attendance records
- Post-training assessment

---

### 5.2 Go-Live Support
**Duration:** 1 week  
**Effort:** 80 hours (hypercare period)  
**Resources:** 2 Support Staff (1 Controls, 1 SAP)

| Task | Hours | Description |
|------|-------|-------------|
| On-call support for user questions | 40 | Help desk coverage during business hours |
| Troubleshooting and issue resolution | 20 | Address data errors, system issues |
| Monitor system performance | 8 | Check for slowness, errors, job failures |
| Collect user feedback | 4 | Survey users on experience and pain points |
| Document lessons learned | 8 | Capture improvements for future rollouts |

**Deliverables:**
- Issue log and resolution report
- User feedback summary
- Lessons learned document

---

## Resource Summary by Phase

| Phase | Duration | Effort (Hours) | Peak FTE |
|-------|----------|----------------|----------|
| **Phase 1: Planning & Configuration** | 3-4 weeks | 140 | 1.5 |
| **Phase 2: Functional Location Creation** | 2-3 weeks | 120 | 1.0 |
| **Phase 3: Equipment Master Data** | 4-6 weeks | 360 | 2.0 |
| **Phase 4: Testing & Validation** | 2 weeks | 80 | 1.0 |
| **Phase 5: Training & Go-Live** | 1-2 weeks | 140 | 1.5 |
| **Total** | **12-16 weeks** | **840 hours** | **2.0 (peak)** |

**Note:** Hours assume manual data entry. Mass upload (LSMW) can reduce Phase 3 from 360 hours to ~80 hours.

---

## Staffing Plan

### Core Team Roles

| Role | Responsibility | Time Commitment | Duration |
|------|---------------|-----------------|----------|
| **SAP Functional Consultant** | SPRO configuration, classification setup | 50% FTE | Weeks 1-6 |
| **Controls Data Specialist** | Equipment data entry, validation | 100% FTE | Weeks 5-12 |
| **Controls Engineer/SME** | Structure design, stakeholder engagement, testing | 30% FTE | Weeks 1-16 |
| **SAP Technical Consultant** | Mass upload programming (if used) | 50% FTE | Weeks 7-8 |
| **Business Analyst** | Templates, training materials, documentation | 25% FTE | Weeks 3-14 |
| **SAP Trainer** | End-user training delivery | 50% FTE | Weeks 13-14 |

### Site Support (Part-Time)

| Site | Role | Hours | When |
|------|------|-------|------|
| LA-C | Controls Engineer | 40 | Weeks 3-4 (data collection), Week 15 (UAT) |
| LA-L | Controls Engineer | 30 | Weeks 3-4 (data collection), Week 15 (UAT) |
| LA-W | Controls Engineer | 40 | Weeks 3-4 (data collection), Week 15 (UAT) |
| WC | Controls Engineer | 30 | Weeks 3-4 (data collection), Week 15 (UAT) |

---

## Cost Estimate (Labor Only)

### Internal Labor

| Role | Hourly Rate | Hours | Cost |
|------|-------------|-------|------|
| SAP Functional Consultant | $150 | 100 | $15,000 |
| Controls Data Specialist | $85 | 360 | $30,600 |
| Controls Engineer/SME | $95 | 120 | $11,400 |
| Business Analyst | $90 | 80 | $7,200 |
| SAP Trainer | $100 | 60 | $6,000 |
| Site Controls Engineers (4 sites) | $95 | 140 | $13,300 |
| **Subtotal Internal** | | **860** | **$83,500** |

### External Consulting (if needed)

| Service | Rate | Hours | Cost |
|---------|------|-------|------|
| SAP Technical Consultant (LSMW) | $175 | 80 | $14,000 |
| Project Manager (oversight) | $135 | 100 | $13,500 |
| **Subtotal External** | | **180** | **$27,500** |

### **Total Estimated Cost: $83,500 - $111,000**

(Depending on use of external resources and mass upload approach)

---

## Risk Assessment & Mitigation

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| **Incomplete site data** | High | Medium | Early data collection, clear templates, ongoing support |
| **SAP authorization delays** | Medium | Medium | Request access in Phase 1, escalate to IT management |
| **Equipment count underestimated** | High | Medium | Buffer 20% in schedule, prioritize critical equipment |
| **Staff availability conflicts** | Medium | High | Cross-train multiple data specialists, flexible scheduling |
| **Configuration errors in production** | High | Low | Thorough DEV/QA testing, peer review before PROD |
| **User adoption resistance** | Medium | Medium | Comprehensive training, show value (PM integration) |
| **Data quality issues** | High | Medium | Validation checkpoints, quality audits, site reviews |

---

## Success Metrics

| Metric | Target | How Measured |
|--------|--------|--------------|
| **Equipment records created** | 1,000+ across 4 sites | Count in IK03 by functional location |
| **Data accuracy** | >95% | Sample audit of 100 records |
| **Functional locations created** | 24 (4 sites × 6 locations) | Count in IL03 |
| **User training completion** | 100% of controls staff | Training attendance records |
| **Go-live issue count** | <10 critical issues | Issue tracking log |
| **User satisfaction** | >80% positive feedback | Post-implementation survey |
| **Work orders linked to equipment** | >50 within first month | PM01/IW31 transaction count |

---

## Assumptions

1. **SAP ECC or S/4HANA is already implemented** at Marathon Petroleum
2. **Basic PM module is configured** (work orders, notifications functional)
3. **Network connectivity** available at all sites for remote work
4. **Data collection templates** will be completed by site personnel within 3 weeks
5. **SAP authorizations** can be obtained within 1 week of request
6. **Equipment count estimate:** 800-1,500 total records across 4 sites
7. **No major scope changes** during implementation
8. **DEV/QA environments available** for testing before production

---

## Dependencies

1. **SAP system availability** - DEV, QA, PROD environments accessible
2. **Site stakeholder engagement** - Controls engineers available for data collection and validation
3. **SAP BASIS team support** - For authorizations, transports, system issues
4. **IT infrastructure** - Network access, Excel/data tools available
5. **Management approval** - Functional location structure approved before configuration
6. **Budget approval** - Funding for consulting resources (if needed)

---

## Recommended Approach: Phased Rollout

### Option 1: Pilot Then Scale (Recommended)
1. **Pilot at LA-C** (largest site, most complex)
2. **Refine process based on lessons learned**
3. **Roll out to remaining 3 sites in parallel**
4. **Advantages:** Lower risk, better process refinement, manageable scope

### Option 2: Big Bang (All Sites at Once)
1. **Configure all sites simultaneously**
2. **Parallel data entry across all locations**
3. **Single go-live date**
4. **Advantages:** Faster overall completion, consistent rollout
5. **Disadvantages:** Higher risk, resource-intensive, less flexibility

**Recommendation:** Use Option 1 (Phased Rollout) for better risk management and quality control.

---

## Next Steps

1. ☐ **Review and approve this estimate** with management
2. ☐ **Secure budget and resources** (staff allocation, external consultants)
3. ☐ **Kick off Phase 1** - Planning & Configuration
4. ☐ **Schedule stakeholder meetings** for functional location validation
5. ☐ **Request SAP authorizations** for project team
6. ☐ **Identify site data collection leads** at LA-C, LA-L, LA-W, WC
7. ☐ **Set up project tracking** (MS Project, SharePoint, or similar)

---

**Document Version:** 1.0  
**Date:** January 8, 2026  
**Prepared By:** Controls Systems Team & SAP Implementation Team  
**Sites:** LA-C, LA-L, LA-W, WC  
**Estimated Duration:** 12-16 weeks  
**Estimated Effort:** 840 hours (520-720 core team + 140 site support)
