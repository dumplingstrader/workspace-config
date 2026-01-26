# Process Controls Value Tracking V3.0 — Supervisor Briefing

**Purpose:** Brief supervisors on the redesigned value tracking initiative.

**Date:** January 2026
**Version:** 3.0

---

## What Changed from V1.0

| V1.0 | V3.0 |
|------|------|
| "Prove we're busy" | "Demand specific changes" |
| 12+ fields per issue | 7 core fields |
| 7 different prompts | 1 unified prompt |
| Generic reports | Stream-specific scorecards |
| Manual cleanup | Auto-classification |
| Defensive posture | Offensive posture |

---

## The Six Streams

Instead of tracking everything in one pile, V2.1 organizes work into **six streams**, each targeting a specific audience with a specific ask.

| Stream | What We Track | Who Sees It | What We Ask For |
|--------|---------------|-------------|-----------------|
| **Project** | AMP/capital project handoff failures | Projects team | PC acceptance gate before phase close |
| **Day-to-Day** | Routine support and troubleshooting | Leadership | Resource planning data |
| **Legacy Modernization** | Obsolete equipment issues | Capital Planning | Fund the obsolescence backlog |
| **Diagnostic** | Time diagnosing non-PC issues | Ops, Maintenance | Restore first-line troubleshooting |
| **After-Hours** | Off-hours calls and emergencies | HR, Leadership | Fair on-call compensation |
| **Applications** | DynAMo, Integrity, Historian support | Ops, IT/OT | Recognize application expertise |

---

## Why This Matters to Supervisors

### 1. After-Hours Visibility

**The problem:** After-hours calls go through supervisors but aren't tracked. Leadership doesn't see the off-hours burden.

**V2.1 solution:** Supervisors log after-hours calls. This creates visibility for:
- Staffing discussions
- On-call compensation
- Coverage planning

**Time commitment:** 2-5 minutes per call-out

### 2. Project Accountability

**The problem:** Projects hands over broken systems and declares victory. Your team inherits the cleanup.

**V2.1 solution:** Track post-handoff issues by project/phase. Create a scorecard that shows:
- How many issues each phase created
- How many PC hours to remediate
- What percentage was preventable

**The ask:** PC sign-off required before project phases close.

### 3. Legacy Equipment Risk

**The problem:** AMP deferred PLC upgrades. We're running 35-year-old equipment. When it fails, it's a crisis.

**V2.1 solution:** Maintain a Technical Debt Register showing:
- Equipment age and failure history
- Risk scores
- Replacement cost estimates

**The ask:** Fund obsolescence backlog before catastrophic failure.

---

## How You Can Help

### Option A: After-Hours Tracking (Minimal Effort)

**Two ways to capture after-hours work:**

**1. Copilot Query (Weekly - 5 minutes)**
Use the After-Hours Copilot Prompt in `docs/COPILOT_PROMPT_AFTER_HOURS.md`:
- Run weekly to catch emails sent outside normal hours
- Captures: Date, Time, Engineer, Issue, System, Duration, Resolution
- Save results to `data/raw/AfterHours_[Date]_[Name].xlsx`

**2. Quick Manual Log (Per Call-Out - 2 minutes)**
For phone calls not captured in email:

| Date | Time | Engineer | Issue Summary | System | Duration | Resolution | Remote/Onsite |
|------|------|----------|---------------|--------|----------|------------|---------------|
| 2026-01-20 | 11:30 PM | J. Smith | Compressor trip | DCS | 45 min | Fixed | Remote |

Save to same file as Copilot results.

### Option B: Encourage Team Participation

Share the QUICK_START guide with your engineers. Ask them to:
- Run the weekly Copilot prompt (10 min/week)
- Tag issues with the correct stream

### Option C: Both (Ideal)

- You track after-hours calls
- Team tracks day-to-day work
- Combined data tells the full story

---

## What This Is NOT

- NOT individual performance evaluation
- NOT micromanagement
- NOT additional burden on overwhelmed team
- NOT another initiative that goes nowhere

## What This IS

- Data to demand specific changes
- Visibility into invisible work
- Evidence for resource discussions
- Accountability for project quality

---

## Outputs You'll See

### Monthly: One-Page Summary

Single page showing volume, trends, and key findings. Takes 5 minutes to review.

### Quarterly: Stream Scorecards

Specific reports for specific audiences:
- Project Handoff Scorecard → Goes to Projects
- Technical Debt Register → Goes to Capital Planning
- After-Hours Burden Report → Goes to HR/Leadership

---

## Timeline

| Phase | When | Activity |
|-------|------|----------|
| **Now** | January | Pilot with existing data |
| **Month 1** | February | First monthly summary |
| **Month 2-3** | March-April | Refine, expand if valuable |
| **Q1 End** | April | First quarterly scorecards |

---

## Questions?

Contact the project coordinator to discuss:
- How this fits with your team's workflow
- What level of participation makes sense
- How to handle specific situations

---

## Next Steps

If you're willing to support this:

1. **Indicate** which option (A, B, or C) works for you
2. **Start** logging after-hours calls (if Option A or C)
3. **Share** the QUICK_START guide with your team (if Option B or C)
4. **Provide feedback** as we refine the approach

---

*V3.0 — Less tracking, more changing. Auto-classification eliminates manual cleanup.*
