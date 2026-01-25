# PC Value Tracker V2.0 — Stream Definitions

Detailed guide to the five tracking streams.

---

## Overview

Each stream is designed with:
- **Specific focus** — What it captures
- **Target audience** — Who needs to see it
- **Key metric** — What we measure
- **The ask** — What change we're demanding

---

## Stream 1: Project Handoff

### Purpose
Track issues caused by capital project delivery failures. Create accountability for project quality.

### What Belongs Here
- Post-cutover problems from AMP or other capital projects
- Issues with contractor deliverables (graphics, configuration, logic)
- Problems that should have been caught in FAT/SAT
- Missing documentation or incomplete commissioning
- MOC-related issues
- Anything that wouldn't exist if project handoff was done right

### Examples
- "Graphics loading slowly after AMP Phase 3 cutover"
- "Alarm configuration missing for new compressor"
- "Logic error in contractor-delivered sequence"
- "FAT issue we flagged but project closed anyway"

### Key Questions to Answer
- Which project/phase caused this?
- Was this preventable at handoff?
- How many PC hours to remediate?

### The Scorecard
```
PROJECT HANDOFF SCORECARD — AMP Phase 3

Issues Found Post-Cutover: 14
PC Hours to Remediate: 47
Preventable at FAT/SAT: 11 (79%)

Top Issue Types:
1. Graphics quality: 6
2. Alarm configuration: 4
3. Documentation gaps: 3

RECOMMENDATION: Phase 4 requires PC acceptance testing before close.
```

### Audience
- AMP Project Manager
- Phase Project Engineers
- Capital Projects leadership

### The Ask
**"Before any project phase closes, Process Controls must sign off that deliverables meet our standards. No sign-off = phase stays open."**

---

## Stream 2: Day-to-Day Support

### Purpose
Track routine support work to show workload and identify patterns.

### What Belongs Here
- Support requests from Operations
- Maintenance questions and assistance
- Routine troubleshooting
- Configuration changes
- Tuning and optimization
- General "how do I..." questions

### Examples
- "Operator asked how to acknowledge shelved alarms"
- "Helped Maintenance troubleshoot compressor trip"
- "Configured new setpoint for FCC reactor"
- "Reviewed control logic for unit startup"

### Key Metrics
- Volume per month (trend up/down?)
- System distribution (which platforms create most work?)
- Requester breakdown (who needs most support?)
- Complexity distribution (how much is Major?)

### The Dashboard
```
DAY-TO-DAY SUPPORT — January 2026

Total Issues: 42
Trend: ▲ 12% vs December

By System:
  Experion: 45%
  PLC: 28%
  HMI: 15%
  Other: 12%

By Requester:
  Operations: 55%
  Maintenance: 30%
  Engineering: 15%

By Complexity:
  Quick: 45%
  Moderate: 40%
  Major: 15%
```

### Audience
- PC Supervisors
- Department Manager
- Leadership (for headcount discussions)

### The Ask
**"Here's the baseline workload. Here's the trend. Here's what we need for sustainable coverage."**

---

## Stream 3: Technical Debt (Legacy)

### Purpose
Track issues with obsolete equipment to justify obsolescence funding.

### What Belongs Here
- PLC-5 failures or near-failures
- SLC-500, MicroLogix issues
- TDC system problems
- Any equipment that is:
  - End-of-life or unsupported
  - 20+ years old
  - Has no available spare parts
  - Vendor no longer supports

### Examples
- "PLC-5 in Unit 12 faulted — recovered but concerning"
- "TDC gateway dropping communications intermittently"
- "SLC-500 battery low — this is the third time"
- "Had to source spare from eBay for 30-year-old system"

### Key Metrics
- Failure frequency per equipment
- Mean time between failures
- Risk score (criticality × age × failure rate)
- Replacement cost estimate

### The Register
```
TECHNICAL DEBT REGISTER — Q1 2026

CRITICAL RISK (Recommend immediate action):
┌─────────────────┬──────┬────────────┬────────┬─────────────┐
│ Equipment       │ Age  │ Failures   │ Risk   │ Replace $   │
│                 │      │ (12 mo)    │ Score  │             │
├─────────────────┼──────┼────────────┼────────┼─────────────┤
│ Unit 12 PLC-5   │ 34yr │ 3          │ HIGH   │ $85,000     │
│ Unit 7 SLC-500  │ 28yr │ 2          │ MEDIUM │ $45,000     │
│ TDC Gateway #4  │ 31yr │ 1          │ MEDIUM │ $120,000    │
└─────────────────┴──────┴────────────┴────────┴─────────────┘

Total Deferred from AMP: $1.2M
Estimated Cost of Failure: $500K - $2M per incident
```

