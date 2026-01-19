# ACM to APO Migration: A Practitioner's Guide to Alarm Database Migration Excellence

**Working Outline - Draft for Review**

**Authors:** Tony Chiu, Subject Matter Expert, Alarm Management
**Contributors:** Barbara Schubert, Marathon Petroleum Corporation
**Date:** January 2026
**Status:** Outline Development

---

## Document Purpose

This whitepaper provides comprehensive guidance for alarm management professionals executing migrations from Honeywell Alarm Configuration Manager (ACM) to Alarm Performance Optimizer (APO). Based on real-world pilot implementations and decades of alarm management expertise, this guide addresses the critical gap between vendor-provided migration tools and the realities of achieving operational excellence.

**Target Audience:**

- Alarm Management Engineers and Subject Matter Experts
- Control System Engineers
- Plant Operations Management
- IT/OT Infrastructure Teams
- Project Managers overseeing alarm system migrations

**Estimated Length:** 60-80 pages

---

## Outline Structure

### **Front Matter**

- Title Page
- Executive Summary (1 page)
- About the Authors (credentials and experience)
- Table of Contents
- List of Figures and Tables

---

## **1. Introduction** (2-3 pages)

### **1.1 The Alarm Management Migration Challenge**

- Industry context: ACM End of Life (December 31, 2027)
- The forced migration: what it means for plants worldwide
- Why alarm database migrations fail: complexity consistently underestimated
- The cost of poor migration execution (safety, operational, financial impacts)
- The gap between "migration complete" and "system operational excellence"

### **1.2 Purpose and Scope**

- **Who should read this guide:**
  - Alarm management professionals planning ACM to APO migrations
  - Control system engineers supporting migration projects
  - Operations and IT leadership overseeing alarm system upgrades
  - Consultants and system integrators performing migrations
- **What this guide covers:**
  - Pre-migration assessment and cleanup procedures
  - Migration planning and risk management
  - Technical execution best practices
  - Post-migration optimization and sustainment
  - Essential custom solutions and tools
  - Industry standards compliance during migration
- **What this guide does NOT cover:**
  - Basic APO installation procedures (refer to Honeywell documentation)
  - Fundamental alarm management principles (assumes working knowledge)
  - Specific site network/infrastructure design

### **1.3 Authors' Perspective and Methodology**

- Real-world experience: Marathon Petroleum Corporation pilot implementations
- Collaboration with Barbara Schubert (27 years alarm management expertise)
- Testing and validation approach: learning from early adopter challenges
- Integration of industry standards (ISA 18.2, EEMUA 191) into migration practices
- Honest assessment: acknowledging what works, what doesn't, and what's missing

---

## **2. Understanding the Migration Landscape** (4-5 pages)

### **2.1 ACM vs. APO: Critical Feature Analysis**

- **Feature parity gaps:**
  - Tags import/export (APO limitation: only Excel rationalization tool)
  - EMDB import/export (APO limitation: only manual individual creation)
  - Ability to move tags between consoles (not available in APO)
  - Easy drag-and-drop in hierarchy UI (not available in APO)
  - TagSync functionality (missing in APO)
  - TagList generation tool not available
  - No BMA support (critical gap)
  - Advanced query and bulk operations
- **APO R3.0.0 new capabilities:**
  - Constraints feature (alarm limit validation)
  - Offline rationalization (Excel-based updates)
  - Tag suspend/resume (maintenance support)
  - DeltaV DCS integration
  - Mode-based enforcement via AMS_Proxy
  - **Note:** Many features already available in ACM, not brand new
- **Functional workarounds required**
- **Vendor must disclose gaps for comprehensive assessment**
- **Timeline for feature development: what's coming, what's not**

### **2.2 Common Migration Misconceptions**

- **Myth 1:** "Installation successful means system is operationally excellent"
  - Reality: Installation is only the beginning; operational excellence requires extensive configuration, cleanup, and custom tools
- **Myth 2:** "Migration is just a database copy operation"
  - Reality: Data transformation, validation, and quality remediation required
- **Myth 3:** "Licensing will transfer automatically"
  - Reality: Ghost tags and invalid entries inflate license requirements; cannot reclaim excess later
- **Myth 4:** "Data quality issues can be fixed post-migration"
  - Reality: APO's limited tools make post-migration cleanup exponentially harder
- **Myth 5:** "Migration takes 2-4 weeks per site"
  - Reality: Depends entirely on pre-migration cleanup; 6-12 months preparation may be required
- **Myth 6:** "Vendor tools handle everything"
  - Reality: Custom solutions essential for operational excellence
- **Myth 7:** "Adjustments are easier in APO than ACM"
  - Reality: Some adjustments are much harder; many tools and functionalities missing
- **Myth 8:** "APO automates alarm rationalization"
  - Reality: APO tools require quality data first; garbage in = garbage out
- **Myth 9:** "APO has all ACM functionalities"
  - Reality: Many ACM features missing and not in product roadmap
- **Myth 10:** "Custom scripts and tools are easy in APO"
  - Reality: No database documentation provided; reverse engineering required
- **Myth 11:** "APO and Reporting can be installed simultaneously"
  - Reality: HAMR (Reporting) can and should be installed first for data quality validation
- **Myth 12:** "APO has no dependency on Reporting quality"
  - Reality: Bad reporting data = bad APO rationalization suggestions and metrics

### **2.3 Industry Standards Context**

- **ISA 18.2 Lifecycle Model implications:**
  - Stage I: Management of Change requirements for migration
  - Stage C: Rationalization review opportunity during migration
  - Stage A: Alarm Philosophy updates required
  - Stage J: Audit requirements before and after migration
- **EEMUA 191 considerations:**
  - Alarm performance KPI maintenance during migration (avoid degradation)
  - Risk assessment for migration activities
  - Operator workload management during transition
- **Migration as an opportunity for standards compliance improvement**

---

## **3. Order of Activities: Migration Sequence** (2-3 pages)

### **3.1 Recommended Migration Sequence**

1. **Install HAMR (Reporting)**

   - Establish baseline alarm performance data
   - Identify data quality issues early
   - Validate M&R database health
2. **Cleanup HAMR Database**

   - Requires HAMR 2.3.0 or later
   - Recommended: Allow few months for cleanup before APO installation
   - Remove ghost tags, optimize performance
3. **Cleanup ACM Database**

   - Hierarchy optimization and data quality remediation
   - Tag structure validation
   - Remove invalid tags and corruptions
4. **Install/Migrate APO**

   - Run in parallel with ACM initially
   - Maintain ACM for fallback capability
5. **Run in Parallel**

   - Typically 30-90 days
   - Longer if custom tools need development/migration
   - Critical validation period
6. **Migrate Custom Tools**

   - Develop APO equivalents for ACM custom tools
   - Test thoroughly in parallel environment
7. **Delta Migration or Re-migration**

   - Handle changes made during parallel operations
   - Incremental updates to APO
8. **Switch (Cutover)**

   - Disable ACM enforcements
   - Enable APO as primary system
   - Decommission ACM (retain for reference)

### **3.2 Training Needs Assessment**

*(Place training planning in Team/Planning section - Section 4.2)*

- **Adjustments to procedures required**
- **New functionalities can be postponed** (not immediately critical)
- **CRITICAL: Missing functionalities must be documented and loss mitigated**
  - Reality: "Users are using tools/options not available anymore!"
  - Reality: "Several new ways are much harder than ACM methods"
- **Training must address workflow changes, not just new features**

---

## **4. Pre-Migration Assessment: The Foundation of Success** (6-8 pages)

### **4.1 Database Health Assessment**

#### **4.1.1 ACM Database Quality Audit**

