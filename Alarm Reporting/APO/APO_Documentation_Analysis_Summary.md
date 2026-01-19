# APO Documentation Analysis Summary

**Date:** January 16, 2026  
**Analysis of:** GuardianNewsletterQ32025.pdf, honeywell-alarm-management-standards-whitepaper.pdf, MPC APO Deployment Cookbook.docx, Potential additions to the Standard HAM delivery (Barbara Schubert).docx

---

## Executive Summary

This analysis examines four critical documents related to Honeywell Alarm Management systems, focusing on Alarm Performance Optimizer (APO) R3.0.0, industry standards (ISA 18.2 and EEMUA 191), and Marathon Petroleum Corporation's internal deployment best practices. The findings reveal significant gaps between vendor-delivered solutions and operational requirements, highlighting the need for enhanced quality controls, better documentation, and more robust deployment practices.

**Key Findings:**
- APO R3.0.0 introduces critical capabilities (ACM migration, constraints, offline rationalization, DeltaV support)
- Significant product lifecycle changes: ACM End of Life extended to December 31, 2027
- Marathon-developed enhancements address critical gaps in vendor-provided functionality
- Industry standards (ISA 18.2, EEMUA 191) provide clear KPIs that many plants fail to meet
- Deployment quality depends heavily on pre-migration cleanup and custom health monitoring solutions

---

<div style="page-break-after: always;"></div>

## 1. Guardian Newsletter Q3 2025 - Product Updates and Support Changes

### 1.1 Critical Product Lifecycle Changes

**ACM (Alarm Configuration Manager) End of Life Extension:**
- **Extended Support Timeline:** Phased-Out Support now begins December 31, 2026 (12-month extension from original date)
- **Final End of Support:** December 31, 2027
- **Rationale:** Allow customers sufficient time for ACM to APO migration
- **Key Dates:**
  - December 31, 2025: End of Sale (no new ACM sales)
  - December 31, 2026: Beginning of Phased-Out Support (limited TAC support, no enhancements)
  - December 31, 2027: End of Support (no TAC, no defects fixed, no development)

**Other Product Support Changes:**
- DynAMo Metrics & Reporting R210.x: Phased-Out in May 2025
- Process Safety Analyzer R20x: Phased-Out in January 2025
- Alarm Configuration Manager R321: Phased-Out in December 2026

### 1.2 APO R3.0.0 New Features (Due August 2025)

#### ACM to APO Migration
**Three-Phase Migration Process:**
1. **Pre-migration:** Configure essential components, secure site environment
2. **Migration:** Validate, map, and migrate data using utility tools
3. **Post-migration:** Conduct reviews, ensure data integrity with validation tools

**Key Capability:** "Seamless migration from ACM to APO with built-in validation and flexibility"

#### Constraints Feature
- **Purpose:** Validate alarm limits against constraint values during proposed changes
- **Functionality:** Prevents changes if proposed alarm limit exceeds constraint (error triggered, change blocked)
- **Value:** Enforces engineering limits to prevent unsafe or inefficient alarm configurations

#### Offline Rationalization
- **Capability:** Update multiple alarm-related variables outside APO Web UI using Excel
- **Workflow:**
  1. Export data with filters
  2. Edit or add entries in Excel
  3. Import back to APO
  4. System processes changes, updates valid records, unlocks modified alarms, flags invalid entries
- **Reporting:** Detailed import/export status and error logs provided

#### Tag Suspend/Resume
- **Purpose:** Temporarily suspend tag enforcement from APO to DCS during planned maintenance
- **Benefits:** Prevents unwanted overwrites during known data changes
- **Functionality:** Enforcement paused for defined time window, automatically or manually resumed

#### DeltaV DCS Integration
- **New Support:** APO now supports DeltaV Control System integration
- **Capabilities:**
  - Import and synchronization of tags and alarm properties from DeltaV systems into APO
  - Modification and rationalization of tag and alarm properties within APO
  - MOC (Management of Change) process for tag approval and release
  - Exception reports to track differences between DCS and master alarm database

#### Mode-Based Enforcement via AMS_Proxy
- **Capability:** Automatic mode changes without manual action, triggered from DCS Server using command-line parameters
- **Requirements:** AMS_Proxy installed on server within same domain as APO Site with .NET Framework 4.8
- **Functionality:** Connects to APO Site and enforces defined mode on specified assets and consoles

### 1.3 Product Family Consolidation

**Process.Honeywell.com Changes:**
All legacy product families consolidated under **"Honeywell Alarm Mgmt"** product family:
- AAM - Alarm Management → Alarm Configuration Manager
- DynAMo → DynAMo Metrics & Reporting, DynAMo UserAlert
- Honeywell Forge Alarm Management → APO, Reporting, Process Safety Analyzer

**Impact:** Knowledge article searches and Technical Support Requests must now use "Honeywell Alarm Mgmt" product family filter

### 1.4 Critical Technical Issues

#### Experion R520/530 Upgrade Data Corruption
**Issue:** Upgrading Experion DCS to R520+ from earlier versions causes data corruption in DynAMo M&R and HAM-Reporting:
- **Extra/Invalid Tagnames:** Affects licensed tag-count limit
- **Extra Assets:** Negatively impacts report performance
- **Reference:** Knowledge articles KSM2022-DYN003x and 000189115
- **Recommendation:** Contact Honeywell Alarm Management GTAC before migrating to Experion R520+

#### Experion R520/530 Kerberos Encryption Changes
**Issue:** Experion 520+ recommends new encryption types (AES256_HMAC_SHA1, AES128_HMAC_SHA1) for Kerberos authentication
- **Impact:** ACM clients cannot connect to application server if compatibility not achieved
- **Cause:** Authentication problems during DCOM communication between client and server
- **Resolution:** Knowledge article pending publication
- **Action:** Contact GTAC if experiencing connection issues

### 1.5 Knowledge Article Summary

**32 Knowledge Articles Published in 2025** covering:
- ACM (Alarm Configuration Manager) issues and resolutions
- APO (Alarm Performance Optimizer) functionality and troubleshooting
- DynAMo M&R and HAM Reporting issues
- Process Safety Analyzer problems and solutions
- SQL Server compatibility and configuration
- ODBC connection failures
- License activation errors
- Database corruption and performance issues

