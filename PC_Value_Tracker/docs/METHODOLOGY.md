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

### Monthly Report Generation

**Automated Script**: `generate_monthly_report.py`

**Purpose**: Generate standardized monthly summaries from the master database for documentation and leadership review.

**How to Generate**:
```bash
python scripts/generate_monthly_report.py --input data/master_combined.json --month 2026-01 --output output/monthly_report_2026-01.xlsx
```

**Output Structure** (4 sheets):
1. **Summary**: Quick stats (total issues, by system, by area, by complexity, by department)
2. **All Issues**: Complete filtered list for the month
3. **By System**: Breakdown showing which platforms generate most work
4. **High Complexity**: Major/Significant issues requiring detailed attention

**Key Metrics Tracked**:
- **Volume**: Total issues handled (target: 15-25 per month)
- **System Distribution**: DCS vs PLC vs SIS vs Network breakdown
- **Complexity**: Routine vs Major vs Significant (aim for <30% high complexity)
- **Cross-Site**: Multi-site coordination activities
- **Departmental Breakdown**: Which departments request most support

**Example Output** (based on 215 entries across 2024-2026):
- Average 25 issues per month
- DCS systems: 45% of workload
- PLC troubleshooting: 30% of workload
- High complexity issues: 23 (10.7% of total)
- Cross-site activities: 24 (11% of total)

**When to Use**:
- End of each month for documentation
- Quarterly reviews with supervisor
- Annual performance review preparation

---

### Quarterly Insights Report

**Automated Script**: `generate_quarterly_insights.py`

**Purpose**: Identify trends, recurring issues, training needs, and strategic improvement opportunities over 3-month periods.

**How to Generate**:
```bash
python scripts/generate_quarterly_insights.py --input data/master_combined.json --quarter 2026-Q1 --output output/quarterly_insights_2026-Q1.xlsx
```

**Output Structure** (5 sheets):
1. **Executive Summary**: Key findings for leadership presentation
2. **Monthly Trends**: Volume trends (increasing/decreasing)
3. **Recurring Issues**: Systems with repeated problems (suggests systemic issues)
4. **Training Needs**: Common questions indicating knowledge gaps
5. **Equipment Reliability**: High-burden systems flagged for monitoring

**Strategic Analysis Includes**:
- **Trend Detection**: Is workload increasing or decreasing?
- **Pattern Recognition**: Same system generating multiple issues?
- **Training Opportunities**: Where are teams asking "how-to" questions?
- **Reliability Concerns**: Which equipment needs proactive maintenance?
- **Resource Planning**: Data to support headcount or tooling requests

**Example Insights**:
- "DCS System 2 generated 18 issues in Q1 (up from 9 in Q4) - investigate reliability"
- "5 separate PLC training questions from Operations - schedule training session"
- "Cross-site support increased 40% - consider standardization project"

**When to Use**:
- End of quarter for strategic planning
- Budget justification for training/resources
- Leadership presentations on team value

---

### Manual Report Templates

For custom presentations or detailed analysis, use pre-formatted templates:

**Excel Template**: `templates/Monthly_Report_Template.xlsx`

**Includes**:
- Executive Summary with metrics placeholders
- Issue Detail table (copy/paste from generated reports)
- System Breakdown with chart area
- Action Items / Recommendations section
- Notes for observations and trends

**PowerPoint Template**: `templates/Leadership_Presentation_Template.pptx`

**Slide Structure** (7 slides):
1. Title slide (customize period and presenter)
2. Executive Summary (key achievements, trends, impact)
3. Key Metrics Dashboard (6 visual metric cards)
4. System Breakdown (chart placeholder)
5. Success Stories (3 impact examples)
6. Recommendations (action items for leadership)
7. Questions (contact info)

**Design**: Professional teal and coral palette with metric cards and visual hierarchy

**How to Use Templates**:
1. Run automated scripts to get raw metrics
2. Copy key numbers into template placeholders (marked with [brackets])
3. Add narrative context and success stories
4. Insert charts from Excel into PowerPoint
5. Customize for specific audience (leadership, peers, annual review)

---

### Sample Questions This Data Answers

1. *"How much of our time goes to issues that aren't actually Process Controls problems?"*
   → Root Cause category breakdown in monthly report shows % handed off

2. *"What systems generate the most support requests?"*
   → System Breakdown sheet shows workload concentration (DCS 45%, PLC 30%)

3. *"Are we seeing the same problems repeatedly?"*
   → Quarterly Insights Recurring Issues sheet identifies systemic patterns

4. *"What's the impact of project delivery quality on our workload?"*
   → Project Delivery category in master database quantifies post-handoff burden