- **Assessment checklist:**
  - Invalid tags (tags not in DCS)
  - Ghost tags (historical tags no longer active)
  - Tags in wrong assets (hierarchy misalignment)
  - Corrupted parameters (invalid alarm limits, units, priorities)
  - SCADA tags requiring cleanup
  - Duplicate tags and naming inconsistencies
  - Corrupted notes
  - Tag description accuracy and completeness
  - Alarm Help configuration dependencies
  - Active enforcement mappings
  - Dynamic mode enforcement configurations
- **Health check methodology**
- **Tools and queries for assessment**
- **Validate ACM Consoles can map APO Consoles to HAMR Operating Positions**
- **Scoring system: Green/Yellow/Red health status**

#### **4.1.2 M&R (Metrics & Reporting) Database Assessment**

- **License consumption analysis:**
  - Identifying ghost tags (no events in M&R)
  - Tag merging opportunities (e.g., History Index 200, 201, 202...)
  - **Case study:** 10,000+ tag spike from invalid Redirection Index tags
- **Old/corrupted assets removal**
- **Path re-arrangements and optimization**
- **Adjustments of Operating Positions for APO\ACM Console mapping**
- **Unassigned process assets should be addressed**
- **Performance improvement opportunities:**
  - Closing invalid alarms in database
  - Removing invalid suppressed states
  - Merging tag descriptions
- **Retention period review and adjustment**

#### **4.1.3 EMDB Integrity Verification**

- **EAS EMDB quality assessment**
- **Automatic comparison tools** (identifying discrepancies)
- **Common EMDB issues discovered:**
  - Inconsistent naming conventions
  - Orphaned assets
  - Incorrect hierarchies
  - Duplicate paths
- **Cleanup and consolidation procedures**

### **4.2 Data Quality Issues to Address**

#### **4.2.1 Tag-Level Issues**

- **Non-alarmable tags:** Tags that don't meet alarm definition (ISA 18.2)
- **Invalid tag structures:** Tags that will fail migration validation
- **Tags not in DCS:** Historical or test tags still in database
- **Tag description quality:** Incomplete, inaccurate, or missing descriptions
- **Duplicate tags:** Same physical point represented multiple times
- **Tags in wrong assets:** Misaligned with plant hierarchy
- **BMA tags:** Need to be removed prior migration, may need to mitigate with APO 3.1
  - **Critical question:** Will Honeywell provide a process? Or each customer needs to reinvent it?

#### **4.2.2 Parameter-Level Issues**

- **Corrupted parameters:** Invalid alarm limits, deadbands, delays
- **Unit mismatches:** Engineering units inconsistent between ACM and DCS
- **Priority misalignment:** Priorities not following rationalization rules
- **Invalid time parameters:** Response times and delay settings
- **SCADA-specific corruptions:** Common in SCADA tag integrations
- **Notes corruption:** May lose alarm help on re-import or notes look unprofessional

#### **4.3.1 M&R Database Assessment**

- **Asset alignment:** Ensuring ACM, M&R, and EAS EMDB consistency
- **Path structure optimization**
- **New paths and reorganization opportunities**
- **Asset migration planning**
- **Addressing unassigned assets or incorrect assets assignments**

### **4.3 Licensing Analysis and Optimization**

#### **4.3.1 True License Requirement Calculation**

- **Ghost tag identification and removal**
- **Invalid tag removal**
- **Merging consolidated tags**
- **License consumption projections**
- **Cost impact analysis**

#### **4.3.2 License Ordering Strategy**

- **CRITICAL:** Cannot reclaim licenses after ordering
- **Validation procedures before license order**
- **Contingency buffer (recommended: 5-10%)**
- **License type selection (permanent vs. term)**

### **4.4 Current System Dependencies Assessment**

#### **4.4.1 Alarm Help Configuration**

- **Alarm Help Router connections**
- **Alarm Help content dependencies**
- **Custom Alarm Help integrations**
- **Migration impact on Alarm Help availability**

#### **4.4.2 Enforcement Dependencies**

- **Static enforcement mappings**
- **Dynamic mode enforcements** (highest risk)
- **Console-specific enforcements**
- **"Reverse enforcement" scenarios** (DCS is master)
  - Example: Dead Band Units controlled only on DCS
  - Custom enforcement rules requiring special handling

#### **4.4.3 Reporting and Integration Dependencies**

- **M&R reporting schedules and dependencies**
- **Custom reports and dashboards**
- **Third-party system integrations**
- **Data exports and interfaces**

### **4.5 Pre-Migration Cleanup Procedures**

#### **4.5.1 Establishing Temporary ACM Environment**

- **Installing temporary Manager Server**
- **Installing temporary Enforcer Server** (can be on client/station)
- **Purpose:** Allow cleanup without affecting production operations
- **Maintaining Alarm Help and enforcement availability**

#### **4.5.2 Step-by-Step ACM Cleanup**

1. **Clean EAS EMDB and load to ACM**
2. **Move tags to correct assets**
3. **Export and delete tags with invalid structure**
4. **Delete Control Modules if not used (CMs)**
5. **Clean known corruptions:**
   - SCADA tags
   - Corrupted notes
   - Invalid parameters
6. **Address reconfiguration errors** (ensures only tag with valid structures in ACM)
7. **Address enforcements errors**
8. **Validate tag descriptions**
9. **Change all enforcements to monitor mode**
10. **Adjust schedules to avoid OPC overload** (overlapping enforcements)
11. **DISABLE enforcements in ACM DB before migrating. You do not want overlap**
12. **Final health check before migration**

#### **4.5.3 M&R Database Optimization**

- **Hierarchy optimization**
- **Ghost tag removal procedures**
- **Asset cleanup and consolidation**
- **Performance optimization (closing invalid alarms, etc.)**
- **Retention adjustment implementation**

#### **4.5.4 Validation and Quality Assurance**

- **Pre-cleanup baseline metrics**
- **Post-cleanup validation**
- **Test enforcements and alarm help**
- **Reporting validation**
- **Sign-off criteria for migration readiness**

---

## **5. Migration Planning and Strategy** (6-8 pages)

### **5.1 Migration Approach Selection**

#### **5.1.1 Big Bang vs. Phased Migration**

- **Big Bang approach:**
  - Advantages: Single cutover, simpler coordination
  - Disadvantages: Higher risk, larger impact window
  - When to use: Small sites, single console configurations
- **Phased migration:**
  - Advantages: Lower risk per phase, learning opportunities
  - Disadvantages: Complex coordination, longer overall timeline
  - When to use: Multi-unit sites, high-criticality operations
- **Hybrid approach considerations**

#### **5.1.2 Parallel Operations Strategy**

- **Running ACM and APO concurrently**
  - Duration: typically 30-90 days
  - Critical for sites with active enforcements
  - Longer time needed when custom tools need to be developed\migrated
  - Especially important for dynamic mode enforcements
- **Synchronization strategies**
  - Change management during parallel operations
  - Conflict resolution procedures
  - Avoid OPC overload and overlap of enforcements
  - Data consistency validation
- **Import BMA tags when APO features are available**
- **Performance monitoring during parallel operations**
- **Cutover decision criteria**

#### **5.1.3 Delta Migration Approach**

- **Handling changes made after initial migration**
- **Incremental update procedures**
- **Validation of delta migrations**
- **When to lock ACM changes**
- **How to compare before switching**

### **5.2 Team Structure and Expertise Requirements**

#### **5.2.1 Required Roles and Responsibilities**

- **Migration Project Manager:** Overall coordination, timeline, stakeholder communication
- **Alarm Management SME:** Technical lead, decision authority on alarm-related issues
- **Control System Engineer:** DCS integration, enforcement testing
- **Database Administrator:** SQL Server configuration, backup/recovery
- **Operations Representative:** Operator impact assessment, training coordination
- **IT/Network Engineer:** Infrastructure, security, connectivity
- **Vendor Technical Support:** Honeywell engagement strategy

#### **5.2.2 Subject Matter Expert Involvement**