**Common Themes:**
- SQL Server version compatibility issues (SQL 2022 not fully supported in some versions)
- ACM Tag Synchronization failures
- APO Transfer Service becoming unresponsive
- M&R collector connection failures
- PSA (Process Safety Analyzer) data processing delays

---

<div style="page-break-after: always;"></div>

## 2. Honeywell Alarm Management Standards Whitepaper - Industry Standards and Best Practices

### 2.1 Executive Overview

**Key Message:** 30+ years after Honeywell formed the Alarm Management Task Force, many companies still lack formal Alarm Management programs or fail to take alarm management seriously.

**Industry Impact:**
- **Longford Gas Explosion (1998):** Partly attributed to poor alarm management
- **Texas City Oil Refinery Explosion (2005):** Alarm management failures contributed
- **Deepwater Horizon Oil Platform (2010):** 11 deaths, $60+ billion in fines/settlements, worst U.S. environmental disaster

**Business Drivers:**
- **Insurance:** Some insurers threaten premium increases for plants without active alarm management programs, or offer discounts for those with programs
- **Legal Liability:** Corporate executives and supervisors have been legally prosecuted for industrial accidents and safety/environmental breaches
- **Duty of Care:** OHS legislation mandates employers provide suitable alarm systems for adequate warning of abnormal situations

### 2.2 Core Standards

#### ISA 18.2-2016 "Management of Alarm Systems for the Process Industries"
**Key Features:**
- Large focus on alarm system lifecycle
- Very clear alarm system performance KPIs
- Conformance requirements section
- Alarm Philosophy purpose and contents
- Alarm System requirements specification
- Enhanced and advanced alarm methods

#### EEMUA 191 Edition 3 (2013) "ALARM SYSTEMS - Guide to Design, Management, and Procurement"
**Key Features:**
- Good detail on alarm design, including risk assessment approaches
- Written in text-book format with excellent examples
- Discussion on Alerts vs. Alarms
- HCI management techniques
- Alarm configuration, processing, testing, suppression techniques
- Performance monitoring/improvement with benchmark values
- Appendix on costs of poor alarm performance
- Appendix on alarm management in Batch Plants

#### IEC 62682 (2014)
- Internationalized adaptation of ISA 18.2
- Recognized as international standard based on ISA 18.2

### 2.3 Alarm Management Definition

**EEMUA 191 Definition:** "The processes and practices for determining, documenting, designing, monitoring, and maintaining alarm system" to ensure safe, reliable operations.

**ISA 18.2 Alarm Definition:** "An audible and/or visible means of indicating to the operator an equipment malfunction, process deviation, or abnormal condition requiring a timely response."

**Key Principle:** An alarm notifies the operator that something in the process has occurred which has undesirable consequences and requires operator action to mitigate the issue in a timely manner.

### 2.4 Layers of Protection (LOP)

**Alarm Management as a LOP:**
- Provides independent protection around hazardous processes
- Used in Safety Integrity Level (SIL) analysis
- Warns operators of impending abnormal situations with safety-related consequences
- **Critical Consideration:** Probability of operator failure to adequately respond must be considered in SIL loop calculations
- **Risk:** Unrealistic probability of failure assignments, especially where alarm rates exceed "maximum manageable" metrics, make SIL designs inaccurate

### 2.5 Why Alarm Management Matters

#### People (Safety)
- Protecting employees, visitors, and surrounding community
- Primary function of alarm system: identify situations posing health/safety risk
- Notify operations in time to address situation and alert personnel

#### Planet (Environment)
- Environmental releases carry health risks and hefty fines
- Increased sensors/analyzers to monitor potential releases of regulated substances
- Alarm systems configured to recognize and alert to conditions leading to potential releases

#### Profits (Business)
- Poorly configured alarm systems lead to:
  - Unnecessary shutdowns
  - Quality issues
  - Equipment damage
  - Production deferment
- Potential financial impacts from fines or litigation
- Reputation and viability risks in competitive markets

**Cost of Abnormal Situations:** Millions or billions of dollars annually across industry

### 2.6 Common Issues Impacting Alarm Management

#### 1. Failure to Correctly Identify an Alarm
**Problem:** Proliferation of "alarms" that fail to meet the definition of an alarm per industry standards
**Root Cause:** Modern control systems make adding alarms easier and less costly, leading to unnecessary alarm configurations
**Example:** Alarm system should NOT notify operator that pump started when supposed to, but rather that pump was supposed to start but did not

#### 2. Poor Process Control Logic and/or Configuration
**Impact:**
- Large numbers of Bad Actor alarms (unnecessary, chattering, duplicate, nuisance alarms)
- Increased operator actions required to control process
- Diminished operator situational awareness
- Missed or overlooked alarms
- Standing and stale alarms
- Operators shelving/inhibiting nuisance alarms for extended periods (weeks/months) without plans to address root cause

#### 3. Equipment Malfunction or Failure
**Problem:** Over-reliance on higher LOPs (safety systems, pressure relief valves)
**Impact:** Poorly maintained equipment/instruments result in nuisance alarms (fleeting, chattering, false alarms)
**Risk:** Increased probability of avoidable incidents

#### 4. No or Poor Alarm Rationalization
**Problem:** Many companies fail to follow ISA 18.2 or EEMUA 191 guidelines for proper Alarm Rationalization
**Alarm Rationalization Process:** Assign alarm priority based on analysis of:
- Cause of alarm
- Consequence if no action taken
- Severity of consequences (Risk Assessment Matrix)
- Maximum Time to Respond for operator to prevent consequences
- Corrective Actions operator should take to mitigate situation

**Impact:** Confusing display of alarms that hinder operator situation awareness, increasing likelihood that critical alarm is missed or incorrect actions are taken

**Result:** "When the alarm system is needed most, operators ignore the alarms because they are overwhelmed with confusing information, and the alarm system becomes virtually unusable"

