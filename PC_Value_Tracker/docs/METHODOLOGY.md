# Process Controls Value Tracking Methodology

**Purpose:** Document and demonstrate the work performed by the Process Controls team through systematic issue tracking and analysis.

**Author:** Tony Chiu, Senior Process Controls Engineer  
**Date:** January 2026  
**Status:** Pilot Phase

---

## Executive Summary

This methodology provides a framework for capturing, categorizing, and analyzing the technical support work performed by Process Controls. The goal is to:

1. **Create visibility** into the volume and complexity of work handled
2. **Identify patterns** in recurring issues and root causes
3. **Quantify effort** spent on different types of support
4. **Enable data-driven decisions** about resources, training, and process improvements

---

## The Challenge

Process Controls handles a high volume of technical requests across multiple systems:
- Distributed Control Systems (DCS)
- Programmable Logic Controllers (PLC)
- Safety Instrumented Systems (SIS)
- Human-Machine Interfaces (HMI)
- Alarm Management Systems
- Network and Infrastructure

Currently, this work is not systematically tracked. This creates challenges:

| Challenge | Impact |
|-----------|--------|
| No central record of issues handled | Difficult to demonstrate workload |
| Root causes not categorized | Patterns go unnoticed |
| Time spent not documented | Resource planning is reactive |
| Resolution outcomes not tracked | Can't measure improvement |

---

## Methodology Overview

### What We Track

For each issue or request that comes to Process Controls:

| Field | Description | Example |
|-------|-------------|---------|
| **Date** | When the issue was reported | 2026-01-15 |
| **Source** | How it came in | PLC_SIS email, direct request, Operations call |
| **Requester** | Who reported it | Unit Operator, Project Engineer, Maintenance |
| **System** | What platform is involved | Experion, ControlLogix, Triconex, DynAMo |
| **Area/Unit** | Where in the refinery | FCC, Coker, Utilities, Plantwide |
| **Issue Summary** | Brief description | "Graphics loading slowly on console 4" |
| **Root Cause Category** | Categorized cause | See categories below |
| **Time Spent** | Hours invested | 2.5 hours |
| **Resolution** | Outcome | Fixed, Handed off, Workaround, Escalated |
| **Business Impact** | What was at stake | Production, Safety, Compliance, Efficiency |

### Root Cause Categories

Issues are categorized by root cause to identify patterns:

| Category | Description | Examples |
|----------|-------------|----------|
| **Process Controls Issue** | Legitimately PC scope - configuration, logic, tuning | Control loop tuning, alarm configuration, graphics fix |
| **Project Delivery** | Issues stemming from capital project handoffs | Post-cutover problems, incomplete commissioning |
| **Vendor/Product** | Issues requiring vendor support or product defects | Software bugs, TAC cases, licensing issues |
| **Obsolete Equipment** | Issues caused by aging or unsupported equipment | Legacy PLC failures, end-of-life systems |
| **Training/Knowledge Gap** | Issues stemming from user unfamiliarity | Operator questions, procedure gaps |
| **Mechanical/Electrical** | Issues that are NOT PC scope | Wiring problems, instrument failures, power issues |
| **Network/Infrastructure** | OT network and server issues | Communication timeouts, server problems |
| **Other** | Doesn't fit above categories | Miscellaneous |

### Business Impact Categories

| Impact | Description |
|--------|-------------|
| **Production** | Affects throughput, yield, or unit operation |
| **Safety** | Involves safety systems, interlocks, or hazard mitigation |
| **Compliance** | Affects regulatory requirements or permits |
| **Efficiency** | Affects optimization, energy use, or performance |
| **None/Low** | Minimal operational impact |

---

## Data Collection Approach

### Phase 1: Pilot (Current)

- Single engineer tracks issues encountered
- Focus on high-visibility and high-effort items
- Validate categorization approach
- Refine data fields as needed

### Phase 2: Expanded Pilot

- Additional engineers participate
- Cover multiple groups (Area, Specialists, Initiatives)
- Standardize definitions and categories
- Develop lightweight tracking tools

### Phase 3: Team Adoption

- All Process Controls engineers participate
- Integrated with existing workflows
- Regular reporting cadence established
- Continuous improvement of categories and metrics

---

## Analysis and Reporting

### Monthly Metrics

| Metric | Description |
|--------|-------------|
| **Volume** | Total issues handled |
| **By Category** | Breakdown by root cause |
| **By System** | Which platforms generate most work |
| **Resolution Rate** | % resolved vs. escalated vs. handed off |
| **Time Investment** | Total hours by category |

### Quarterly Insights

- Recurring issue identification
- Trend analysis (increasing/decreasing workload)
- Training needs identification
- Equipment reliability concerns
- Project delivery quality feedback

### Sample Questions This Data Answers

1. *"How much of our time goes to issues that aren't actually Process Controls problems?"*
   → Root cause category breakdown shows % handed off to other groups

2. *"What systems generate the most support requests?"*
   → System breakdown shows where effort is concentrated

3. *"Are we seeing the same problems repeatedly?"*
   → Recurring issue analysis identifies systemic problems

4. *"What's the impact of project delivery quality on our workload?"*
   → Project Delivery category quantifies post-handoff burden

5. *"Where should we focus training efforts?"*
   → Training/Knowledge Gap category reveals common questions

---

## Benefits

### For Process Controls Team
- Documented evidence of work performed
- Visibility into actual workload distribution
- Data to support resource requests
- Identification of training needs

### For Leadership
- Quantified view of PC team contributions
- Data for resource allocation decisions
- Visibility into recurring issues and root causes
- Feedback loop on project delivery quality

### For Operations
- Faster issue resolution through better tracking
- Identification of systemic problems
- Improved communication on issue status

### For Projects
- Feedback on deliverable quality
- Data on post-handoff support burden
- Input for future project planning

---

## Tools and Implementation

### Data Capture
- Outlook email analysis (via Copilot)
- Manual logging for phone/in-person requests
- Integration with existing systems where possible

### Storage
- Excel workbook for pilot phase
- Potential SAP integration for long-term

### Reporting
- Monthly summary reports
- Quarterly trend analysis
- Ad-hoc analysis as needed

---

## Success Criteria

After 3-6 months of pilot tracking:

| Metric | Target |
|--------|--------|
| Data completeness | 80%+ of significant issues captured |
| Category accuracy | 90%+ correctly categorized |
| Time estimates | Within 25% of actual |
| Actionable insights | 3+ improvement recommendations |

---

## Next Steps

1. **Continue pilot data collection** (Month 1-3)
2. **Refine categories and definitions** based on actual data
3. **Generate first monthly report** for review
4. **Gather feedback** from supervisors on usefulness
5. **Propose expanded pilot** if initial results are valuable

---

## Contact

**Tony Chiu**  
Senior Process Controls Engineer  
Initiatives Group

---

*This methodology is a pilot initiative to improve visibility into Process Controls team activities. Feedback and suggestions for improvement are welcome.*
