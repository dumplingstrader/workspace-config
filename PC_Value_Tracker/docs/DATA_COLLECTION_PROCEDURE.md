# Process Controls Value Tracking — Data Collection Procedure

**Purpose:** Guide for supervisors and team members to extract and contribute issue tracking data using Microsoft Copilot.

**Author:** Tony Chiu, Senior Process Controls Engineer  
**Date:** January 2026  
**Version:** 1.0

---

## Overview

We are piloting a methodology to document and demonstrate the work performed by the Process Controls team. Your participation helps us:

1. **Show the volume** of technical support we provide
2. **Identify patterns** in recurring issues
3. **Quantify the effort** spent on different types of work
4. **Make data-driven cases** for resources and improvements

This document explains how to extract your issue data using Microsoft Copilot and submit it in a standardized format.

---

## Time Commitment

| Task | Frequency | Time |
|------|-----------|------|
| Weekly extraction | Every Friday | 10-15 minutes |
| Monthly summary | End of month | 15-20 minutes |

---

## What We're Tracking

For each technical issue or support request you handle:

| Field | Description | Example |
|-------|-------------|---------|
| Date | When the issue was reported | 2026-01-15 |
| Requester | Who asked for help | Operations, Projects, Maintenance |
| System | What platform was involved | Experion, PLC, SIS, HMI, Alarms |
| Area/Unit | Where in the refinery | FCC, Coker, Utilities |
| Issue Summary | Brief description | "Graphics loading slowly" |
| Resolution | How it was resolved | Fixed, Handed off, Escalated |
| Time Spent | Your estimate in hours | 2.5 |
| Was This PC's Job? | Yes, No, or Partial | Partial — helped diagnose, handed to Electrical |

---

## Step-by-Step Instructions

### Step 1: Open Microsoft Copilot

- In **Outlook**: Click the Copilot icon in the ribbon
- In **Teams**: Open Copilot chat
- In **Edge**: Go to copilot.microsoft.com (if enabled)

### Step 2: Run the Weekly Extraction Prompt

Copy and paste this prompt into Copilot:

```
Search my sent emails from the past 7 days. For each email that involves troubleshooting, problem resolution, or technical support, extract the following information in a table format:

| Date | Requester | System | Area/Unit | Issue Summary | Resolution | Time Estimate |

Where:
- Date: When the email was sent
- Requester: Who asked for help (person, group, or department)
- System: What platform (Experion, PLC, SIS, HMI, Alarms, Network, etc.)
- Area/Unit: Where in the refinery (FCC, Coker, Utilities, Plantwide, etc.)
- Issue Summary: Brief description of the problem (1-2 sentences)
- Resolution: Fixed, Handed off, Escalated, Pending, or In Progress
- Time Estimate: Quick (<1hr), Moderate (1-4hr), Significant (4-8hr), or Major (8+hr)

Focus on emails where I provided technical assistance, troubleshooting, or coordination. Skip routine administrative emails, meeting invites, and FYI-only messages.

Format the output as a table I can copy into Excel.
```

### Step 3: Review the Results

Copilot will generate a table. Review it for:
- **Accuracy** — Did it capture the right issues?
- **Completeness** — Are any significant issues missing?
- **Categorization** — Are systems and areas correct?

### Step 4: Add Your Judgment

For each row, mentally assess (or add columns for):
- **Was this actually PC's job?** (Yes / No / Partial)
- **Root cause category:**
  - PC Issue (configuration, logic, tuning)
  - Project Delivery (AMP, post-cutover problems)
  - Vendor Issue (product defect, TAC case)
  - Obsolete Equipment (legacy system failure)
  - Training Gap (user didn't know how)
  - Not PC (mechanical, electrical, other)

### Step 5: Export to Excel

1. Copy the table from Copilot
2. Open Excel
3. Paste into a new sheet
4. Add columns for your assessments
5. Save as: `PC_Value_[YourName]_[YYYYMMDD].xlsx`

Example: `PC_Value_JSmith_20260124.xlsx`

### Step 6: Submit Your Data

Save your Excel file to the shared location:
```
[To be determined — shared drive path or email to Tony]
```

Or email to: [Tony's email]

---

## Alternative Prompts

### For Monthly Summary (Run at End of Month)

```
Search my sent emails from the past 30 days. Categorize all technical support emails into:

1. Alarm Management
2. PLC/SIS Issues  
3. DCS/Experion
4. HMI/Graphics
5. Network/Infrastructure
6. Vendor Coordination
7. Project Support (AMP, capital projects)
8. Training/Documentation

For each category, provide:
- Count of issues
- Brief summary of main themes
- Any recurring problems

Format as a summary I can copy into a report.
```

### For Specific System Deep-Dive

```
Search my sent emails from the past 30 days that mention [SYSTEM NAME - e.g., "Triconex" or "DynAMo"]. 

For each, extract:
- Date
- Issue description
- Resolution status
- Time spent (if mentioned)

Format as a table.
```

---

## What Happens with Your Data

1. **Aggregation** — All submissions are combined into a master dataset
2. **Analysis** — Patterns are identified across the team
3. **Reporting** — Monthly/quarterly summaries generated
4. **Anonymization** — Individual names removed for leadership reports (we report team totals, not individual performance)

Your data helps demonstrate the VALUE of our team, not evaluate individual performance.

---

## Tips for Better Results

### Be Consistent
- Run the weekly prompt every Friday
- Use the same format each time
- Submit on schedule

### Add Context Copilot Misses
Copilot only sees emails. Add notes for:
- Phone calls you handled
- Walk-up requests
- Issues resolved in person
- Time spent that wasn't documented in email

### Flag Significant Items
If you handled something major (emergency, long troubleshooting, cross-functional coordination), make a note so it stands out in the data.

### Don't Overthink Time Estimates
Rough categories are fine:
- Quick: < 1 hour
- Moderate: 1-4 hours
- Significant: 4-8 hours
- Major: 8+ hours

---

## FAQ

**Q: What if Copilot misses some issues?**
A: Add them manually. The prompt catches most email-documented work, but you know your week best.

**Q: What if an issue spans multiple days?**
A: Log it once with the total time estimate and note "multi-day" in the summary.

**Q: Should I include issues I helped with but didn't lead?**
A: Yes — note "assisted" in the resolution. We want to capture all PC involvement.

**Q: What about recurring issues (same problem every week)?**
A: Log each occurrence. The pattern is valuable data.

**Q: Is this evaluating my performance?**
A: No. This is about demonstrating TEAM value, not individual metrics. Reports to leadership show team totals.

---

## Questions or Issues?

Contact: Tony Chiu
- Email: [your email]
- Teams: [your Teams handle]
- Desk: [your location]

---

## Submission Schedule

| Period | Due Date | Submit To |
|--------|----------|-----------|
| Week of Jan 20-24 | Jan 24 | [location/email] |
| Week of Jan 27-31 | Jan 31 | [location/email] |
| January Monthly | Feb 3 | [location/email] |

---

*Thank you for participating in this pilot. Your data helps demonstrate the value our team provides to the refinery.*