### 2.7 Alarm Performance KPIs

#### EEMUA 191 KPIs (per operator, 10-minute periods)

**Average Alarm Rate:**

| Alarms per Hour | Alarms per 10 Minutes | Acceptability |
|-----------------|----------------------|---------------|
| >60 | >10 | Very likely to be unacceptable |
| 30 | 5 | Likely to be over-demanding |
| 12 | 2 | Manageable |
| <6 | <1 | Very likely to be acceptable |

**Maximum Alarm Rate Following Plant Upset:**

| Alarms in 10 Minutes | Acceptability |
|---------------------|---------------|
| More than 100 | Definitely excessive, very likely to lead to operator abandoning system |
| 20-100 | Hard to cope with |
| Under 10 | Should be manageable (but may be difficult if several require complex operator response) |

**Additional EEMUA Targets:**
- Standing alarms: <10 for sites with >1000 configured alarms
- Shelved alarms: <30 (excluding maintenance shelved alarms)
- % of time alarm rates outside "Very likely to be acceptable": <10%

#### ISA 18.2 KPIs (Very Clearly Defined)

| Metric | Target Value: Very Likely to be Acceptable | Target Value: Maximum Manageable |
|--------|-------------------------------------------|--------------------------------|
| Annunciated Alarms per 10 Minutes per Operating Position | ~1 (average) | ~2 (average) |
| % of hours containing more than 30 alarms | <1% | - |
| % of 10-minute periods containing more than 5 alarms | <1% | - |
| Maximum number of alarms in 10-minute period | 10 or less | - |
| % of time alarm system in flood condition | <1% | - |
| % contribution of top 10 most frequent alarms | 1% to 5% maximum (with action plans) | - |
| Quantity for chattering and fleeting alarms | Zero (action plans for any that occur) | - |
| Stale Alarms | <5 present on any day (with action plan) | - |
| Annunciated Priority Distribution (3 priorities) | ~80% Low, ~15% Medium, ~5% High | - |
| Annunciated Priority Distribution (4 priorities) | ~80% Low, ~15% Medium, ~5% High, <1% Highest | - |
| Unauthorized Alarm Suppression | Zero outside controlled/approved methodologies | - |
| Improper Alarm Attribute Change | Zero outside approved methodologies or MOC | - |

### 2.8 ISA 18.2 Lifecycle Model

**Ten Stages in Three Loops:**

#### Outer Loop (Philosophy & Audit)
- **Stage A: Philosophy** - Documents site approach to alarm management (mandatory requirement)
- **Stage J: Audit** - Periodic audit of alarm system and processes

#### Implementation Loop
- **Stage B: Identification** - Determine if alarm required (PHA, HAZOP, incident investigations)
- **Stage C: Rationalization** - Reconcile each alarm against philosophy principles and requirements
- **Stage D: Detailed Design** - DCS/PLC configuration, HMI design, advanced methods
- **Stage E: Implementation & Training** - Testing, training, commissioning
- **Stage I: Management of Change** - Structured approval/authorization for alarm additions, modifications, deletions

#### Operations Loop
- **Stage F: Operation** - Alarm in service, reporting abnormal conditions
- **Stage G: Maintenance** - Periodic/predictive maintenance of instruments, final control elements, control systems
- **Stage H: Monitoring & Assessment** - Periodic data collection and analysis, reports identifying nuisance alarms, stale alarms, floods

### 2.9 Steps to Achieve Compliance

1. **Purchase ISA 18.2 and/or EEMUA 191**
2. **Undertake Alarm System Audit:**
   - Benchmark current alarm system performance
   - Identify deficiencies and areas needing improvement
   - Establish reference point to measure improvements
3. **Get Senior Management Sponsorship:**
   - Present operator survey results
   - Show Bad Actor analysis report
   - Compare plant KPIs with ISA 18.2/EEMUA 191 requirements
4. **Prepare Strategic Plan:**
   - Alarm Philosophy Document Development
   - Functional Specifications
   - Purchase alarm database and software tools
   - Identify and rationalize Top 20 most frequent alarms OR classic rationalization of all alarms
   - 12-24 month project plan with milestones
   - Required training (engineers, technicians, operators)
5. **Implement Strategic Plan**

---

<div style="page-break-after: always;"></div>

## 3. MPC APO Deployment Cookbook - Marathon Internal Best Practices

**Author:** Barbara Schubert (bschubert@marathonpetroleum.com)  
**Version:** V0.2, December 14, 2025  
**Purpose:** Document recommendations and deployment standards for ACM to APO migration

### 3.1 Critical Pre-Migration Requirements

#### Clarify Licensing Requirements BEFORE Ordering
**Key Issue:** If license calculated too high, it is not possible later to reclaim unnecessary licenses
**Prerequisites:**
1. Clean ACM (see detailed cleanup requirements below)
2. Clean M&R (Metrics & Reporting)

### 3.2 ACM Cleanup Requirements

#### Remove Non-Alarmable Tags
- Tags not in DCS
- Tags with invalid structure
- SCADA tags (if corrupted)

#### Data Quality Issues to Address
- Corrupted notes
- Invalid parameters
- Tag descriptions incorrect
- Tags in wrong assets

#### Consider Reverse Enforcements
**Scenario:** Where DCS is still master (e.g., Dead Band Units may only be controlled/changed on DCS)

### 3.3 M&R (Metrics & Reporting) Cleanup Requirements

#### Merge Tags Causing Unnecessary License Consumption
**Example:** History Index 200, History Index 201, etc.
**Impact:** Cases where such tags caused 10,000+ spike in license consumption in just ~20 minutes

#### Delete Ghost Tags
- Tags that do not have events in M&R anymore
- Old/ghost tags (license savings)

#### Consider Retention Changes
**Question:** Should retention periods be adjusted to reduce licensing and improve performance?

### 3.4 APO Limitations Requiring ACM Cleanup

**Critical Statement:** "APO is currently mainly enhanced Rationalization tool with enforcements similar to ACM. APO is still missing critical Alarm Management tools that will make adjustments more challenging so cleanup before migration is critical."

