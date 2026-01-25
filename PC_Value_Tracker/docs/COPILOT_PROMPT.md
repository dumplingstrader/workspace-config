# PC Value Tracker V2.0 — Unified Copilot Prompt

**Purpose:** One prompt to extract and categorize all technical support work.

**Version:** 2.0
**Updated:** January 2026

---

## The Unified Prompt

Copy this entire prompt into Microsoft Copilot (Outlook or Teams):

```
Search my sent emails from the past 7 days. For each email involving technical support, troubleshooting, or problem resolution, extract:

| Date | System | Summary | Stream | Complexity | Resolution |

FIELD DEFINITIONS:

Date: When sent (YYYY-MM-DD)

System: What platform or technology was involved?

Use the most specific name you can identify. Categories:

- DCS: Experion, C300, Control Builder, TDC, HPM, Hiway, Native Window, ControlEdge
- ARC (Advanced Regulatory Control): TDC Control Language, Experion SCM, control strategies, loop tuning
- PLC: ControlLogix, CompactLogix, PLC-5, SLC-500, MicroLogix, Studio 5000, RSLogix 5, RSLogix 500, Modicon
- SIS: Triconex, Trident, Tricon CX, TS1131, Safety Manager, HIMA, BMS, Heaters
- Turbine: GE Mark VIe, ToolboxST
- Compressor: Woodward Flex500, GAP software, Triconex-based compressor controls
- Alarm: DynAMo, ACM, APO, ASM, alarm rationalization
- Historian: PHD, PI, PI Vision, data trending, data quality/integrity
- HMI: HMIWeb, GUS, FactoryTalk View, PanelBuilder32, field HMIs, thin clients, VMs
- Network: OPC, Modbus, FTE, serial (RS-232/485), MOXA, Blackbox protocol converters
- Integrity: Change management, configuration snapshots, I/O reservations
- APC: Aspen DMC3, Imubit, inferentials, optimization
- Analyzers: Analyzer troubleshooting, environmental data
- SAP: Equipment master, work orders, ERP integration
- Vibration: BN3500, Bently Nevada, System 1 (Maintenance-owned, PC assists)
- Other: Only if none of the above categories apply

Summary: Brief description of the issue (1-2 sentences)

Stream: Categorize as ONE of these:
- Project: Related to capital project, AMP, MOC, contractor deliverable, commissioning, cutover
- Day-to-Day: Routine support, troubleshooting, operator/maintenance request
- Legacy: Involves obsolete equipment (PLC-5, SLC-500, TDC, end-of-life systems)
- Diagnostic: I investigated but handed off to another group (Electrical, Mechanical, etc.)
- After-Hours: Work outside 7am-5pm weekdays or on weekends

Complexity: Effort level
- Quick: Less than 1 hour
- Moderate: 1-4 hours
- Major: More than 4 hours

Resolution: Outcome
- Fixed: Issue resolved
- Handed Off: Transferred to another group
- Escalated: Sent to vendor or higher support
- Workaround: Temporary fix in place
- Pending: Still in progress

INSTRUCTIONS:
- Focus on emails where I provided technical assistance or coordination
- Skip routine administrative emails, meeting invites, FYI messages
- If an issue fits multiple streams, pick the PRIMARY driver
- Format as a table I can copy to Excel
```

---

## When to Run

**Weekly (Recommended):** Every Friday, 5-10 minutes

**Monthly:** If you miss weeks, run for past 30 days

---

## Follow-Up Prompts (If Needed)

### Fill Missing Fields

```
For entries with blank or unclear fields, please infer:
- System: Look for platform keywords (Experion, PLC, alarm, etc.)
- Stream: Check for project names, after-hours timestamps, legacy equipment mentions
- Complexity: Estimate from email thread length and urgency words
```

### Add Business Impact