### Audience
- Capital Planning
- Reliability Engineering
- Leadership

### The Ask
**"These systems are time bombs. AMP deferred $1.2M in PLC upgrades. Fund the top 3 before we have a catastrophic failure."**

---

## Stream 4: Diagnostic Value ("Not Our Problem")

### Purpose
Capture the invisible work of diagnosing issues that turn out to not be PC scope.

### What Belongs Here
- Issues you investigated that turned out to be:
  - Electrical (wiring, power, motor)
  - Mechanical (valve, pump, actuator)
  - Instrumentation (transmitter, analyzer)
  - Operations (procedure, training)
  - IT (network, server, non-OT)
- Any time you spent proving what something WASN'T
- Work where you helped even though it wasn't your job

### Examples
- "Spent 2 hours troubleshooting 'PLC issue' — was a loose wire"
- "Investigated alarm flood — root cause was stuck valve"
- "Helped Ops with 'graphics problem' — actually a training gap"
- "Diagnosed compressor trip — handed off to Mechanical"

### Key Metrics
- Hours spent diagnosing non-PC issues
- Breakdown by handoff destination (Electrical, Mechanical, etc.)
- Percentage of "PC calls" that weren't actually PC

### The Value Statement
```
DIAGNOSTIC VALUE — Q4 2025

Issues Investigated: 24
Actual PC Issues: 15 (63%)
Handed Off to Others: 9 (37%)

PC Hours on Non-PC Issues: 18 hours

Handoff Destinations:
  Electrical: 4
  Mechanical: 3
  Instrumentation: 2

VALUE STATEMENT: We provide diagnostic services for issues
that aren't our responsibility. This saves other groups time
but is invisible in our workload metrics.
```

### Audience
- Leadership
- Operations management
- Maintenance management

### The Ask
**"We spend 18+ hours per quarter diagnosing issues that aren't ours. Either recognize this as a service we provide, or restore Maintenance's first-line troubleshooting capability."**

---

## Stream 5: After-Hours Burden

### Purpose
Make off-hours work visible to support staffing and compensation discussions.

### What Belongs Here
- Weekend calls or work
- Evening/night support (after 5pm, before 7am)
- Holiday work
- Emergency call-outs
- Any time you were interrupted outside normal hours

### Examples
- "Called at 11pm Saturday for compressor trip"
- "Worked Sunday to support unit startup"
- "Emergency remote session at 2am for alarm flood"
- "Holiday coverage for critical system issue"

### Key Metrics
- Call-out frequency (per week/month)
- Response time (how fast did we respond?)
- Off-hours hours worked
- Resolution rate (fixed remotely vs. had to go on-site)

### The Burden Report
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
  Required on-site: 33%

BURDEN STATEMENT: Team members responded to 12 after-hours
calls this quarter, working 34 hours outside normal schedule.
```

### Audience
- Leadership
- HR
- Supervisors

### The Ask
**"Here's the after-hours burden. Here's what sustainable on-call coverage looks like. Here's what fair compensation for this responsiveness would be."**

---

## Stream Decision Tree

```
Is this related to a capital project, AMP, or MOC?
├─ YES → PROJECT stream
└─ NO ↓

Is this obsolete equipment (PLC-5, SLC, TDC, 20+ years)?
├─ YES → LEGACY stream
└─ NO ↓

Did I hand this off to another group (Electrical, Mechanical, etc.)?
├─ YES → DIAGNOSTIC stream
└─ NO ↓

Was this outside normal working hours?
├─ YES → AFTER-HOURS stream
└─ NO → DAY-TO-DAY stream
```

---

## Multi-Stream Issues

Sometimes an issue could fit multiple streams. Pick the PRIMARY driver:

| Scenario | Choose |
|----------|--------|
| AMP issue with legacy PLC | PROJECT (AMP is the root cause) |
| Weekend call for routine support | AFTER-HOURS (timing is notable) |
| Project issue I handed off | PROJECT (project is the source) |
| Legacy equipment call at night | AFTER-HOURS (burden is the story) |

---

*V2.0 — Every stream has an ask. Every ask drives change.*