**Missing Functionality in APO (vs. ACM):**
- Tags import/export (only import/export to Excel rationalization tool supported)
- EMDB import/export (only manual individual creation of assets supported)
- Move tags to other consoles
- TagSync functionality

### 3.5 Recommended Cleanup Process

**Install Temporary ACM Components:**
- Manager Server
- Enforcer Server (does not need dedicated server, can be installed on client/station)
- **Purpose:** Allow cleanup without affecting current operations (alarm help, enforcement)

**Cleanup Steps:**
1. Clean EAS EMDB and load to ACM
2. Move tags to correct assets
3. Export and delete tags with invalid structure
4. Delete CMs (if not used)
5. Clean known corruptions:
   - SCADA tags
   - Corrupted notes
   - Invalid parameters
6. Ensure tag descriptions correct
7. **CRITICAL:** Health check ACM DB before migration

### 3.6 Installation Best Practices

**Follow Marathon Standards During Install:**
- SQL permissions/configuration
- Schema name conventions
- Folders locations/names
- Database migration procedures
- Assets migration
- System configuration
- Backup standards (to ensure DETERMINISTIC restore)
- Notifications configuration

**Application Configuration:**
- Updates to custom solutions (e.g., OL best practices)
- ACM running in parallel (critical for sites with enforcements, especially dynamic mode enforcements)

### 3.7 Delta Migration and Parallel Operations

**Critical for Sites with Enforcements:**
- Especially dynamic mode enforcements
- **Question:** "How to delta migration..." (process not fully documented)

### 3.8 Testing Requirements

**Most Important Testing Points:**
- Hierarchy is correct
- No errors in enforcements
- (Additional testing points not fully detailed in cookbook)

### 3.9 Decommissioning ACM

**Process:** Not fully detailed in cookbook (marked as "Hints" section needing completion)

### 3.10 Gaps and Missing Information

The cookbook explicitly notes several areas still under development:
- "TODO: Instructions how to clean without affecting current operations"
- "What is still missed..."
- "HowTo..."
- "etc"

**Interpretation:** This cookbook is a work-in-progress document capturing lessons learned and best practices as Marathon deploys APO across multiple sites.

---

<div style="page-break-after: always;"></div>

## 4. Potential Additions to Standard HAM Delivery - Marathon Enhancement Solutions

**Author:** Barbara Schubert (bschubert@marathonpetroleum.com)  
**Date:** September 18, 2025  
**Scope:** Documents additions to HAM delivery implemented by Barbara Schubert at one or more Marathon sites to ensure quality, easy maintenance, and usability

### 4.1 Core Problem Statement

**Key Insight:** "Reporting is collecting and produces reports on schedule... ACM can do enforcements and shows alarm help... It does not mean the system works well and provides optimal value!"

**Impact of These Solutions:**
- Quality of reporting and ACM alarm help
- More effective usage of standard functionality
- Immediate savings (e.g., reduce license needs and maintenance effort)
- Daily automated health checks (prevents months of frustration before issues are reported, weeks to identify source)

### 4.2 Critical Solution: Daily Automated Health Checks

**Category:** COMMON SENSE addition every site should have

#### Benefits Beyond HAM
**Discovered Issues in Other Systems:**
- TPS wrong timestamps
- TPS unit mapping errors
- Experion Points incorrectly assigned
- Duplicate points
- Unassigned points
- Other system misconfigurations

#### Health Check Categories

**1. ACM Health Checks:**
- ACM replication heartbeat
- No collection
- No suppress sync
- No active sync
- No disk space
- No database backups
- No reports delivered (checked hourly, failure email sent)
- No reports generated on schedule
- No enforcements
- User closed activities (note: "should not be required if there is quality!")
- Hierarchy needs attention (new paths, tags in wrong assets)
- Hierarchy does not match (Reporting vs. ACM)
- ACM Tag Sync failures/monitoring (optionally marking tags needing attention)
- ACM Enforcements stuck (optional automatic recovery)
- ACM Maintenance notification
- ACM fully customizable enforcement reports
- ACM DB quality

**2. DCS Issue Detection:**
- Active Sync opened too many alarms
- Active Sync opened very old alarm
- Other notifications indicating DCS issues

**3. License Management:**
- Duplicate tags
- Licensing notifications (include information on potential reduction)

**4. Critical Event Notifications:**
- Alarms were DISCARD-ed
- Enforcements failed with specific errors

### 4.3 ACM Maintenance Solution

**Purpose:** Reliability of ALARM HELP and ENFORCEMENTS

**Combines Information from Multiple Sources:**
1. Database
2. Enforcements
3. TagSync (reconfiguration, add/delete, SCADA maintenance)
4. Reporting (e.g., detects tags that alarmed but are not in ACM)

**Functionality:**
- Clearly mark tags needing deterministic attention
- Tags may need to be moved, reloaded, deleted, or released

### 4.4 "Reverse Enforcements" Tools

**Purpose:** Keep ACM and DCS in sync when DCS is master for certain parameters
**Example:** Dead Band Units may only be controlled/changed on DCS

### 4.5 Meaningful Backup and Purge

**Coordinated and Complete Backups:**
- Ensure deterministic restore
- **Issue:** Standard instructions do not ensure deterministic restore

**Effective Purge:**
- Removes unnecessary data while preserving critical information

### 4.6 Asset Management Tools

**Purpose:** Streamline asset management, ensure assets in HAM match Experion and customer needs

**Automatic Comparisons of EMDBs:**
- Cleanup of EMDBs
- **Finding:** Tool usually finds issues in EMDBs at site
- Provides deterministic way to ensure EAS EMDB and HAM-R hierarchy integrity

**Automatic Construction of Code for Reporting:**
- Some setups require asset mapping for reporting quality

### 4.7 Quality of Reporting Tools

#### Full Active Sync
**Developed:** Barbara Schubert and LAR in 2021, critical additions added 2025

**Features:**
- Sync shelved alarms
- Sync system alarms
- Additions to work around many M&R limitations:
  - Sync DAS (Distributed Alarm Server)
  - Sync CUTOUT
  - Maintenance tools