- **When SME involvement is critical:**
  - Pre-migration assessment and cleanup planning
  - Migration strategy selection
  - Complex data transformation decisions
  - Post-migration optimization
- **Avoiding over-reliance on vendor resources**
- **Building internal expertise for long-term sustainment**

#### **5.2.3 Internal vs. External Resources**

- **When to use external consultants**
- **Knowledge transfer requirements**
- **Retaining institutional knowledge**

### **5.3 Risk Assessment and Mitigation**

#### **5.3.1 Critical Risk Categories**

- **Technical risks:**
  - Data corruption during migration
  - Non-optimal configurations (impossible\difficult to adjust later)
  - Enforcement failures
  - Reporting inaccuracies
  - Performance degradation
  - Integration failures
  - Data corruptions during potential DB\snapshots restore (high risk for multiple servers)
  - **Develop a plan for reliable backup and restore**
  - **Can we redo migration without a need to restore servers?**
- **Operational risks:**
  - Operator confusion or alarm fatigue
  - Loss of alarm help during transition
  - Increased alarm response times
  - Safety system impacts
- **Project risks:**
  - Timeline overruns
  - Resource unavailability
  - Vendor support delays
  - Budget overruns

#### **5.3.2 High-Risk Site Profiles**

- **Complex multi-unit sites**
- **Sites with extensive custom integrations**
- **Sites with poor ACM data quality**
- **Sites with dynamic mode enforcements**
- **Sites with limited alarm management expertise**
- **Sites with multiple APO servers** (so synchronized snapshots critical)

#### **5.3.3 Mitigation Strategies**

- **Risk-specific mitigation plans**
- **Contingency planning**
- **Rollback procedures and criteria, how to avoid data inconsistencies on restore**
- **Communication escalation paths**

### **5.4 Timeline and Milestone Planning**

#### **5.4.1 Realistic Timeline Development**

- **Pre-migration phase: 6-12 months**
  - Assessment: 1-2 months
  - Cleanup: 3-6 months
  - Tool development: 2-4 months (concurrent)
  - Team training: ongoing
- **Migration execution: 2-4 weeks per site**
- **Post-migration stabilization: 30-90 days**

#### **5.4.2 Critical Path Activities**

- **License estimation**
- **License ordering (long lead time)**
- **Database cleanups (often underestimated)**
- **Hierarchy cleanups (spans ACM, M&R, and EMDBs)**
- **Infrastructure preparation**
- **Vendor coordination**

#### **5.4.3 Milestone Definition and Tracking**

- **Phase gates and go/no-go criteria**
- **Metrics for progress tracking**
- **Regular status reporting cadence**

#### **5.4.4 Buffer Planning**

- **Recommended buffer: 25-30% on top of estimated timeline**
- **Contingency time allocation**
- **Managing stakeholder expectations**

### **5.5 Stakeholder Communication Plan**

#### **5.5.1 Operations Involvement and Buy-In**

- **Early engagement with operations leadership**
- **Operator surveys and feedback**
- **Training needs assessment**
- **Change impact communication**

#### **5.5.2 Management Reporting**

- **Executive-level status reporting**
- **Financial tracking and budget management**
- **Risk escalation procedures**
- **Success metrics and KPIs**

#### **5.5.3 Change Management Approach**

- **Communication frequency and channels**
- **Training and awareness programs**
- **Resistance management**
- **Celebrating milestones**

---

## **6. Technical Migration Execution** (10-12 pages)

### **6.1 Environment Preparation**

#### **6.1.1 Infrastructure Requirements**

- **Server specifications** (APO Site Server, Transfer Service)
- **Network requirements** (connectivity to DCS, database servers)
- **Storage requirements and growth planning**
- **Virtualization considerations**

#### **6.1.2 SQL Server Configuration**

- **SQL Server version requirements** (compatibility matrix)
- **Database sizing and performance tuning**
- **SQL permissions and service accounts**
- **SQL Server properties**
- **Transaction log management**
- **Backup infrastructure**

#### **6.1.3 Organizational Standards**

- **Schema naming conventions** (consistency across sites)
- **Folder structures and file organization**
- **Service account naming and management**
- **Security group assignments**
- **Documentation standards**

#### **6.1.4 Network and Security**

- **Firewall rules and port requirements**
- **Certificate management (SSL/TLS)**
- **Domain trust relationships**
- **OT security compliance**

### **6.2 Installation Best Practices**

#### **6.2.1 Following Organizational Standards During Install**

- **Standard installation checklists**
- **Standard naming conventions**
- **Standard configurations**
- **Configuration management approach**
- **As-built documentation requirements**

#### **6.2.2 Database Creation and Migration**

- **APO database creation procedures**
- **ACM to APO data migration process**
- **Validation of migrated data**

#### **6.2.3 Asset Migration Approach**

- **EMDB to APO asset structure mapping**
- **Hierarchy recreation and validation**
- **Console assignment**

#### **6.2.4 System Configuration**

- **Site settings and preferences**
- **User authentication (Active Directory integration)**
- **Role-based access control (RBAC) setup**
- **Notification configuration (email alerts, etc.)**

### **6.3 Data Migration Process**

**Pre-migration: Mandatory... disable scheduled enforcement for ACM DB that will migrate. You do not need overlap or execution before testing! This is why it is important to have temporary environment to make these adjustments (not in production!)**

#### **6.3.1 APO R3.0.0 Migration Utility Usage**

- **Migration utility features and capabilities**
- **Pre-migration validation checks**
- **Migration utility configuration**
- **Execution and monitoring**

#### **6.3.2 Three-Phase Migration Approach**

- **Phase 1: Pre-migration**
  - Configure essential components
  - Secure site environment
  - Validate prerequisites
  - Validate quality of data
- **Phase 2: Migration**
  - Validate source data
  - Map assets and tags
  - Execute migration utility
  - Monitor progress
- **Phase 3: Post-migration**
  - Conduct data integrity reviews
  - Validation tools execution
  - Reconciliation reports
  - Validate quality of data

#### **6.3.3 Data Transformation and Mapping**

- **Tag attribute mapping (ACM to APO)**
- **Priority translation**
- **Alarm type conversions**
- **Custom field mapping**

#### **6.3.4 Error Handling and Resolution**

- **Common migration errors and causes**
- **Error log analysis**
- **Remediation procedures**
- **When to restart vs. fix-forward**

#### **6.3.5 Data Integrity Verification**

- **Tag count reconciliation**
- **Asset structure validation**
- **Alarm limit verification**
- **Enforcement mapping confirmation**
- **Sample testing approach**

### **6.4 Parallel Operations Management**

#### **6.4.1 Running ACM and APO Concurrently**

- **Infrastructure for parallel operations**
- **Data synchronization strategy**
- **Avoid OPC overload \ overlapping tasks (enforcements, tagsync)**
- **Operator interface management (which system is primary?)**

#### **6.4.2 Critical Considerations for Enforcements**

- **Static enforcements:** Parallel operation approach
- **Dynamic mode enforcements:** High-risk scenarios
- **Testing enforcements without impacting DCS**
- **Enforcement cutover planning**

#### **6.4.3 Conflict Resolution Procedures**

- **Change request management during parallel operations**
- **Which system is source of truth?**
- **Merging changes from both systems**

#### **6.4.4 Performance Monitoring**

- **System resource utilization**
- **Response time monitoring**
- **Operator workload assessment**

### **6.5 Testing and Validation**

#### **6.5.1 Comprehensive Testing Checklist**

- **Hierarchy verification:** All assets and tags in correct locations
- **Tag count reconciliation:** ACM vs. APO counts match expectations
- **Alarm limit accuracy:** Sample testing of limits, deadbands, priorities
- **Enforcement testing:** No errors when enforcing to DCS
- Static enforcements
- Dynamic mode enforcements
- Reverse enforcements (DCS is master)
- **Alarm Help validation:** All Alarm Help content accessible
- **Reporting integration:** APO receiving M&R/HAM-R receiving APO data
- **User authentication:** All users can log in with correct permissions
- **Console connectivity:** All consoles communicating with APO
- **Notification testing:** Email alerts and notifications working
- **Performance benchmarking:** Response times acceptable