```
For the previous table, add a column for Business Impact:
- Production: Affected throughput, yield, or unit operation
- Safety: Involved safety systems or hazards
- Compliance: Affected regulatory requirements
- Efficiency: Affected optimization or performance
- Low: Minimal operational impact

Look for keywords like "production", "down", "trip", "safety", "urgent", "critical".
```

### Get More Detail on Major Items

```
For entries marked as Major complexity, provide more detail:
- What was the root cause?
- How many hours were actually spent?
- Was this preventable at project handoff?
- Who else was involved?
```

---

## Exporting Results

1. Copy the table from Copilot
2. Paste into Excel
3. Save as: `data/raw/Weekly_[YYYY-MM-DD]_[Name].xlsx`

Example: `Weekly_2026-01-24_TChiu.xlsx`

---

## Stream Classification Guide

### Project Stream — Choose when:
- Issue traces to AMP, capital project, or MOC
- Problem is post-cutover or post-commissioning
- Contractor quality is involved
- FAT/SAT feedback was ignored
- Project handoff was incomplete

### Day-to-Day Stream — Choose when:
- Routine support request
- Operator or Maintenance question
- Standard troubleshooting
- Configuration or tuning work
- Not tied to a specific project

### Legacy Stream — Choose when:
- Involves PLC-5, SLC-500, MicroLogix
- TDC or other end-of-life systems
- Equipment is 20+ years old
- Spare parts unavailable
- "We're just hoping it holds together"

### Diagnostic Stream — Choose when:
- You investigated but it wasn't a PC issue
- Handed off to Electrical, Mechanical, I&E, etc.
- Root cause was outside PC scope
- You spent time proving what it WASN'T

### After-Hours Stream — Choose when:
- Email sent outside 7am-5pm weekdays
- Weekend work
- Emergency call-out
- Urgent response required

---

## Tips for Better Results

### Be Consistent
- Run every Friday at the same time
- Use the exact prompt (Copilot learns patterns)

### Add Context Copilot Misses
- Phone calls
- Walk-up conversations
- Time spent that wasn't in email

### Flag High-Value Items
If something was major (emergency, long troubleshooting, cross-team coordination), make a note so it stands out.

---

## Comparison: V1.0 vs V2.0

| Aspect | V1.0 | V2.0 |
|--------|------|------|
| Prompts | 7 different prompts | 1 unified prompt |
| Fields | 12+ | 6 core |
| Stream concept | None (flags scattered) | Central organizing principle |
| Focus | Extract everything | Categorize for action |

---

## Quick Reference Card

```
SYSTEMS (use specific names when possible):
  DCS:        Experion, C300, Control Builder, TDC, HPM, Native Window, ControlEdge
  ARC:        TDC Control Language, Experion SCM, loop tuning
  PLC:        ControlLogix, CompactLogix, PLC-5, SLC-500, Studio 5000, RSLogix
  SIS:        Triconex, Trident, TS1131, Safety Manager, HIMA, BMS, Heaters
  Turbine:    GE Mark VIe, ToolboxST
  Compressor: Woodward Flex500, GAP, Triconex-based
  Alarm:      DynAMo, ACM, APO, ASM
  Historian:  PHD, PI, PI Vision
  HMI:        HMIWeb, GUS, FactoryTalk View, PanelBuilder32, field HMIs
  Network:    OPC, Modbus, FTE, serial, MOXA, Blackbox
  Integrity:  Change management, config snapshots, I/O reservations
  APC:        Aspen DMC3, Imubit
  Analyzers:  Analyzer troubleshooting, environmental data
  SAP:        Equipment master, work orders
  Vibration:  BN3500, Bently Nevada (PC assists)

STREAMS: Project, Day-to-Day, Legacy, Diagnostic, After-Hours

COMPLEXITY: Quick (<1hr), Moderate (1-4hr), Major (4+hr)

RESOLUTION: Fixed, Handed Off, Escalated, Workaround, Pending
```

---

*V2.0 — One prompt, five streams, actionable data.*
