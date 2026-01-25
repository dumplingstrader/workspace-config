# PC Value Tracker — Supervisor After-Hours Prompt

**Purpose:** Capture after-hours calls, weekend work, and emergency support.

**Audience:** Process Controls Supervisors

**Time Required:** 5 minutes weekly

---

## The After-Hours Prompt

Copy this into Copilot (Outlook or Teams):

```
Search my sent emails AND calendar from [DATE RANGE - e.g., "the past 7 days" or "last week"].

Find any Process Controls after-hours activity:
- Emails sent outside 7am-5pm weekdays
- Weekend emails (Saturday/Sunday)
- Calendar entries for emergency calls or call-outs
- Emails mentioning: emergency, urgent, call-out, after-hours, weekend, night

For each after-hours item found, extract:

| Date | Time | Engineer | Issue Summary | System | Duration | Resolution | Remote/Onsite |

FIELD DEFINITIONS:

Date: When it occurred (YYYY-MM-DD)

Time: Approximate time (e.g., "10:30 PM", "Sunday morning")

Engineer: Who responded to the call

Issue Summary: Brief description of the problem (1-2 sentences)

System: Platform involved (DCS, PLC, SIS, Alarm, HMI, Network, Other)

Duration: Approximate time spent (e.g., "30 min", "2 hours", "ongoing")

Resolution: Current status
- Fixed: Issue resolved
- Pending: Still being worked
- Escalated: Sent to vendor or next shift
- Workaround: Temporary fix in place

Remote/Onsite: How it was handled
- Remote: Fixed via phone/VPN
- Onsite: Required coming to site
- Hybrid: Started remote, went onsite

INSTRUCTIONS:
- Include emails TO or FROM Process Controls engineers
- Include forwarded call-out notifications
- Include any "FYI" emails about overnight issues
- Skip routine automated alerts unless someone responded
- Format as a table I can copy to Excel
```

---

## Follow-Up Prompt (Optional)

If you need more detail on a specific call-out:

```
For the [DATE] after-hours call about [ISSUE]:
- What was the root cause?
- How long was the engineer engaged?
- Could this have waited until morning?
- Was this preventable?
```

---

## Quick Manual Log Template

For phone calls or walk-ups not captured in email:

| Date | Time | Engineer | Issue Summary | System | Duration | Resolution | Remote/Onsite |
|------|------|----------|---------------|--------|----------|------------|---------------|
| 2026-01-20 | 11:30 PM | J. Smith | Compressor trip alarm flood | DCS | 45 min | Fixed | Remote |
| 2026-01-22 | Sunday 8 AM | T. Chiu | PLC fault Unit 12 | PLC | 2 hours | Escalated | Onsite |

---

## Saving Results

Save the Excel file to:
```
data/raw/AfterHours_[YYYY-MM-DD]_[Supervisor].xlsx
```

Example: `AfterHours_2026-01-24_JSmith.xlsx`

The aggregation script will automatically:
- Import into the master database
- Tag as "After-Hours" stream
- Include in monthly/quarterly reports

---

## What Leadership Will See

The quarterly report summarizes after-hours burden:

```
AFTER-HOURS BURDEN — Q4 2025

Total Call-Outs: 12
Total Off-Hours Worked: 34 hours

By Time:
  Evenings (5pm-10pm): 5
  Nights (10pm-7am): 4
  Weekends: 3

Response Time:
  < 30 min: 75%
  < 1 hour: 92%

Resolution:
  Fixed remotely: 67%
  Required onsite: 33%

BURDEN STATEMENT: Team members responded to 12 after-hours
calls this quarter, working 34 hours outside normal schedule.
```

---

## Quick Reference

| Field | Values |
|-------|--------|
| System | DCS, PLC, SIS, Alarm, HMI, Network, Other |
| Resolution | Fixed, Pending, Escalated, Workaround |
| Remote/Onsite | Remote, Onsite, Hybrid |

---

## The Ask

*"Here's the after-hours burden. Here's what sustainable on-call coverage looks like. Here's what fair compensation for this responsiveness would be."*

---

*V2.1 — Supervisor After-Hours Tracking*