#### **6.5.2 Test Scenarios and Scripts**

- **Normal operations testing**
- **Alarm flood scenario**
- **Enforcement failure scenarios**
- **User permission testing**
- **Failover and recovery testing**

#### **6.5.3 Operator Acceptance Testing**

- **Operator-led validation**
- **Usability feedback**
- **Training effectiveness assessment**

#### **6.5.4 Go-Live Readiness Assessment**

- **Go/no-go criteria checklist**
- **Sign-off procedures**
- **Rollback decision criteria**

---

## **7. Post-Migration Operations and Optimization** (5-6 pages)

### **7.1 Immediate Post-Migration Activities**

#### **7.1.1 Proper Backups Implemented**

- **Database backup verification**
- **Snapshot strategy for multiple servers**
- **Recovery testing procedures**
- **Backup retention policies**

#### **7.1.2 Go-Live Checklist**

- All operators trained and signed off
- ACM parallel operations plan executed (if applicable)
- 24/7 support coverage for first 48-72 hours
- Communication to stakeholders (go-live announcement)
- Monitoring dashboard active
- Escalation procedures communicated

#### **7.1.2 First 24-48 Hours Monitoring**

- **Intensive monitoring period**
- **Common issues in first hours:**
  - Enforcement synchronization delays
  - Alarm Help access issues
  - Reporting data gaps
  - User authentication problems
- **On-call support requirements**

#### **7.1.3 Incident Response Procedures**

- **Issue categorization (Critical/High/Medium/Low)**
- **Escalation paths**
- **Communication protocols**
- **War room operations (if needed)**

#### **7.1.4 Quick-Fix Strategies**

- **Common issues and rapid solutions**
- **When to rollback vs. fix-forward**
- **Documentation requirements for post-go-live changes**

### **7.2 Health Monitoring Implementation**

#### **7.2.1 Daily Automated Health Checks (ESSENTIAL)**

- **Why this is non-negotiable:** Vendor delivery does not include effective health monitoring
- **Health check categories:**
  - **ACM/APO replication heartbeat** (if running parallel)
  - **Collection status** (data flow from DCS)
  - **Suppress sync status**
  - **Active sync status**
  - **Disk space monitoring**
  - **Database backups completion**
  - **Reports delivery** (scheduled reports sent successfully)
  - **Reports generation** (reports running on schedule)
  - **Enforcements status** (no stuck enforcements)
  - **User closed activities** (should be minimal if quality is good)
  - **Hierarchy integrity** (new paths, tags in wrong assets)
  - **Hierarchy consistency** (Reporting vs. APO alignment)
  - **Tag Sync monitoring** (failures, tags needing attention)
  - **Enforcements stuck detection** (with optional automatic recovery)
  - **Database quality checks**
  - **Duplicate tag detection**
  - **Licensing alerts** (include optimization opportunities)
  - **Critical event notifications** (alarms discarded, enforcement errors)

**Sync Quality Validation (Daily/Weekly):**

- **Active Alarms report reasonableness check:**
- More ReturnToNormal events than Alarm events (healthy system indicator)
- Stale alarms should be accurately synced
- **Suppressed Report spot-check:** Validate longest duration disable/enable/inhibit entries
- **Shelved Report accuracy:** Focus on active process alarms (>90% target)
- **"Confusion period" monitoring:** Time delays in sync processing (Active: ~1-3 min, Suppressed: ~10 min)
- **DynAMoSyncQueue inspection:** Check for invalid paths/priorities before processing

#### **7.2.2 Alert Configuration and Escalation**

- **Alert severity levels**
- **Notification distribution lists**
- **Escalation timelines**
- **After-hours support coverage**

#### **7.2.3 Proactive Issue Detection**

- **Trending and analytics**
- **Predictive issue identification**
- **Preventive maintenance triggers**

#### **7.2.4 Benefits Beyond Alarm Management**

- **Case studies:** Health checks discovering issues in TPS, Experion, DCS
- **System-wide visibility**
- **Reduced MTTR (Mean Time to Repair)**

### **7.3 Reporting Quality Assurance**

#### **7.3.1 Active Sync Enhancements**

- **Why standard Active Sync is insufficient**
- **Essential enhancements:**
  - Sync shelved alarms
  - Sync system alarms
  - Sync DAS (Distributed Alarm Server/Dynamic Alarm Suppression)
  - Sync CUTOUT
  - Sync Enable/Disable/Inhibit/JournalOnly
  - Sync Inactive
- **Workarounds for M&R limitations**
  - E.g. re-open valid alarms closed by the user
- **Maintenance tools**

#### **7.3.2 Suppressed Sync Improvements**

- **Standard suppressed sync gaps:**
  - Missing suppress value columns (no meaningful user info)
  - Lack of filtering capabilities
  - Sync Enable/Disable/Inhibit/JournalOnly
  - Sync Inactive
- **Impact of missing suppressed sync: "Not only Suppressed report but also KPIs are not accurate"**
- **Implementation of full suppressed sync**

#### **7.3.3 KPI Accuracy Validation**

- **Comparison: ACM KPIs vs. APO KPIs[BS5.1]**
- **Reconciliation of discrepancies**
- **ISA 18.2 / EEMUA 191 metrics validation**

#### **7.3.4 Custom Filtering and Reporting Setup**

- **Alarm Class filtering (every site should have)**
- **Normal and Current Mode reporting**
- **Daily differences reporting (lists)**
- **Charts comparing and showing progress over time**
- **Enhanced Tag Sync management – APO 3.0 does not have TagSync**

### **7.4 Backup and Recovery Procedures**

#### **7.4.1 Deterministic Backup Strategies**

- **Problem:** Standard instructions do not ensure deterministic restore
- **Coordinated backup approach:**
  - APO database (full)
  - Configuration files
  - Custom scripts and tools
  - Integration points
- **Backup schedule and retention**
- **Off-site/cloud backup considerations**

#### **7.4.2 Recovery Testing and Validation**

- **Regular recovery drills**
- **Recovery time objective (RTO) validation**
- **Recovery point objective (RPO) validation**
- **Documentation of recovery procedures**

#### **7.4.3 Purge Strategies for Performance**

- **Effective purge procedures**
- **Data retention policies**
- **Archive strategies for historical data**
- **Performance impact of data growth**

### **7.5 Continuous Improvement**

#### **7.5.1 Regular Database Maintenance**

- **Weekly maintenance tasks**
- **Monthly optimization activities**
- **Quarterly health assessments**

#### **7.5.2 License Optimization (Ongoing)**

- **Ghost tag monitoring and removal**
- **License consumption trending**
- **Optimization opportunities identification**

#### **7.5.3 Performance Tuning**

- **Query optimization**
- **Index maintenance**
- **Resource utilization monitoring**

#### **7.5.4 User Feedback Incorporation**

- **Regular operator surveys**
- **Usability improvement initiatives**
- **Feature request tracking**

---

## **8. Essential Tools and Custom Solutions** (4-5 pages)

### **8.1 Why Standard Delivery Is Insufficient**

#### **8.1.1 APO Limitations vs. Operational Requirements**

- **Vendor statement:** "APO is currently mainly enhanced Rationalization tool with enforcements similar to ACM"
- **Missing critical alarm management tools**
- **Impact on post-migration adjustments**

#### **8.1.2 The Gap Between Installation and Excellence**

- **Installation ≠ operational effectiveness**
- **"Reporting is collecting and produces reports on schedule... ACM can do enforcements and shows alarm help... It does not mean the system works well and provides optimal value!"**

