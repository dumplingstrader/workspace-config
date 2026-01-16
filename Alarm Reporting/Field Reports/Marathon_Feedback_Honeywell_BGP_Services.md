# Honeywell BGP Plus Services - Marathon Feedback

**To:** Honeywell Process Solutions - BGP Plus Services Team
**From:** Marathon Petroleum - Alarm Management
**Date:** January 15, 2026
**Re:** Field Service Report Review - Anacortes, Salt Lake City, & Detroit Sites

---

## Executive Summary

Marathon Petroleum appreciates Honeywell's continued support through the Benefits Guardianship Plus (BGP Plus) program. As a premium service contract holder, we expect comprehensive and accurate field service delivery that matches the level of investment we've made in this partnership.

This document provides constructive feedback on recent BGP Plus site visits to our **Anacortes, WA (December 9-11, 2025)**, **Detroit, MI (December 9-13, 2024)**, and **Salt Lake City** facilities. While we recognize Honeywell's technical expertise, several discrepancies between reported activities and actual outcomes require immediate attention and corrective action.

**Key Operational Impacts:**

- Increased internal troubleshooting time and resource allocation
- Delayed realization of benefits from BGP Plus program
- Risk to compliance and alarm management integrity
- Incomplete work requiring rollback to pre-visit backups in some cases

---

<div style="page-break-after: always;"></div>

## Site Visit: Anacortes, WA (December 9-11, 2025)

### Reported Outcomes vs. Operational Status

#### ❌ **Primary Objective Failure: Software Not Upgraded Despite Multiple BGP Plus Visits Over 4 Years**

**Vendor Report States:**

> "Initially planned to upgrade ACM and database to 321.12.7... system was left at the current release of 321.12.4." (Section 2.6)

**Operational Status:**

- **Planned upgrade was not completed** despite being a stated objective
- **System running on 4-year-old software release** despite multiple previous BGP Plus site visits
- **Pattern of upgrade neglect** - critical updates deferred across multiple service visits
- Site closure due to flooding was on **Day 3 only**
- **Two full days (Day 1-2) were available** for the upgrade before the emergency
- No evidence that upgrade was attempted during available time
- System remains on older version, missing critical patches and features

**Expected Action:**

- Upgrade should have been prioritized and completed on Day 1 or Day 2
- Emergency on Day 3 should not have prevented completion of primary deliverable
- Alternative scheduling should have been proposed immediately

**Marathon's Concern:**
We paid for a 3-day site visit with a clear objective. Only receiving a health check (routine maintenance) when we contracted for an upgrade represents incomplete service delivery. The emergency closure affected **33% of the visit**, but the upgrade was achievable in the remaining **67%** of scheduled time. More critically, **this system has been 4 years behind on software updates despite multiple BGP Plus visits**—raising serious questions about service value and proactive maintenance across the entire contract period.

---

#### ❌ **Multiple Non-Functional Features After "Healthy" System Declaration**

**Vendor Report States:**

> System is "healthy" and "running normally"

**Operational Status:**

Despite the report stating the system is "healthy" and "running normally," **post-visit validation revealed multiple critical features are non-functional**:

- **Collection not working for one channel** - alarm data not being captured
- **Synchronization (Standard Suppressed Sync) not working for all of the channels**
- **ACM Enforcements not working** - alarm enforcement rules not functioning
- **Alarm Help updates not working for one system** - could not propose or update alarm help documentation
- **Critical non-functional features not recorded or escalated** during the site visit
- "System healthy" conclusion contradicts actual system state
- This discrepancy suggests incomplete testing or validation during the site visit

**Expected Action:**

- All features must be validated as functional before declaring system "healthy"
- Collection and synchronization must be tested for all channels
- Discrepancies must be documented and escalated immediately
- Follow-up visit required to restore functionality

**Marathon's Concern:**
The "system healthy" conclusion is contradicted by non-functional features discovered post-visit. This represents either inadequate testing procedures or incomplete validation protocols. Critical alarm management functions are compromised, yet this was not detected or reported during the site visit.