5. *"Where should we focus training efforts?"*
   → Quarterly Insights Training Needs sheet reveals common knowledge gaps

6. *"How has workload changed over time?"*
   → Quarterly Insights Monthly Trends sheet shows volume trajectory

7. *"Which issues required the most complex problem-solving?"*
   → High Complexity sheet in monthly report (currently 23 major/significant issues)

---

### Report Frequency Recommendations

| Report Type | Frequency | Audience | Purpose |
|-------------|-----------|----------|---------|
| **Automated Monthly Report** | Monthly | Self, supervisor | Documentation, pattern tracking |
| **Quarterly Insights** | Quarterly | Leadership, manager | Strategic planning, resource requests |
| **Leadership Presentation** | Quarterly or annual | Senior leadership | Demonstrate team value, justify resources |
| **Ad-hoc Analysis** | As needed | Project teams, operations | Answer specific questions, support decisions |

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

**Primary Method**: GitHub Copilot + Outlook Email Analysis
- Use Copilot prompts (see COPILOT_PROMPTS_QUICKSTART.md) to extract structured data from sent emails
- Run weekly or monthly: "Extract all troubleshooting/technical assistance from my sent emails"
- Copilot automatically categorizes System, Complexity, Root Cause, and My Role

**Manual Logging**: For phone calls, in-person discussions, or non-email work
- Add entries directly to Excel exports or master database

**Frequency**: Weekly recommended (Friday end-of-week review) to maintain accuracy

---

### Data Storage

**Master Database**: `data/master_combined_issues.xlsx`
- **Persistent database** - source of truth for all work history
- Cumulative and never loses data when adding new exports
- Current size: 215 unique entries (2024-2026)

**JSON Format**: `data/master_combined.json`
- Converted from master Excel for script processing
- Used by reporting scripts

**Backup Strategy**: Git version control + network folder sharing

---

### Data Processing Scripts

Located in `scripts/` directory:

| Script | Purpose | Usage |
|--------|---------|-------|
| `combine_excel_files.py` | Merge new Copilot exports into persistent master database | `python scripts/combine_excel_files.py` |
| `excel_to_json.py` | Convert master Excel to JSON for reporting | `python scripts/excel_to_json.py` |
| `export_simple_tracker.py` | Generate 9-sheet analysis workbook | `python scripts/export_simple_tracker.py` |
| `generate_monthly_report.py` | Monthly summary report | `python scripts/generate_monthly_report.py --month 2026-01` |
| `generate_quarterly_insights.py` | Quarterly trends and insights | `python scripts/generate_quarterly_insights.py --quarter 2026-Q1` |

**Key Design Pattern**: Persistent database mode
- combine_excel_files.py loads existing master FIRST
- New exports are appended and deduplicated
- Guarantees no data loss when adding new entries

---

### Reporting Tools

**Automated Reports**:
- Monthly reports: 4 sheets with metrics, issue lists, system breakdown
- Quarterly insights: 5 sheets with trends, recurring issues, training needs

**Manual Templates**:
- Excel template: Pre-formatted monthly report with placeholders
- PowerPoint template: 7-slide leadership presentation deck

**Template Generators** (run once to create templates):
```bash
python scripts/create_monthly_report_template.py
python scripts/create_leadership_presentation_template.py
```

Templates saved to `templates/` directory for reuse

---

### Technology Stack

- **Python 3.13+**: Data processing and automation
- **pandas**: Data manipulation and Excel processing
- **openpyxl**: Excel file creation and formatting
- **python-pptx**: PowerPoint template generation
- **Virtual Environment**: Isolated dependencies at `.venv/`

**Environment Setup** (one-time):
```bash
python -m venv .venv
.venv\Scripts\activate
pip install pandas openpyxl python-pptx
```

---

### Workflow Summary

1. **Weekly Data Capture**:
   - Run Copilot prompt on sent emails → Export to Excel
   - Save as `data/Troubleshooting_Emails_WeekOf_[Date]_[Name].xlsx`

2. **Monthly Consolidation**:
   - Run `combine_excel_files.py` to merge all exports into master database
   - Run `excel_to_json.py` to convert for reporting
   - Generate monthly report with `generate_monthly_report.py`

3. **Quarterly Analysis**:
   - Generate insights report with `generate_quarterly_insights.py`
   - Use templates to create leadership presentation
   - Review trends and identify improvement opportunities

4. **Annual Review**:
   - Aggregate all quarterly reports
   - Create comprehensive PowerPoint from template
   - Highlight key achievements and strategic contributions

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