#### **8.1.3 Cost of Not Addressing Gaps**

- **Inaccurate KPIs and reporting**
- **Prolonged troubleshooting times**
- **License bloat and wasted costs**
- **Operator frustration and alarm fatigue**
- **Increased risk of alarm-related incidents**

### **8.2 Critical Custom Solutions**

#### **8.2.1 Daily Automated Health Checks**

- **Implementation guide:**
  - Architecture (scheduled tasks, PowerShell/Python scripts, SQL queries)
  - Data collection methods
  - Alert generation and distribution
  - Dashboard visualization
- **Sample scripts and queries**
- **Maintenance and updates**

#### **8.2.2 ACM Maintenance Solution**

- **Purpose:** Ensure reliability of Alarm Help and Enforcements
- **Combines information from:**
  - Database
  - Enforcements
  - TagSync (reconfiguration, add/delete, SCADA maintenance)
  - Reporting (detects tags that alarmed but not in ACM/APO)
- **Functionality:**
  - Mark tags needing deterministic attention
  - Identify tags needing to be moved, reloaded, deleted, or released

#### **8.2.3 Full Active Sync and Suppressed Sync**

**Standard Sync Quality Issues (Quantified):**

- **Experion Active Sync:** 95% accuracy (70% for system alarms)
- **ESVT Active Sync:** 90% accuracy (requires unknown timestamp hotfix)
- **TPS Active Sync:** 50-93% accuracy (degrades over time)
- **Suppressed Sync:** 50-99% accuracy, causes system overload
- **Shelved Sync:** 70% accuracy, generates excessive confusing events

**Alternative Active Sync Approach (Barbara Schubert Method):**

- **Quality:** Consistently near 100% accuracy (does not degrade over time)
- **Method:** File-based sync using notifdump files from consoles
- **Advantages:**
  - Eliminates OPC dependency and connectivity issues
  - Syncs after collection completes (no "confusion periods")
  - WYSIWYG validation (simple VBS script)
  - Handles hybrid systems (no standard sync available)
  - Detects missing alarms (ESVT standard sync cannot)
- **Implementation:**
  1. Generate notifdump files from EST/ESVT/TPS consoles (scheduled)
  2. Process files with custom script (ActiveSync_GenerateFilesForDynAMo)
  3. Validate output file for correctness
  4. Map priorities and paths via PPS script
  5. Schedule Active Sync to process ACT file
- **Deployment History:** Successfully implemented at Carson, Wilmington, Robinson, Canton, Garyville, Paulsboro
- **When to Use:** Hybrid systems, complex OPC environments, sites requiring maximum accuracy

**Standard Active/Suppressed Sync Enhancements:**

- Sync shelved alarms, system alarms, DAS, CUTOUT
- Sync Enable/Disable/Inhibit/JournalOnly and Inactive
- Add suppress value columns for meaningful reporting
- Implement filtering capabilities
- **Critical:** "Without these enhancements, not only Suppressed report but also KPIs are not accurate"

#### **8.2.4 Asset Management Tools**

- **EMDB comparison and cleanup utilities**
- **Automatic construction of code for reporting**
- **Asset mapping for reporting quality**

#### **8.2.5 Reverse Enforcement Tools**

- **Purpose:** Keep APO and DCS in sync when DCS is master
- **Use cases and implementation**

#### **8.2.6 Custom Filtering and Reporting**

- **Alarm Class implementation**
- **Normal and Current Mode reporting tools**
- **Enhanced management using Tag Sync**
- **Notifications and exclusion lists management**

### **8.3 Tool Selection and Development**

#### **8.3.1 Build vs. Buy Decisions**

- **When to develop custom solutions**
- **When to purchase third-party tools**
- **Partnership opportunities (e.g., Barbara Schubert consulting)**

#### **8.3.2 Integration Considerations**

- **API and interface requirements**
- **Data exchange formats**
- **Security and authentication**

#### **8.3.3 Maintenance and Support Planning**

- **Internal capability development**
- **Update and enhancement procedures**
- **Version control and change management**

#### **8.3.4 Knowledge Transfer Requirements**

- **Documentation standards**
- **Training programs**
- **Succession planning**

---

## **9. Common Pitfalls and How to Avoid Them** (4-5 pages)

### **9.1 Technical Pitfalls**

#### **9.1.1 Insufficient Pre-Migration Cleanup**

- **Symptom:** Migration takes 3x longer than estimated, or migration fails validation
- **Root cause:** Underestimating ACM database corruption and quality issues
- **Prevention:** Comprehensive pre-migration assessment (Section 3)
- **Recovery:** May require migration rollback and re-cleanup

#### **9.1.2 Underestimating Data Quality Issues**

- **Symptom:** Inaccurate licensing, enforcements fail, reporting discrepancies
- **Root cause:** Assuming "migration tool handles everything"
- **Prevention:** Detailed data quality audit and remediation before migration
- **Recovery:** Manual tag-by-tag correction (time-consuming and error-prone)

#### **9.1.3 Ignoring EMDB Integrity**

- **Symptom:** Assets misaligned, tags in wrong locations, hierarchy confusion
- **Root cause:** Not validating EAS EMDB before migration
- **Prevention:** EMDB comparison and cleanup tools (Section 7.2.4)
- **Recovery:** Asset restructuring post-migration (limited tools in APO)

#### **9.1.4 Inadequate Testing Before Cutover**

- **Symptom:** Critical issues discovered in production, operator confusion
- **Root cause:** Rushing to cutover without comprehensive testing
- **Prevention:** Follow testing checklist (Section 5.5.1)
- **Recovery:** Emergency troubleshooting during production operations (high risk)

#### **9.1.5 Ghost Tags and License Bloat**

- **Symptom:** License count 2-3x higher than expected, cannot reclaim
- **Root cause:** Not removing ghost tags and invalid entries before license order
- **Prevention:** License optimization procedures (Section 3.3)
- **Recovery:** None - cannot reclaim licenses after ordering

#### **9.1.6 Backup/Restore Failures**

- **Symptom:** Cannot restore system to known-good state
- **Root cause:** Following standard instructions that don't ensure deterministic restore
- **Prevention:** Coordinated backup strategy (Section 6.4.1)
- **Recovery:** Manual system rebuild (significant downtime)

### **9.2 Organizational Pitfalls**

#### **9.2.1 Lack of Subject Matter Expert Involvement**

- **Symptom:** Poor decisions during migration, scope creep, rework
- **Root cause:** Treating migration as "IT project" rather than alarm management initiative
- **Prevention:** Engage alarm management SME from project inception
- **Recovery:** Bring in expert for post-migration remediation (expensive)

#### **9.2.2 Insufficient Operator Training**

- **Symptom:** Operators confused, increased alarm response times, resistance to new system
- **Root cause:** Underestimating change impact on operators
- **Prevention:** Comprehensive training program and operator involvement
- **Recovery:** Remedial training and operator support (impacts confidence)

#### **9.2.3 Poor Change Management**

- **Symptom:** Resistance, lack of buy-in, communication breakdowns
- **Root cause:** Treating migration as technical project without change management
- **Prevention:** Stakeholder communication plan (Section 4.5)
- **Recovery:** Retroactive change management (limited effectiveness)

#### **9.2.4 Unrealistic Timelines**

- **Symptom:** Rushed migration, skipped steps, quality compromises
- **Root cause:** Underestimating migration complexity, ACM End of Support deadline pressure
- **Prevention:** Realistic timeline development with 25-30% buffer (Section 4.4)
- **Recovery:** Extend timeline (if possible) or accept technical debt

#### **9.2.5 Inadequate Resources**

- **Symptom:** Project delays, key person burnout, corners cut
- **Root cause:** Underestimating effort required, resource allocation issues
- **Prevention:** Proper team structure (Section 4.2)
- **Recovery:** Bring in additional resources (may delay project)