---

#### ⚠️ **Incomplete Troubleshooting: Unrecognized Messages Documented But Not Resolved**

**Vendor Report States:**

> "Checked data flow to archiver. Some unrecognized messages in UTL channel" (Appendix A, Day 1, Item 11)

**Operational Status:**

- Issue was **identified but not investigated**
- No root cause analysis performed
- No resolution attempted or scheduled
- Issue remains in production system

**Expected Action:**

- Immediate investigation of unrecognized messages
- Determination of whether messages indicate data loss or system malfunction
- Remediation plan with timeline
- Documentation of workaround if immediate fix unavailable

**Marathon's Concern:**
Identifying issues without resolution does not fulfill the "troubleshoot and resolve" objective (Section 2.1, Objective #2). Premium service should include root cause analysis and remediation, not just issue identification.

---

#### 📊 **Licensing Capacity Warning Without Action Plan**

**Vendor Report States:**

> "Licensed tag count is getting close to maximum (88.55% of total). Recommend increasing licensed tag count." (Section 2.8)

**Operational Status:**

- Critical capacity warning provided **without proactive planning**
- No timeline for when 100% capacity will be reached
- No guidance on how to increase license count
- No quote or procurement process initiated
- **Recommendation misaligned with actual system health**: Suggesting license expansion while critical features are non-functional prioritizes growth over stability

**Expected Action:**

- Projection of when tag limit will be exceeded based on historical growth
- Detailed quote for license expansion
- Timeline for procurement and implementation
- Temporary mitigation strategies if expansion cannot occur immediately
- **Prioritize system stability over capacity expansion**: Fix non-functional features before recommending license increases

**Marathon's Concern:**
At 88.55% capacity, we are approaching a critical service disruption. Simply recommending an increase without actionable next steps delays our planning and budgeting cycles. More importantly, recommending license expansion when the system has non-functional features suggests the health check prioritized upselling over ensuring operational integrity. We expect recommendations to align with actual system needs and health status.

---

#### 📋 **Baseline Expectations**

These items represent the **minimum standard procedures** that should be performed during every BGP Plus visit to ensure system health and operational continuity:

- Comprehensive health check documentation
- All services verified operational
- Database backup validation confirmed
- Client tools connectivity verified
- Clear documentation of system configuration

---

<div style="page-break-after: always;"></div>

## Site Visit: Detroit, MI (December 9-13, 2024)

### Reported Outcomes vs. Operational Status

#### ❌ **Critical Activity Left Incomplete: L4 ACM Web Patch Not Applied**

**Vendor Report States:**

> "L4 Reporting Server ACM Web Patch Update of R321.12.7 - This activity could not be performed as Matthew did not have enough rights to update the patches in the Server." (Day 7, Section 3)

**Operational Status:**

- **Vendor failed to coordinate access requirements in advance**
- Critical patch not applied due to lack of preparation
- Issue discovered **on Day 3** of a 5-day visit
- No contingency plan executed
- System left in **inconsistent state** (ACM upgraded to R321.12.7, but ACM Web still on R120.3)

**Expected Action:**

- Access requirements should have been validated **before arrival**
- If access unavailable, escalation to Marathon management should have occurred **immediately**
- Alternative: Remote completion post-visit with proper credentials
- At minimum: Detailed procedure left for Marathon staff to complete patch

**Marathon's Concern:**
This represents a **critical failure in service planning and execution**. Honeywell has serviced our Detroit facility multiple times and should have documented access requirements. Leaving the system with inconsistent patch levels creates potential compatibility issues and support complications.

---

#### ❌ **Critical System Failure Not Noticed or Recorded: M&R Collection and Sync Stopped**

**Operational Status:**

- **Maintenance & Repair (M&R) collection and synchronization stopped 3 days before the end of the visit**
- **This critical failure was not noticed or recorded** by Honeywell field personnel during the 5-day visit
- System was left in **worse state than before the visit**
- When functionality was finally restored, **there was a data gap covering the 3 days of the BGP Plus visit**
- Critical alarm and maintenance data lost during the service period

**Expected Action:**

- Continuous monitoring of system health during site visits
- Immediate escalation when critical functions stop operating
- Data integrity validation before declaring work complete
- Recovery procedures to minimize data gaps when issues are discovered

**Marathon's Concern:**
This represents the most serious technical oversight: a critical system function failed during the visit and went completely unnoticed by the field engineer. The fact that M&R collection and sync stopped 3 days before visit completion—and was not detected—demonstrates inadequate monitoring and validation procedures. The resulting data gap creates compliance risks and operational blind spots that undermine the entire purpose of the BGP Plus service.

---

#### ⚠️ **Incomplete Client Patching: 12 of 28 Clients Not Updated**

**Vendor Report States:**

> "12 Nos of ACM Clients still need to be patched as Marathon OT is awaiting for Admin rights on those Clients to apply the patches." (Day 8, Section 3)

**Reality:**

- **43% of client systems remain unpatched**
- Partial deployment creates version inconsistency across environment
- Support burden now shifted to Marathon staff
- No plan provided for completing remaining clients
- **Persistent replication and synchronization issues despite reported upgrade completion**
- Upgrade marked as "complete" when nearly half of clients remain on old version

**Expected Action:**

- Complete list of 12 unpatched clients with detailed instructions
- Remote support session scheduled to complete patching
- Verification procedure to confirm all clients operational post-patch
- Timeline commitment for 100% completion
- **Resolution of replication and sync issues** that persisted after upgrade

**Marathon's Concern:**
An incomplete rollout increases our operational risk and support complexity. If access was the blocker, the vendor should have escalated immediately to ensure Marathon IT prioritized access provisioning. This represents poor change management planning. More critically, marking an upgrade as "complete" when 43% of clients remain unpatched and replication issues persist demonstrates a disconnect between reported success and operational status.

---

#### 📋 **Baseline Expectations**

These items represent the **minimum standard procedures** that should be performed during every BGP Plus visit to ensure system health and operational continuity:

- ACM successfully upgraded to R321.12.7 on all servers and clients
- SQL replication temporary removal and restoration executed properly
- Comprehensive system health check performed
- Clear documentation of future work recommendations

---

<div style="page-break-after: always;"></div>

## Site Visit: Salt Lake City

**Site Visit Dates:** November 17-21, 2025

### Reported Outcomes vs. Operational Status

#### ❌ **Critical Data Loss: Known Export Bug Not Communicated, Led to Loss of Alarm Notes**

**Operational Status:**

- **Special characters in Note fields** (e.g., "1.", "2.") cause export to split data into separate rows
- **Engineer observed the anomalous rows during export**, commented "I don't know why those are there"
- **No corrective action taken** despite recognizing the issue
- **Entire database re-imported** instead of only changed columns/rows
- **Critical Note data lost** (basis, consequence, response documentation)
- This is a **known issue also affecting Detroit site**, yet BGP Plus personnel were not briefed

**Expected Action:**

- Known technical issues should be communicated to field engineers before site visits
- Only import changed columns/rows, not entire database (risk mitigation)
- Validate data integrity after import operations
- Flag and escalate unexpected data during export/import operations

**Marathon's Concern:**
A known bug that causes data loss should have been communicated to field personnel before the visit. The engineer's comment "I don't know why those are there" reveals lack of knowledge transfer about existing issues. Importing an entire database instead of only modified fields represents poor change control. This failure destroyed critical alarm documentation that supports our safety and operational response procedures.

---

#### ❌ **Catastrophic Data Loss: Bulk Approve Operation Lost 1200+ SCADA Tag Configurations**

**Operational Status:**

- Engineer requested Marathon approve/release SCADA tags to allow bulk Propose and Approve of his Alarm Manager Client changes
- **Unbeknownst to site and engineer**: Most SCADA tags were in "in progress" state from prior reconfigurations
- **Known issue (existing TAC ticket)**: Tags contained incorrect empty rows with no data
- **Approving/releasing made empty rows "highest visible"** in Alarm Help and Alarm Manager Client
- **Result: Lost alarm, priority, and note data for 1200+ SCADA tags** (tags originally built in older ACM version, now on R321.12.9)
- **Engineer left site unaware anything was wrong**
- **System health check showed no findings** despite massive data loss
- **Forced rollback to 11/16/25 backup** to recover correct Released versions
- **Site remains unable to make changes or release SCADA tags** (ongoing TAC ticket with Roy/Honeywell support)

**Expected Action:**

- Pre-visit assessment of system state, including pending reconfigurations and known TAC tickets
- Awareness of existing issues that could be triggered by bulk operations
- Post-change validation before declaring work complete
- System health check should detect missing alarm data for 1200 tags

**Marathon's Concern:**
This is the most severe data loss incident: a bulk operation triggered a known bug (with active TAC ticket), destroying configurations for over 1200 SCADA tags. The engineer left without detecting the issue, and the system health check failed to identify massive data loss. This demonstrates inadequate coordination between field services and TAC support, absence of post-change validation, and ineffective health check procedures. We are now **blocked from making any SCAMA tag changes indefinitely** due to this incident.

---

#### ❌ **Critical Failure: Cleanup and Merge Tasks Required System Rollback**

**Operational Status:**

- **Cleanup and merge tasks were incomplete and caused system instability**
- **Rollback to pre-visit backup was required** to restore system functionality (specifically 11/16/25 backup)
- Work performed during site visit had to be **completely undone**
- System left in worse state than before visit

**Expected Action:**

- Comprehensive testing in non-production environment before production changes
- Rollback plan documented and validated before any production modifications
- Post-implementation validation to confirm system stability
- Immediate escalation when rollback was required

**Marathon's Concern:**
This represents the most serious service failure pattern: work performed during a BGP Plus visit caused system instability requiring full rollback. This not only wasted Marathon resources but also created operational risk and downtime. A premium service should never leave a system in worse condition than found. This incident demonstrates inadequate testing procedures and change management planning.

---

<div style="page-break-after: always;"></div>

## Recurring Patterns Across All Three Sites

### 1. **Incomplete Primary Deliverables**

All three sites experienced incomplete execution of stated objectives:

- **Salt Lake City:** Cleanup/merge failed, requiring full system rollback (negative outcome)
- **Anacortes:** Upgrade not completed (0% completion)
- **Detroit:** L4 patch not applied, 43% of clients not patched

### 2. **Discrepancy Between Reported Status and Operational Status**

- **Salt Lake City:** Work reported as completed had to be rolled back
- **Anacortes:** System declared "healthy" despite collection and sync failures on multiple channels
- **Detroit:** Upgrade marked "complete" with 43% of clients unpatched; M&R collection/sync failure unnoticed for 3 days

### 3. **Reactive Rather Than Proactive Service**

- Issues identified without resolution plans
- Capacity warnings without procurement guidance
- Access issues discovered during visit, not before
- System health conclusions contradicted by post-visit validation

### 4. **Insufficient Pre-Visit Planning**

- Required access not validated before arrival
- Upgrade readiness not confirmed before site visit
- Dependencies not identified in advance
- Inadequate testing protocols before production changes

### 5. **Lack of Understanding of Customer Environment**

- **Salt Lake City:** Insufficient understanding of system data led to failed merge
- **Anacortes:** Incomplete feature validation before declaring system healthy
- **Detroit:** Replication architecture issues not anticipated or resolved; M&R collection failure went unnoticed for 3+ days

### 6. **Inefficient Documentation Practices**

- **Health check reports recreated from scratch during every BGP Plus visit**
- Same information documented repeatedly (IP addresses, file locations, system configuration)
- No maintained baseline documentation that is updated incrementally
- Field engineers spend time on non-value-added documentation instead of proactive problem-solving
- Lack of historical trend analysis due to inconsistent documentation format

---

<div style="page-break-after: always;"></div>

## Marathon's Expectations for Premium BGP Plus Service

As a **premium service contract holder**, Marathon expects:

### ❗ **Multi-Year Documentation Continuity for Annual Service Contracts**

- **Comprehensive site visit history** maintained in standardized format per refinery
- **Year-over-year tracking** of recommendations and completion status
- **Historical record** of what was implemented, deferred, or abandoned and why
- **Personnel transition continuity** - documentation survives resource changes
- **Trending analysis** - identify recurring issues across annual visits
- Accessible repository enabling Marathon to audit service value and ROI across contract lifecycle

### ❗ **Clear Documentation of Deliverables and Improvements**

- **Explicit listing of what was delivered** during the visit
- **Documented improvements and enhancements** implemented
- **Reusable configurations and settings** clearly documented for enterprise-wide deployment
- **Lessons learned and best practices** that can be applied to other Marathon refineries
- **Catalog of implemented features and customizations** maintained by Honeywell for Marathon enterprise visibility
- **Showcase of successful implementations** that other Marathon sites can review and request
- Deliverables formatted for easy replication across multiple sites

### ❗ **Complete Deliverable Execution**

- All stated objectives completed within scheduled visit
- If completion impossible, immediate escalation and contingency planning
- No partial implementations left for customer to complete
- **No work that makes system worse than pre-visit state**

### ❗ **Proactive Problem Resolution**

- Issues not just identified but **resolved** or escalated
- Root cause analysis performed for all anomalies
- Action plans with timelines for any deferred work
- **Comprehensive testing before production changes**

### ❗ **Comprehensive Pre-Visit Planning**

- Access requirements validated 2 weeks before arrival
- Upgrade readiness checklist completed and shared with customer
- Change management plan reviewed and approved before execution
- **Backup and rollback procedures documented and validated**

### ❗ **Professional Follow-Up**

- Outstanding items tracked with Honeywell ticket numbers
- Regular status updates on deferred work
- Remote completion offered for items blocked by access issues
- **Post-implementation validation to confirm system health**

### ❗ **Technical Competency in Customer Environment**

- Engineers demonstrate deep understanding of customer's architecture
- Replication, synchronization, and integration issues anticipated and mitigated
- Feature validation performed before declaring system healthy
- **Training and knowledge transfer on complex architectures (e.g. ACM replication)**

---

<div style="page-break-after: always;"></div>

## Required Corrective Actions

We respectfully request Honeywell address the following items:

### **Immediate Actions (Within 4 Weeks)**

1. **Internal Root Cause Analysis (Recommended for Honeywell's Process Improvement)**

   - Marathon strongly recommends Honeywell conduct comprehensive internal RCAs to understand the systemic failures across these three sites:
     - **Salt Lake City:** Why cleanup/merge tasks failed and required rollback
     - **Anacortes:** Why planned upgrade was not attempted despite 2 available days; why system was declared "healthy" with non-functional features
     - **Detroit:** Why access coordination failed; why 43% of clients remained unpatched; why replication issues were not resolved during 5-day visit
   - These analyses are essential for Honeywell to identify technical skill gaps, planning deficiencies, and process breakdowns
   - Marathon does not require formal RCA reports, but these failures warrant Honeywell's internal investigation to prevent recurrence
2. **Technical Documentation and Support**

   - Provide complete technical documentation and procedures:
     - **Salt Lake City:** Cleanup/merge procedure with validated testing plan
     - **Anacortes:** ACM upgrade to R321.12.7 procedure, UTL channel troubleshooting guide, feature restoration steps
     - **Detroit:** L4 ACM Web patch installation guide, client patching procedure, replication resolution guide
   - Include lessons learned and known pitfalls from your field reports
   - Provide dedicated remote technical support contact for follow-up questions
3. **Service Process Improvement**

   - Share revised BGP Plus pre-visit planning checklist with mandatory items
   - Implement mandatory testing protocols before production changes
   - Implement access validation procedure 2 weeks before all site visits
   - Provide service level commitments for objective completion rates
   - Document escalation procedures when objectives cannot be completed

### **Short-Term Actions (Within 90 Days)**

4. **Field Personnel Technical Competency Assessment**

   - Provide detailed assessment of technical skill gaps identified across these three site visits
   - Explain how field engineers are selected and qualified for BGP Plus assignments
   - Document minimum technical competency requirements for:
     - ACM/Experion system upgrades
     - Complex system architectures (replication, synchronization)
     - Pre-visit planning and access coordination
     - Production change management and rollback procedures
   - Outline specific training deficiencies that led to these failures
5. **Technical Competency Improvement Plan**

   - Describe how Honeywell will ensure field personnel have adequate skills before site assignments
   - Provide certification/qualification process for complex system work
   - Explain quality assurance process for validating work completion
   - Detail mentoring or peer review process for less experienced engineers
   - Commit to skill-appropriate staffing for future Marathon visits
6. **Validation Protocol Implementation**

   - Develop and share validation protocol for post-implementation system health checks
   - Include comprehensive feature testing checklist before declaring systems "healthy"
   - Implement mandatory post-visit validation calls with customer to confirm system stability
   - Define objective completion criteria and success metrics for BGP Plus visits

### **Long-Term Actions (Ongoing)**

7. **BGP Plus Program Enhancement**
   - Implement objective completion metrics and reporting for all sites
   - Provide quarterly performance reviews of BGP Plus service delivery
   - Customer satisfaction surveys after each visit with transparent results
   - **Training and knowledge transfer** on complex architectures (ACM replication, synchronization issues)
   - **Value assurance reviews** to ensure Marathon realizes expected benefits from BGP Plus investment
   - Continuous improvement process based on customer feedback and incident analysis

---

<div style="page-break-after: always;"></div>

## Conclusion

Marathon Petroleum values our partnership with Honeywell and appreciates the technical expertise your team provides. However, as a premium BGP Plus customer, we require consistent and complete service delivery that matches our investment level.

The issues outlined in this document represent significant service delivery failures across three sites that suggest **fundamental technical competency gaps in field personnel**. Marathon has been forced to allocate additional internal resources and costs to complete the work that was not delivered during these visits. This represents an unexpected burden that should not be necessary with a premium support contract.

**Our primary concern is not financial compensation, but rather ensuring Honeywell has a concrete plan to address the technical skill limitations that led to these failures.** We need confidence that future BGP Plus visits will be staffed with appropriately qualified personnel who can complete planned objectives and handle complex system architectures.

We look forward to Honeywell's detailed response on technical competency improvements and process enhancements that will prevent similar failures. Future BGP Plus engagements must demonstrate the proactive, comprehensive support and technical excellence we expect and pay for.

**We appreciate your timely response to these concerns**, including:

- Acknowledgment of incomplete deliverables at all three sites
- **Detailed technical competency assessment and improvement plan**
- **Explanation of how field personnel are qualified for complex system work**
- **Commitment to skill-appropriate staffing for future Marathon engagements**
- Technical documentation and support for completion of incomplete work, included in the respository of site visits documentation
- Timeline for process improvement implementation
- Commitment to enhanced pre-visit planning processes

*(Note: Marathon recommends, but does not require, that Honeywell conduct internal RCAs for these failures to inform your process improvements)*

Thank you for your attention to these matters. We remain committed to a successful long-term partnership.

---

**Prepared by:**
Marathon Petroleum Alarm Management
Tony Chiu

**Distribution:**

- Honeywell BGP Plus Program Manager
- Honeywell Account Executive - Marathon Petroleum
- Marathon Sites Leadership
- Marathon Sites Alarm Engineers (Anacortes, Detroit, Salt Lake City)

---

*Document Classification: Business Confidential*
*Revision: 1.0*
*Date: January 15, 2026*