#### Full Suppressed Sync
**Includes:**
- Additional columns with suppress value (meaningful user info)
- Ability to filter (standard functionality does not provide)
- **Impact:** Without this solution, not only Suppressed report but also KPIs are not accurate

#### Additional Sync Capabilities
- Sync Enable/Disable/Inhibit/JournalOnly
- Sync Inactive
- Fill Shelved, Suppressed, Visible columns (delivered as part of Active Sync, Shelved Sync, and Suppressed Sync improvements)

### 4.8 Adjustments to Default Settings in Rules

**Issue:** "Below is the fragment from HAM standard rules. It lists many adjustments that should be considered/validated to ensure quality. These options are left at defaults at sites while adjustments are important for quality."

**Maintenance:** Rules continuously updated as needed and adjusted for new releases

### 4.9 Custom Filtering/Reporting (Every Site Should Consider)

**Alarm Class Filtering:**
- Critical filtering option every site should have
- Normal and Current Mode (including sync of Normal, Current, and INACTIVE)

**Normal and Current Mode Reporting:**
- Daily Reporting of differences (lists)
- Charts to visually compare and show progress over time
- Enhanced management using ACM Tag Sync
- Notifications showing which tags need to be reloaded and why
- Exclusion Lists auto-management
- Mark tags needing to be deleted, moved, or reloaded

### 4.10 Services Every Site Would Benefit From

#### 1. Reduce License Requirements, Improve Performance, Prevent Failures
**Actions:**
- Remove ghost (old) and invalid tags
- Prevent ghost/invalid tags in future

#### 2. Replication Support (ACM and Reporting)
**Issue:** "Marathon does not have a resource to support replication. It is not supported by Honeywell."

#### 3. Cleanup of ACM DB (Important Before Migration to APO!)
**Tasks:**
- Invalid tags
- Tags in wrong assets
- Tags with no alarms
- Corrupted parameters + SCADA cleanup
- Adjustments to improve usage

#### 4. Cleanup of M&R DB
**Tasks:**
- Old/ghost tags (license savings)
- Old assets (or corrupted assets)
- Paths re-arrangements/optimization and cleanup
- Improving quality and performance:
  - Closing invalid alarms in DB
  - Removing invalid suppressed
  - Merging tag descriptions

#### 5. HAM-R: Assistance in Incident Analysis
**Capability:** Queries superior to M&R Reports can extract events in more effective format

#### 6. Consulting/Training/Reconfiguration for Effective Usage
**Examples:**
- Enforcements in audit mode
- Reverse enforcements
- Easy way to delete tag lists from ACM or clean asset assignments
- Audit workflow when not all units ready for Enforcements yet

### 4.11 Author Credentials and Value Proposition

**Barbara Schubert's Experience:**
- 27 years in Alarm Management as developer (including designing and maintaining ACM database)
- 27 years as project engineer
- 10+ years as the only Automation College instructor

**Value:** Experience provides good foundation for effective consulting and analyzing what is possible

---

<div style="page-break-after: always;"></div>

## 5. Critical Gaps Analysis - Vendor Delivery vs. Operational Requirements

### 5.1 Fundamental Issues with Vendor-Delivered Solutions

#### APO Feature Gaps (vs. ACM)
**Missing Critical Functionality:**
- No tags import/export capability (only Excel rationalization tool)
- No EMDB import/export (only manual individual creation)
- No ability to move tags to other consoles
- No TagSync functionality
- No automated cleanup tools
- No built-in health monitoring
- No replication support ("It is not supported by Honeywell")

**Impact:** "APO is currently mainly enhanced Rationalization tool with enforcements similar to ACM. APO is still missing critical Alarm Management tools that will make adjustments more challenging so cleanup before migration is critical."

#### HAM Reporting Quality Issues
**Without Marathon-Developed Enhancements:**
- Active Sync incomplete (does not sync shelved, system alarms, DAS, CUTOUT, Enable/Disable/Inhibit/JournalOnly, Inactive)
- Suppressed Sync incomplete (missing suppress value columns, filtering capabilities)
- **Critical Impact:** "Without this solution not only Suppressed report but also KPIs are not accurate"
- M&R limitations require workarounds

### 5.2 Deployment Quality Dependencies

#### Pre-Migration Requirements Not Emphasized by Vendor
**Marathon-Identified Critical Steps:**
1. Clean ACM DB (invalid tags, wrong assets, corrupted parameters, SCADA cleanup)
2. Clean M&R DB (ghost tags, old assets, path cleanup)
3. Clarify licensing BEFORE ordering (cannot reclaim excess licenses later)
4. Health check ACM DB before migration
5. Install temporary ACM Manager/Enforcer for cleanup without disrupting operations

**Vendor Emphasis:** Focus on APO R3.0.0 features (ACM migration utility, constraints, offline rationalization), not on critical pre-migration cleanup

#### Daily Automated Health Checks
**Vendor Delivery:** None
**Marathon Solution:** Comprehensive daily health checks covering:
- ACM replication, collection, syncs, disk space, backups, reports, enforcements
- Database quality
- Hierarchy integrity
- Tag Sync monitoring
- Licensing optimization
- DCS issue detection

**Value:** "These daily health checks helped not only to identify issues in HAM but also in other systems (e.g., TPS wrong timestamps, TPS unit mapping, Experion Points incorrectly assigned, duplicate points, unassigned points etc). They save lots of frustration and troubleshooting time. They catch issues that are easily missed for a long time (e.g., it may be assumed sync channels are working as they are green but... in fact they may not work)."

### 5.3 Support and Expertise Gaps

#### Replication Support
**Marathon Statement:** "Marathon does not have a resource to support replication. It is not supported by Honeywell."
**Impact:** Customers left without support for critical replication functionality

#### Backup/Restore Quality
**Marathon Finding:** "Standard instructions do not ensure deterministic restore"
**Marathon Solution:** "Coordinated and complete backups to ensure deterministic restore"

#### EMDB Quality
**Marathon Finding:** "This tool usually finds issues in EMDBs at site in addition to providing deterministic way to ensure EAS EMDB and HAMR hierarchy integrity"
**Vendor Delivery:** No automated EMDB comparison/cleanup tools