### **9.3 Vendor Relationship Pitfalls**

#### **9.3.1 Over-Reliance on Standard Vendor Delivery**

- **Symptom:** Operational excellence not achieved, continuous frustration
- **Root cause:** Assuming vendor tools provide complete solution
- **Prevention:** Understand gaps (Section 2.1, 7.1) and plan custom solutions
- **Recovery:** Develop custom solutions post-migration (harder than proactive development)

#### **9.3.2 Unclear Support Boundaries**

- **Symptom:** Issues unresolved, finger-pointing, extended downtime
- **Root cause:** Not understanding what Honeywell does/doesn't support (e.g., "replication not supported")
- **Prevention:** Clear SLA definition and escalation procedures
- **Recovery:** Bring in third-party expertise

#### **9.3.3 Insufficient SLA Definition**

- **Symptom:** Slow vendor response, unmet expectations
- **Root cause:** Not negotiating response times and support levels
- **Prevention:** Enhanced SLAs (Section 6 recommendations from analysis document)
- **Recovery:** Escalation and contract renegotiation

#### **9.3.4 Missing Functionality Discovered Post-Migration**

- **Symptom:** Cannot perform operations previously possible in ACM
- **Root cause:** Not conducting thorough gap analysis before migration
- **Prevention:** Feature parity analysis (Section 2.1)
- **Recovery:** Develop workarounds or wait for APO feature development (may be 12-24 months or full solution may not be delivered in any reasonable time)

### **9.4 Case Studies: Lessons Learned**

#### **9.4.1 Case Study 1: License Issued Based on Past License Count**

- **Scenario:** License issued based on past ACM license count without evaluating current database usage
- **Issue:** Customer actually had higher usage in ACM than licensed but never noticed; migration to APO validation fails
- **Impact:** Migration delays while waiting for additional licenses, project timeline extended by weeks or months
- **Lesson:** Always evaluate actual current database usage before ordering licenses; past license counts may not reflect reality (Section 3.3)

#### **9.4.2 Case Study 2: Ghost Tag License Crisis**

- **Scenario:** Site migrated without cleanup, ordered licenses based on ACM MnR \ HAMR tag count
- **Issue:** APO license count 2.5x higher than expected (10,000+ ghost tags from Redirection Index entries)
- **Additional Impact:** HAMR can have even 30-40% of ghost tags (old tags with no events)… they not just inflate the cost \ license but affect performance
- **Impact:** Unplanned $XXX,XXX cost, cannot reclaim excess licenses
- **Lesson:** License optimization MUST occur before ordering (Section 3.3)

#### **9.4.3 Case Study 3: Dynamic Enforcement Failure**

- **Scenario:** Site with dynamic mode enforcements migrated without parallel operation period
- **Issue:** Enforcements failed in production, DCS overwrites caused process upsets
- **Impact:** 48-hour period of manual alarm management, operator frustration
- **Lesson:** Sites with dynamic enforcements require extended parallel operations (Section 4.1.2)

#### **9.4.4 Case Study 4: Reporting Inaccuracy**

- **Scenario:** Site migrated and declared "successful," KPIs reported for management
- **Issue:** KPIs discovered to be inaccurate (Active Sync and Suppressed Sync incomplete, Operating Positions wrong)
- **Impact:** Management decisions based on bad data, compliance risk
- **Lesson:** Standard Active/Suppressed Sync insufficient, custom solutions required (Section 7.2.3)

#### **9.4.5 Case Study 5: Health Check Gap**

- **Scenario:** Site migrated without implementing daily health checks
- **Issue:** Enforcements stopped working due to service failure, not discovered for 3 weeks
- **Impact:** DCS and APO out of sync, required manual reconciliation
- **Lesson:** Daily automated health checks are essential, not optional (Section 6.2.1)

#### **9.4.6 Case Study 6: Standard Sync Degradation**

- **Scenario:** TPS site using standard Active Sync, initially reporting 85% accuracy
- **Issue:** Sync accuracy degraded to 50% over 6 months; stale alarms persisted in reports
- **Impact:** Management decisions based on inaccurate KPIs, compliance risk
- **Solution:** Implemented Alternative Active Sync (file-based method)
- **Result:** Accuracy improved to near 100%, consistently maintained
- **Lesson:** Standard sync accuracy degrades over time; Alternative sync prevents deterioration (Section 7.2.3)

#### **9.4.7 Case Study 7: Hybrid System Without Sync**

- **Scenario:** Site with hybrid Experion/TPS system (operators using both stations and native windows)
- **Issue:** No standard sync available for hybrid configurations
- **Impact:** Active Alarms report completely inaccurate, operators lost confidence in alarm management system
- **Solution:** Alternative Active Sync (only available option for hybrid systems)
- **Result:** Accurate reporting restored, operator confidence rebuilt
- **Lesson:** Hybrid systems require Alternative Active Sync approach (Section 7.2.3)

*(Note: Case studies use anonymous site references to protect confidentiality)*

---

## **10. Industry Standards Compliance During Migration** (3-4 pages)

### **10.1 ISA 18.2 Lifecycle Implications**

#### **10.1.1 Stage A: Philosophy Updates Required**

- **Migration triggers Philosophy review:**
  - Update to reflect APO capabilities and limitations
  - Document workarounds and custom solutions
  - Revise alarm performance targets (if applicable)
  - Update MOC procedures for APO
- **Philosophy as migration guide**

#### **10.1.2 Stage C: Rationalization Review Opportunity**

- **Migration as catalyst for rationalization:**
  - Review alarm priorities during migration
  - Update consequence and response time analysis
  - Correct historical rationalization errors
  - Align with current ISA 18.2 / EEMUA 191 best practices
- **Rationalization timing considerations** (before or after migration?)

#### **10.1.3 Stage I: MOC Procedures for Migration**

- **Migration is a major MOC:**
  - Formal approval and sign-off required
  - Risk assessment and mitigation plans
  - Rollback procedures documented
  - Change communication to all stakeholders
- **Managing changes during migration** (freeze periods, delta migrations)

#### **10.1.4 Stage J: Audit Requirements**

- **Pre-migration audit:** Establish baseline
- **Post-migration audit:** Validate compliance maintained or improved
- **Audit frequency during migration period**

#### **10.1.5 Stage H: Monitoring & Assessment Continuity**

- **Maintaining KPI tracking during migration**
- **Avoiding alarm performance degradation**
- **Reporting continuity strategies**

### **10.2 EEMUA 191 Considerations**

#### **10.2.1 Alarm Performance KPI Maintenance**

- **Target: No degradation during migration**
- **Monitoring alarm rates throughout migration:**
  - Average alarm rate per operator
  - Peak alarm rates
  - % of time in flood conditions
- **Intervention if KPIs worsen**

#### **10.2.2 Risk Assessment for Migration Activities**

- **Migration as a hazard:** What could go wrong?
- **Layers of Protection analysis:** What protects against migration failures?
- **Mitigation hierarchy:**
  1. Eliminate risk (e.g., thorough pre-migration testing)
  2. Reduce risk (e.g., parallel operations)
  3. Detect risk (e.g., health monitoring)
  4. Respond to risk (e.g., rollback procedures)

#### **10.2.3 Operator Workload Management**

- **EEMUA guidance on operator capacity:**
  - Maximum manageable alarm rate: 2 per 10 minutes
  - Acceptable alarm rate: <1 per 10 minutes
- **Ensuring migration does not overload operators**
- **Training and support during transition**

### **10.3 Compliance Validation**

#### **10.3.1 Pre-Migration Compliance Baseline**

- **Document current compliance status:**
  - ISA 18.2 KPI metrics
  - EEMUA 191 benchmarks
  - Philosophy adherence
  - Audit findings
- **Establish improvement targets for post-migration**

#### **10.3.2 Post-Migration Compliance Verification**

