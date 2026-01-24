# Quick Start: Weekly Value Tracking with Copilot

**Purpose:** Extract your weekly technical assistance work from Outlook emails in 5 minutes.

**Who This Is For:** Process Controls engineers tracking workload for performance reviews, promotions, or capacity planning.

---

## 🚀 Quick Start (3 Steps)

### Step 1: Open Copilot
- Open **Microsoft Copilot** in Outlook or Teams
- Make sure you're logged into your work account

### Step 2: Copy & Paste This Prompt

```
Search my sent emails from the past 7 days. For each email that involves troubleshooting, problem resolution, or technical support, extract the following information in a table format:

| Date | Subject | Requester | System/Equipment | Issue Summary | Resolution | Time Indicator | Request Source |

For each field:
- Date: When the email was sent
- Subject: Email subject line
- Requester: Who asked for help or reported the issue (person or group)
- System/Equipment: What system was involved (e.g., Experion, PLC-5, Triconex, DynAMo, graphics, alarms)
- Issue Summary: Brief description of the problem (1-2 sentences)
- Resolution: How it was resolved OR current status (fixed, handed off, pending, escalated)
- Time Indicator: Any mention of time spent or urgency (e.g., "spent 2 hours", "emergency", "quick fix")
- Request Source: Where the request came from (PLC_SIS email group, direct request, Operations, Projects, AMP, etc.)

Focus on emails where I provided technical assistance, troubleshooting, problem solving, or coordination. Skip routine administrative emails, meeting invites, and FYI-only messages.

Format as a table I can copy to Excel.
```

### Step 3: Export to Excel
- Copy the table Copilot generates
- Paste into Excel (Ctrl+V)
- Save with filename like `Weekly_Issues_2026-01-24.xlsx`

**Done!** You now have structured data for this week's work.

---

## 💡 Pro Tips

### Run This Every Friday
- Set a recurring calendar reminder: "Export weekly issues to Excel"
- Takes 5 minutes
- Builds history over time without relying on memory

### If Time Indicators Are Missing
Many entries might not show time spent. Use this **follow-up prompt** after the initial results:

```
For entries in the previous table where Time Indicator is incomplete or unclear, please infer the time/effort based on:

1. Email thread length (number of back-and-forth messages)
2. Time span between first message and resolution
3. Keywords indicating effort ("investigating", "urgent", "troubleshooting", "spent", "working on")
4. Complexity of the issue described

Estimate as: Quick fix (<1hr), Moderate (1-4hr), Significant (4-8hr), Major effort (8+hr), or Ongoing/Multi-day

Update the table with these estimates.
```

### Customize for Your Environment
**System/Equipment names** - Adjust to match your plant:
- Your systems: DCS, PLC, SIS, HMI, alarms, network, etc.
- Example: "Experion, PLC-5, Triconex" → "TDC, ControlLogix, Safety Manager"

**Request Sources** - Adjust to match your organization:
- Email groups you monitor
- Departments that request help (Operations, Maintenance, Projects, Engineering)
- Example: "PLC_SIS email group" → "Controls_Team distribution list"

---

## 🔧 Troubleshooting

### "Copilot found too many results"
Break into smaller periods:
```
Search my sent emails from January 20-24, 2026...
```

### "Missing emails I know I sent"
Be more specific about keywords:
```
Search my sent emails from the past 7 days that mention "troubleshooting" OR "problem" OR "issue" OR "not working"...
```

### "Table won't paste into Excel properly"
Ask Copilot to reformat:
```
Please reformat the previous table as comma-separated values (CSV) that I can paste into Excel.
```

### "Results include too many non-technical emails"
Add exclusions to the prompt:
```
...Skip routine administrative emails, meeting invites, FYI-only messages, status updates, and acknowledgments where I didn't provide technical help.
```

---

## 📊 What You'll Get

**Example output:**

| Date | Subject | Requester | System/Equipment | Issue Summary | Resolution | Time Indicator | Request Source |
|------|---------|-----------|------------------|---------------|------------|----------------|----------------|
| 1/22/26 | Console 3 alarm issues | Operations | Experion HMI | Alarms not clearing properly after reset | Cleared stuck alarms in ACM database | 30 minutes | Direct request |
| 1/23/26 | PLC-5 communication fault | Maintenance | PLC-5 | Lost comms to Tank Farm PLC | Cable damaged by forklift - handed to Electrical | 2 hours diagnosing | PLC_SIS group |
| 1/24/26 | Graphics slow to load | Lead Operator | Experion | Station 2 graphics taking 10+ seconds to load | Cleared cache, restarted display services | Quick fix | Direct request |

**After 4 weeks**, you'll have ~20-50 entries documenting your technical contributions.

---

## 📈 Next Steps

### Weekly Tracking (This File)
- ✅ You're doing this now - keep going!

### Monthly Summary
- Once you have 4+ weeks of data, run a monthly analysis
- See patterns, recurring issues, time spent by category
- Find in full prompts: `COPILOT_PROMPTS.md`

### Historical Extraction
- Extract past work for annual reviews or promotion packets
- Adjust date range: "from January 1, 2025 to December 31, 2025"
- Note: Email retention policies may limit how far back you can go

### Advanced Prompts
- AMP-related issue extraction
- "Not our problem" tracking (diagnostic work handed to others)
- Recurring issues identification
- Full set available in: `COPILOT_PROMPTS.md`

---

## ❓ Questions?

**"How far back can I extract?"**
- Depends on your company's email retention policy
- Typically 1-2 years
- Test with: "Search my sent emails from January 2024..."

**"Can I use this for performance reviews?"**
- Yes! Export to Excel and add columns for:
  - Business impact (Production, Safety, Cost savings)
  - Skills demonstrated (Troubleshooting, Leadership, Vendor coordination)
  - Time saved for others

**"What if I work on multiple sites/plants?"**
- Add a "Site/Location" column to the prompt
- Run separately for each site if needed
- Combine in Excel afterwards

**"Can teammates use the same prompt?"**
- Yes! Share this file with your team
- Everyone should customize System/Equipment names and Request Sources
- Results format will be consistent for team rollups

---

## 📁 File Naming Convention

Recommended naming for weekly exports:

```
Weekly_Issues_YYYY-MM-DD.xlsx
```

Example:
- `Weekly_Issues_2026-01-24.xlsx`
- `Weekly_Issues_2026-01-31.xlsx`
- `Weekly_Issues_2026-02-07.xlsx`

This makes it easy to:
- Sort chronologically
- Combine multiple weeks later
- Track coverage (any weeks missing?)

---

## 🎯 Success Metrics

After 1 month of weekly tracking, you should have:
- ✅ 20-50+ documented issues
- ✅ Time estimates for major work
- ✅ Clear picture of where your time goes
- ✅ Data for workload discussions with management
- ✅ Evidence for performance reviews/promotions

---

**Ready to start?** Open Copilot and paste the prompt above. Takes 5 minutes, saves hours of memory work later!

---

## Version

- **Version:** 1.0 Quick Start
- **Created:** January 2026
- **Based on:** COPILOT_PROMPTS.md (full version)