### 5.4 License Management Issues

#### Ghost Tags and License Bloat
**Marathon Finding:** "History Index 200, History Index 201 etc. There were cases when such tags caused 10,000+ spike in license consumption in just ~20 minutes."
**Vendor Delivery:** No automated tools to identify and remove ghost tags
**Marathon Solution:** Tools to remove ghost/invalid tags and prevent them in future

#### License Optimization
**Marathon Solution:** "Licensing notifications (include information on potential reduction)"
**Vendor Delivery:** No proactive license optimization guidance

### 5.5 Migration Complexity and Risk

#### Parallel Operations During Migration
**Critical for Sites with Enforcements:** "ACM running in parallel (critical for sites with enforcements, especially dynamic mode enforcements)"
**Vendor Guidance:** Limited documentation on delta migration process
**Marathon Cookbook:** "How to delta migration..." (process not fully documented even internally)

#### Testing Requirements
**Marathon Cookbook:** Lists "Most important testing points" but provides minimal detail
**Vendor Guidance:** APO R3.0.0 promises "built-in validation" but extent/effectiveness unclear

### 5.6 Training and Knowledge Transfer

#### Effective Usage Not Guaranteed by Installation
**Marathon Statement:** "Consulting/training/reconfiguration to ensure EFFECTIVE USAGE. e.g. Enforcements in audit mode, reverse enforcements, easy way to delete tag lists from ACM or to clean asset assignments etc."

**Implication:** Standard vendor delivery and training insufficient to ensure effective system usage

### 5.7 Industry Standards Compliance Gap

#### Standards Awareness vs. Implementation
**Honeywell Whitepaper:** "More than 30 years after Honeywell formed the Alarm Management Task Force... many companies still do not have a formal Alarm Management program or take the issues associated with Alarm Management seriously."

**Marathon Reality:** Even sophisticated customers like Marathon require custom-developed solutions to achieve quality alarm management, indicating:
- Standard Honeywell delivery does not ensure ISA 18.2/EEMUA 191 compliance
- Tools and processes needed for compliance not included in base product
- Significant expertise (27 years) required to develop effective solutions

---

<div style="page-break-after: always;"></div>

## 6. Recommendations for Marathon and Industry

### 6.1 Immediate Actions for APO Deployment

#### 1. Formalize MPC APO Deployment Cookbook
**Current State:** V0.2, work-in-progress with TODO sections and incomplete "HowTo" content
**Recommendations:**
- Complete missing sections (cleanup procedures, delta migration process, testing checklist, decommissioning steps)
- Add detailed step-by-step instructions for critical procedures
- Include troubleshooting guides for common issues
- Create checklists for each deployment phase
- Version control and maintain as living document

#### 2. Establish Pre-Migration Assessment Process
**Requirements:**
- Formal ACM DB health check procedure
- M&R DB quality assessment
- License consumption analysis
- Identification of ghost tags, invalid tags, corrupted parameters
- EMDB integrity verification
- Current enforcement/alarm help dependencies documentation

#### 3. Deploy Barbara Schubert's Solutions as Standard
**Critical Solutions for All Sites:**
- Daily automated health checks (highest priority)
- ACM Maintenance solution
- Full Active Sync and Suppressed Sync improvements
- Meaningful backup/purge procedures
- Asset management tools (EMDB comparison/cleanup)
- Custom filtering/reporting (Alarm Class, Normal/Current Mode)

#### 4. Enhance Vendor Relationship and Accountability
**Actions:**
- Share MPC APO Deployment Cookbook with Honeywell (where appropriate, considering proprietary Marathon IP)
- Request Honeywell address missing APO functionality (tags import/export, EMDB import/export, move tags to consoles, TagSync)
- Escalate replication support gap
- Request improved backup/restore documentation ensuring deterministic restore
- Request automated license optimization tools
- Request built-in health monitoring capabilities

### 6.2 Long-Term Strategic Recommendations

#### 1. Standardize APO Deployment Across Marathon Sites
**Components:**
- Standard SQL configurations, schema names, folder structures
- Common health check deployment and monitoring procedures
- Unified backup/restore procedures
- Shared knowledge base and lessons learned
- Cross-site support and expertise sharing

#### 2. Develop APO Center of Excellence
**Purpose:** Centralize expertise, tools, and support for alarm management across Marathon
**Functions:**
- Maintain and update deployment standards
- Develop and share custom solutions
- Provide deployment support and troubleshooting
- Conduct post-deployment audits
- Track industry standards evolution (ISA 18.2, EEMUA 191 updates)
- Continuous improvement of alarm management practices

#### 3. Establish Formal ISA 18.2/EEMUA 191 Compliance Program
**Components:**
- Alarm Philosophy development for each site (mandatory per standards)
- Regular alarm system audits (ISA 18.2 Stage J)
- KPI monitoring and reporting (target: ISA 18.2 "Very Likely to be Acceptable" metrics)
- Bad Actor alarm identification and remediation
- Management of Change (MOC) procedures for alarm system changes
- Operator training programs
- Senior management sponsorship and accountability

#### 4. Address Knowledge Transfer and Succession Planning
**Risk:** Barbara Schubert's 27 years of expertise represents single point of failure
**Actions:**
- Document all custom solutions, tools, and procedures
- Train additional resources on custom solutions maintenance and enhancement
- Create Marathon-specific alarm management training curriculum
- Establish mentoring program for alarm management engineers
- Consider hiring or developing additional experts

### 6.3 Vendor Accountability Recommendations

#### 1. Enhanced Service Level Agreements (SLAs)
**Requirements:**
- Define acceptable response times for critical issues (ACM/APO down, enforcements failing, data corruption)
- Establish escalation procedures for unresolved issues
- Include provisions for on-site support when remote troubleshooting insufficient
- Require proactive notification of known issues affecting Marathon deployments