- **KPI comparison: pre-migration vs. post-migration**
- **Philosophy adherence validation**
- **Lifecycle stage execution review**
- **Audit findings and remediation plans**

#### **10.3.3 Addressing Compliance Gaps Discovered**

- **Migration as opportunity to close gaps**
- **Prioritization of compliance initiatives**
- **Long-term compliance roadmap**

---

## **11. Roadmap to Migration Success** (3-4 pages)

### **11.1 6-12 Month Pre-Migration Phase**

#### **Month 1-2: Assessment and Planning**

- Conduct comprehensive database health assessment (Section 3.1)
- Perform licensing analysis and optimization (Section 3.3)
- Assess current system dependencies (Section 3.4)
- Select migration approach (Section 4.1)
- Define team structure and assign roles (Section 4.2)
- Conduct risk assessment (Section 4.3)
- Develop project plan and timeline (Section 4.4)
- Establish stakeholder communication plan (Section 4.5)
- **Deliverables:** Assessment report, migration strategy document, project plan

#### **Month 3-6: Cleanup and Optimization**

- Establish temporary ACM environment (if needed) (Section 3.5.1)
- Execute ACM database cleanup (Section 3.5.2)
- Execute M&R database optimization (Section 3.5.3)
- Clean and validate EMDB (Section 3.2.3)
- Conduct post-cleanup validation (Section 3.5.4)
- **Milestone:** Database cleanup complete and validated

#### **Month 4-8: Tool Development/Acquisition (Concurrent)**

- Develop or acquire daily health check solution (Section 7.2.1)
- Implement ACM Maintenance solution (Section 7.2.2)
- Develop Active Sync and Suppressed Sync enhancements (Section 7.2.3)
- Implement asset management tools (Section 7.2.4)
- Configure custom filtering and reporting (Section 7.2.6)
- Test all custom solutions
- **Milestone:** Essential custom solutions ready for deployment

#### **Month 6-9: Infrastructure and Environment Prep**

- Prepare APO infrastructure (servers, storage, network) (Section 5.1)
- Configure SQL Server (Section 5.1.2)
- Install APO software (Section 5.2)
- Configure APO Site settings (Section 5.2.4)
- **Milestone:** APO environment ready for migration

#### **Month 9-10: Team Training**

- Alarm management SME advanced training
- Control system engineer APO training
- Database administrator APO-specific training
- Operator awareness and preliminary training
- IT/Network engineer infrastructure training
- **Milestone:** Team trained and ready

#### **Month 10-12: Final Validation and Go-Live Prep**

- Order APO licenses (ensure accuracy - cannot reclaim excess) (Section 3.3.2)
- Conduct pre-migration compliance baseline (Section 9.3.1)
- Final validation of cleaned databases
- Develop detailed cutover plan
- Prepare rollback procedures
- Schedule migration execution window
- Communicate go-live plans to stakeholders
- **Milestone:** Ready for migration execution

### **11.2 Migration Execution Phase (2-4 weeks per site)**

#### **Week 1: Migration Execution**

- **Day 1-2:** Execute data migration using APO utility (Section 5.3)
- **Day 2-3:** Validate migrated data (Section 5.3.5)
- **Day 3-4:** Configure enforcements and Alarm Help (Section 5.4)
- **Day 4-5:** Conduct comprehensive testing (Section 5.5.1)
- **Day 5:** Go/no-go decision for parallel operations

#### **Week 2: Parallel Operations Begin**

- Start ACM and APO parallel operations (Section 5.4.1)
- Monitor system performance continuously (Section 5.4.4)
- Deploy daily health checks (Section 6.2.1)
- Address any issues discovered in parallel operations
- Conduct operator training on APO interface

#### **Week 3-4: Stabilization and Cutover**

- Continue parallel operations monitoring
- Validate reporting integration (Section 6.3)
- Conduct operator acceptance testing (Section 5.5.3)
- Final go-live readiness assessment (Section 5.5.4)
- Execute cutover to APO primary
- Maintain ACM as backup for 30 days (if possible)
- **Milestone:** Go-live complete

### **11.3 Post-Migration Stabilization (30-90 days)**

#### **Days 1-7: Intensive Monitoring**

- 24/7 support coverage
- Hourly monitoring for first 48 hours (Section 6.1.2)
- Daily monitoring for remainder of week
- Rapid issue resolution (Section 6.1.3)
- Daily status reports to stakeholders

#### **Days 8-30: Optimization Phase**

- Implement reporting quality enhancements (Section 6.3)
- Configure backup and recovery procedures (Section 6.4)
- Fine-tune health checks based on observations
- Address any operator feedback
- Conduct post-migration compliance validation (Section 9.3.2)
- **Milestone:** 30-day post-go-live review

#### **Days 31-90: Continuous Improvement**

- Establish regular database maintenance schedule (Section 6.5.1)
- Implement license optimization procedures (Section 6.5.2)
- Performance tuning based on usage patterns (Section 6.5.3)
- Conduct operator survey and incorporate feedback (Section 6.5.4)
- Decommission ACM (if parallel operations still active)
- **Milestone:** 90-day post-go-live review and project closeout

### **11.4 Long-Term Sustainment (Ongoing)**

#### **Weekly Activities**

- Review daily health check alerts
- Address any flagged issues
- Monitor alarm performance KPIs

#### **Monthly Activities**

- Database maintenance and optimization
- License consumption review
- Performance tuning
- Operator feedback review

#### **Quarterly Activities**

- Comprehensive health assessment
- KPI trending and analysis
- Compliance audit (Stage J - ISA 18.2)
- Identify continuous improvement opportunities

#### **Annual Activities**

- Formal audit of alarm system (ISA 18.2 Stage J)
- Alarm Philosophy review and update (Stage A)
- Rationalization review (Stage C)
- Training refresher for operators and engineers

---

## **12. Recommendations and Future Considerations** (2-3 pages)

### **12.1 For Plant Operations**

#### **12.1.1 Building Internal Expertise**

- **Invest in alarm management training and certification**
- **Develop internal alarm management champions**
- **Cross-train control system engineers on alarm management**
- **Document lessons learned and institutional knowledge**

#### **12.1.2 Continuous Improvement Programs**

- **Establish regular alarm system audits** (ISA 18.2 Stage J)
- **Bad Actor alarm identification and remediation**
- **Operator feedback mechanisms**
- **KPI tracking and trending**

#### **12.1.3 Standards Compliance Commitment**

- **Formal Alarm Philosophy development/update** (ISA 18.2 Stage A)
- **Target ISA 18.2 "Very Likely to be Acceptable" KPIs:**
  - ~1 alarm per 10 minutes per operator (average)
  - <1% of hours with more than 30 alarms
  - <1% of time in flood conditions
- **Regular rationalization reviews** (Stage C)
- **Robust MOC procedures** (Stage I)

### **12.2 For Vendors (Honeywell and Industry)**

#### **12.2.1 Product Development Priorities**

- **Achieve full ACM feature parity before End of Support (Dec 31, 2027):**
  - Tags import/export functionality
  - EMDB import/export capabilities
  - Ability to move tags between consoles
  - TagSync functionality restoration
- **Develop built-in health monitoring and alerting**
- **Provide automated cleanup and maintenance tools**
- **Implement full import/export capabilities**
- **Add replication support with comprehensive documentation**

#### **12.2.2 Support Enhancement Needs**

- **Replication support commitment** (currently "not supported by Honeywell")
- **Enhanced SLAs for critical issues** (defined response times)
- **Proactive notification of known issues affecting customers**
- **On-site support availability for complex deployments**
- **Migration support beyond "migration utility usage"**

#### **12.2.3 Documentation Improvements**

- **Complete, accurate installation and configuration guides**
- **Backup/restore procedures ensuring deterministic restore**
- **Comprehensive troubleshooting guides** (based on 32+ knowledge articles in 2025)
- **Best practices documentation** (not just feature descriptions)
- **Strong emphasis on pre-migration cleanup requirements**
- **Migration-specific documentation** (not just "new system installation")

#### **12.2.4 Quality Assurance**

- **Testing against customer-scale deployments before GA release**
- **Provide upgrade validation scripts to customers**
- **Document known limitations and workarounds clearly**
- **Address knowledge article findings in product roadmap**

### **12.3 For Industry (User Community)**

#### **12.3.1 Best Practice Sharing**

- **Revitalize ASM (Abnormal Situation Management) Consortium**
- **Establish active Honeywell Alarm Management user groups**
- **Regular meetings to share challenges, solutions, best practices**
- **Collaborative development of deployment standards**
- **Vendor participation and responsiveness to user feedback**

#### **12.3.2 Industry Standards Evolution**

- **Contribute lessons learned to ISA 18.2 updates**
- **Participate in EEMUA 191 revision efforts**
- **Develop migration-specific guidance for standards bodies**
- **Address cloud and virtualization considerations in standards**

#### **12.3.3 Insurance and Regulatory Incentives**

- **Expand insurance company programs:**
  - Premium discounts for ISA 18.2 / EEMUA 191 compliant sites
  - Premium increases for sites without formal alarm management programs
  - Regular audits required to maintain favorable rates
- **Regulatory mandates:**
  - Alarm management standards compliance in process safety regulations
  - Include alarm system performance in incident investigations
  - Require alarm management programs as part of operating permits

---

## **13. Conclusion** (1-2 pages)

### **13.1 Summary of Critical Success Factors**

**The migration from ACM to APO is not simply a software upgrade—it is a transformational alarm management initiative.** Success requires:

1. **Thorough Pre-Migration Cleanup** (6-12 months)

   - ACM and M&R database health assessment and remediation
   - EMDB integrity verification and correction
   - License optimization (cannot reclaim excess licenses later)
2. **Essential Custom Solutions**

   - Daily automated health checks (not included in standard delivery)
   - Active Sync and Suppressed Sync enhancements (required for accurate KPIs)
   - ACM Maintenance solution (for reliability)
   - Asset management tools
3. **Subject Matter Expert Involvement**

   - Alarm management expertise required throughout migration
   - Not just an IT project or vendor-led installation
4. **Realistic Timeline and Resources**

   - 6-12 months pre-migration preparation
   - 2-4 weeks migration execution per site
   - 30-90 days post-migration stabilization
   - 25-30% buffer for unknowns
5. **Comprehensive Testing Before Cutover**

   - Hierarchy, enforcements, Alarm Help, reporting
   - Operator acceptance testing
   - Performance benchmarking
6. **Industry Standards Compliance**

   - ISA 18.2 Lifecycle Model adherence
   - EEMUA 191 KPI maintenance or improvement
   - Migration as opportunity to close compliance gaps
7. **Continuous Improvement Commitment**

   - Regular database maintenance
   - Performance monitoring and optimization
   - Operator feedback incorporation
   - Long-term sustainment planning

### **13.2 The Path Forward**

**For those embarking on ACM to APO migration:**

- Use this whitepaper as your roadmap
- Avoid the pitfalls documented in Section 8
- Invest in pre-migration cleanup (it will save time and cost overall)
- Don't rely solely on vendor tools—plan for essential custom solutions
- Engage alarm management expertise early and throughout

**For the industry:**

- Share lessons learned through user groups and ASM Consortium
- Demand better from vendors (product quality, documentation, support)
- Advocate for regulatory and insurance incentives for standards compliance
- Continue advancing alarm management as a critical safety discipline

**For vendors:**

- Listen to customer feedback from early adopters
- Close the gap between standard delivery and operational excellence
- Support replication and other missing functionality
- Improve documentation and customer enablement

### **13.3 Call to Action**

**ACM End of Support is December 31, 2027.** The clock is ticking for hundreds of plants worldwide. Those who start planning now, conduct thorough pre-migration cleanup, and implement essential custom solutions will achieve successful migrations. Those who wait until the deadline or underestimate the complexity will face rushed migrations, compromised quality, and operational issues.

**The choice is yours: migration by design or migration by desperation.**

This whitepaper provides the knowledge and framework to choose the former. Use it well.

---

## **Appendices**

### **Appendix A: Pre-Migration Assessment Checklist**

*(Comprehensive checklist with ~100 items covering database health, data quality, licensing, dependencies)*

### **Appendix B: ACM Database Cleanup Scripts and Procedures**

*(Sample SQL queries and scripts for identifying and remediating common database issues)*

### **Appendix C: Testing and Validation Checklists**

*(Detailed checklists for pre-migration testing, migration validation, and post-migration verification)*

### **Appendix D: Daily Health Check Configuration Examples**

*(Sample scripts, queries, and configuration for implementing automated health checks)*

### **Appendix E: Sample Migration Project Plan**

*(Gantt chart and detailed task list for 6-12 month migration project)*

### **Appendix F: Glossary of Terms**

*(Definitions of ACM, APO, EMDB, ghost tags, rationalization, enforcement, etc.)*

### **Appendix G: References and Additional Resources**

- ISA 18.2-2016 "Management of Alarm Systems for the Process Industries"
- EEMUA 191 Edition 3 (2013) "Alarm Systems - Guide to Design, Management, and Procurement"
- IEC 62682 (2014) "Management of Alarm Systems for the Process Industries"
- Honeywell Guardian Newsletter Q3 2025
- Honeywell Alarm Management Standards Whitepaper
- APO R3.0.0 Release Notes and Documentation
- ASM Consortium resources (www.asmconsortium.org)

### **Appendix H: Alternative Active Sync Implementation Guide**

*(Step-by-step implementation of Barbara Schubert's file-based Active Sync method)*

- Configuration requirements
- Script templates (ActiveSync_GenerateFilesForDynAMo, PPS mapping)
- Notifdump file generation procedures
- Windows Task scheduling
- Validation and testing procedures
- Quality comparison: Standard vs. Alternative sync

### **Appendix I: Vendor Contact Information and Escalation Procedures**

*(Honeywell Technical Support contacts, escalation paths, SLA reference)*

### **Appendix J: About the Authors**

*(Detailed credentials, experience, and contact information for authors and contributors)*

---

**End of Outline**

---

## Notes for Development

**Sections Requiring Additional Detail:**

- Case studies in Section 8.4 (need anonymous real-world examples)
- Sample scripts in Appendix D (health check implementations)
- Gantt chart in Appendix E (migration project timeline)
- Detailed checklists in Appendices A, B, C

**Content to Validate with Barbara Schubert:**

- Technical accuracy of custom solutions descriptions (Section 7)
- Health check implementation details (Section 6.2)
  	Sample health check emails, hierarchy health check scripts etc
- Cleanup procedures (Section 3.5)
  	Will show scripts outcomes
- Timeline estimates (Section 10)

**Graphics and Tables to Develop:**

- Feature parity comparison table (ACM vs. APO)
- Sync quality comparison table (Standard vs. Alternative Active Sync)
- ISA 18.2 Lifecycle Model diagram
- Migration timeline Gantt chart
- Health check architecture diagram
- Decision tree for migration approach selection
- M&R data flow diagrams (from PPTX Slide 14)
- Active Sync data flow comparison (Standard vs. Alternative, PPTX Slides 56-57)
- Syncing architecture diagram (Experion vs. ESVT/TPS, PPTX Slide 16)

**Next Steps:**

1. Review and refine outline with stakeholders
2. Begin drafting sections (suggested order: 1, 2, 3, 8, 10)
3. Validate technical content with Barbara Schubert
4. Develop appendices and checklists
5. Create graphics and diagrams
6. Conduct peer review
7. Final editing and formatting
8. Publication and distribution