#### 2. Product Quality Requirements
**APO Feature Completeness:**
- Full feature parity with ACM before ACM End of Support (December 31, 2027)
- Built-in health monitoring and alerting
- Automated cleanup and maintenance tools
- Comprehensive import/export capabilities
- Replication support with full documentation

**Testing and Validation:**
- Require Honeywell conduct upgrade testing against Marathon-scale deployments
- Provide upgrade validation scripts to customers
- Document known limitations and workarounds before GA release

#### 3. Documentation and Training Enhancement
**Requirements:**
- Complete, accurate installation and configuration documentation
- Backup/restore procedures ensuring deterministic restore
- Troubleshooting guides for common issues (based on knowledge articles)
- Best practices documentation (not just feature descriptions)
- Customer-specific training addressing Marathon's deployment standards

### 6.4 Industry-Wide Recommendations

#### 1. Standards Adoption and Enforcement
**For Processing Plants:**
- Mandate ISA 18.2 or EEMUA 191 compliance for all alarm management systems
- Conduct regular third-party audits of alarm system performance
- Include alarm management performance in safety management systems
- Establish accountability for alarm management at executive level

**For Vendors (Honeywell and Competitors):**
- Design products for ISA 18.2/EEMUA 191 compliance by default
- Include compliance checking and reporting in base products
- Provide built-in lifecycle management tools (Philosophy, Identification, Rationalization, MOC, Monitoring & Assessment, Audit)
- Eliminate need for custom solutions to achieve basic compliance

#### 2. Sharing Best Practices
**ASM Consortium Revival:**
- Re-energize Abnormal Situation Management Consortium
- Share lessons learned from APO deployments
- Develop industry-standard deployment practices
- Create common troubleshooting knowledge base

**User Groups:**
- Establish active Honeywell Alarm Management user groups
- Regular meetings to share challenges, solutions, and best practices
- Collaborative development of deployment standards
- Vendor participation and responsiveness to user group feedback

#### 3. Insurance and Regulatory Incentives
**Expand Insurance Company Programs:**
- Premium discounts for sites with ISA 18.2/EEMUA 191 compliant alarm management systems
- Premium increases for sites without formal alarm management programs
- Regular audits required to maintain favorable rates

**Regulatory Requirements:**
- Mandate alarm management standards compliance in process safety regulations
- Include alarm system performance in incident investigations
- Require alarm management programs as part of operating permits

---

<div style="page-break-after: always;"></div>

## 7. Conclusions and Key Takeaways

### 7.1 Critical Insights

#### 1. Vendor-Delivered Solutions Insufficient for Quality Alarm Management
**Evidence:**
- APO missing critical ACM functionality (tags import/export, EMDB management, TagSync)
- No built-in health monitoring requiring custom development
- Standard instructions do not ensure deterministic backup/restore
- Reporting quality issues require custom Active/Suppressed Sync solutions
- "Without this solution not only Suppressed report but also KPIs are not accurate"

**Implication:** Achieving ISA 18.2/EEMUA 191 compliance requires sophisticated customers to develop custom solutions beyond standard vendor delivery.

#### 2. Pre-Migration Cleanup Criticality Cannot Be Overstated
**Marathon Finding:** "APO is currently mainly enhanced Rationalization tool with enforcements similar to ACM. APO is still missing critical Alarm Management tools that will make adjustments more challenging so cleanup before migration is critical."

**Requirements:**
- ACM DB cleanup (invalid tags, wrong assets, corrupted parameters, SCADA)
- M&R DB cleanup (ghost tags, old assets, paths optimization)
- License calculation and optimization
- EMDB integrity verification
- Health check before migration

**Risk:** Insufficient cleanup leads to poor APO performance, inaccurate licensing, unreliable reporting, and difficult post-migration troubleshooting.

#### 3. Daily Automated Health Checks Are Essential, Not Optional
**Value Beyond Alarm Management:**
- Discovers issues in TPS, Experion, and other systems
- Prevents months of frustration and weeks of troubleshooting
- Catches issues easily missed ("sync channels green but... in fact may not work")

**Marathon Assessment:** "COMMON SENSE addition every site should have"

**Vendor Gap:** Not included in standard Honeywell delivery, requiring custom development

#### 4. Industry Standards Awareness ≠ Industry Standards Compliance
**Honeywell Whitepaper:** 30+ years after AMTF formation, many companies still lack formal alarm management programs

**Marathon Reality:** Even sophisticated customers require 27 years of expertise to develop solutions ensuring quality and approaching standards compliance

**Industry Cost:** Continued incidents (Longford, Texas City, Deepwater Horizon) with alarm management as contributing factor

### 7.2 Deployment Success Factors

**Critical Success Factors for APO Deployment:**
1. **Pre-Migration Cleanup:** Thorough ACM and M&R DB cleanup before migration
2. **Health Monitoring:** Daily automated health checks deployed from Day 1
3. **Custom Solutions:** Marathon-developed Active/Suppressed Sync, ACM Maintenance, asset management tools
4. **Expertise:** Access to deep alarm management expertise (internal or consultants)
5. **Formal Standards:** Commitment to ISA 18.2/EEMUA 191 compliance, not just product installation
6. **Parallel Operations:** ACM and APO running in parallel during critical migration phase
7. **Testing:** Comprehensive testing of hierarchy, enforcements, reporting before cutover
8. **Training:** Effective usage training beyond standard vendor curriculum
9. **Continuous Improvement:** Regular monitoring, assessment, and remediation of Bad Actor alarms

### 7.3 Risk Assessment

**High-Risk Deployment Scenarios:**
- Insufficient pre-migration cleanup
- No daily automated health checks
- Reliance solely on standard Honeywell delivery
- Limited alarm management expertise
- No ISA 18.2/EEMUA 191 compliance program
- Inadequate testing before cutover
- ACM End of Support deadline driving rushed migration

**Low-Risk Deployment Scenarios:**
- Comprehensive ACM/M&R DB cleanup
- Marathon-style daily automated health checks deployed
- Custom solutions addressing known gaps (Active/Suppressed Sync, ACM Maintenance, etc.)
- Expert oversight throughout deployment
- Formal Alarm Philosophy and standards compliance program
- Parallel ACM/APO operations with thorough testing
- Post-deployment audit and continuous improvement process

### 7.4 Final Recommendations Priority Matrix

#### Immediate Priority (Execute Now)
1. Deploy daily automated health checks across all Marathon sites
2. Complete MPC APO Deployment Cookbook (eliminate TODO sections)
3. Establish pre-migration assessment procedures
4. Document Barbara Schubert's custom solutions for sharing/maintenance

#### High Priority (Next 6 Months)
5. Standardize APO deployment practices across Marathon
6. Develop APO Center of Excellence
7. Initiate formal ISA 18.2/EEMUA 191 compliance program
8. Address knowledge transfer and succession planning
9. Enhance vendor accountability through SLAs and product quality requirements

#### Medium Priority (Next 12 Months)
10. Establish Marathon alarm management training curriculum
11. Create cross-site support and expertise sharing mechanisms
12. Conduct post-deployment audits of completed APO migrations
13. Develop KPI tracking and reporting dashboards
14. Implement Management of Change procedures for alarm systems

#### Long-Term Priority (Ongoing)
15. Participate in or establish industry user groups
16. Contribute to ASM Consortium revival
17. Advocate for insurance/regulatory incentives for standards compliance
18. Continuously improve alarm management practices based on lessons learned

### 7.5 Knowledge Transfer Imperative

**Critical Risk:** Barbara Schubert's 27 years of expertise represents invaluable but vulnerable knowledge asset

**Recommended Actions:**
- Comprehensive documentation of all custom solutions, tools, and procedures
- Video recording of key procedures and troubleshooting techniques
- Formal training program for additional Marathon resources
- External consulting agreements to preserve access to expertise
- Regular knowledge sharing sessions across Marathon sites
- Mentoring program pairing experienced and developing alarm management engineers

**Timeline:** Knowledge transfer should begin immediately and accelerate before any personnel changes

---

<div style="page-break-after: always;"></div>

## 8. Vendor Feedback Summary for Honeywell

Based on this analysis, the following feedback should be provided to Honeywell regarding APO and alarm management product family:

### 8.1 Critical Product Gaps

**APO Missing Functionality (vs. ACM):**
1. Tags import/export capability (only Excel rationalization tool available)
2. EMDB import/export (only manual individual creation supported)
3. Ability to move tags to other consoles
4. TagSync functionality
5. Automated cleanup tools
6. Built-in health monitoring and alerting
7. Replication support

**Request:** Achieve full feature parity with ACM before ACM End of Support (December 31, 2027)

### 8.2 Quality and Reliability Issues

**Reporting Accuracy:**
- Active Sync incomplete (missing shelved, system alarms, DAS, CUTOUT, Enable/Disable/Inhibit/JournalOnly, Inactive)
- Suppressed Sync incomplete (missing suppress value columns, filtering capabilities)
- Impact: "Without this solution not only Suppressed report but also KPIs are not accurate"

**Backup/Restore:**
- Standard instructions do not ensure deterministic restore
- Request: Provide guaranteed deterministic backup/restore procedures

**Health Monitoring:**
- No built-in health checks for ACM replication, syncs, enforcements, database quality, hierarchy integrity
- Customers discover issues months after occurrence
- Request: Built-in comprehensive health monitoring with alerting

### 8.3 Documentation and Support Gaps

**Installation/Configuration:**
- Insufficient emphasis on critical pre-migration cleanup requirements
- Limited guidance on delta migration and parallel operations
- Incomplete testing procedures documentation

**Support:**
- Replication not supported by Honeywell (customers left without recourse)
- Backup/restore procedures insufficient
- Limited troubleshooting guidance for complex issues

### 8.4 Customer Impact

**License Management:**
- No automated tools to identify/remove ghost tags
- License bloat examples: 10,000+ tag spike from invalid History Index tags
- No license optimization guidance

**Migration Complexity:**
- APO described as "mainly enhanced Rationalization tool with enforcements similar to ACM"
- Missing tools make post-migration adjustments challenging
- Cleanup before migration critical but not sufficiently emphasized in vendor guidance

**Deployment Success:**
- Achieving quality alarm management requires sophisticated customer to develop extensive custom solutions
- 27 years of expertise needed to develop effective workarounds
- Standard vendor delivery insufficient for ISA 18.2/EEMUA 191 compliance

### 8.5 Requested Actions

**Product Development:**
1. Restore all critical ACM functionality in APO before End of Support
2. Develop built-in comprehensive health monitoring
3. Provide automated cleanup and maintenance tools
4. Implement full import/export capabilities
5. Add replication support with documentation

**Documentation:**
1. Complete, accurate installation/configuration guides
2. Backup/restore procedures ensuring deterministic restore
3. Comprehensive troubleshooting guides based on knowledge articles
4. Best practices documentation (not just feature descriptions)
5. Emphasis on pre-migration cleanup requirements

**Support:**
1. Replication support commitment
2. Enhanced SLAs for critical issues
3. Proactive notification of known issues
4. On-site support availability for complex deployments

**Quality:**
1. Testing against customer-scale deployments before GA release
2. Provide upgrade validation scripts to customers
3. Document known limitations and workarounds clearly
4. Address knowledge article findings in product (32 articles in 2025 indicates quality issues)

---

## 9. Document References

1. **GuardianNewsletterQ32025.pdf** - Honeywell Alarm Management quarterly newsletter (Q3 2025)
2. **honeywell-alarm-management-standards-whitepaper.pdf** - Comprehensive standards guide (ISA 18.2, EEMUA 191, IEC 62682)
3. **MPC APO Deployment Cookbook.docx** - Marathon Petroleum Corporation internal deployment standards (V0.2, December 14, 2025)
4. **Potential additions to the Standard HAM delivery (Barbara Schubert).docx** - Marathon-developed enhancements documentation (September 18, 2025)

---

**Analysis Prepared By:** AI Assistant  
**Analysis Date:** January 16, 2026  
**Based On:** Extracted content from four Marathon APO documentation sources  
**Purpose:** Comprehensive analysis for alarm management standards, deployment best practices, and vendor accountability
