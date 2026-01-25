# PC Value Tracker V2.1 — Unified Copilot Prompt

**Purpose:** One prompt to extract and categorize all technical support work.

**Version:** 2.1
**Updated:** January 2026

---

## Important: Batch Size Limits

**Copilot works best with smaller time ranges.** Large requests (30+ days) cause:
- Laggy/unresponsive behavior
- Missing or incomplete fields
- Truncated results

**Recommended batch sizes:**
| Range | Best For |
|-------|----------|
| 7 days | Weekly routine (fastest, most accurate) |
| 14 days | Catching up after vacation |
| 30 days | Monthly if you missed weeks |

**Never request more than 30 days at once.** If you need historical data, run multiple 30-day batches.

---

## The Unified Prompt

Copy this entire prompt into Microsoft Copilot (Outlook or Teams):

```
Search my sent emails from [DATE RANGE - e.g., "the past 7 days" or "December 1-31, 2025"].

For each email involving technical support, troubleshooting, or problem resolution, extract ALL of these fields (do not leave any blank):

| Date | System | Summary | Stream | Complexity | Resolution | Business Impact |

REQUIRED FIELD DEFINITIONS (all fields must be filled):

Date: When sent (YYYY-MM-DD format)

System: Platform or technology involved. Use the most specific name:
- DCS: Experion, C300, Control Builder, TDC, HPM, Hiway, Native Window, ControlEdge
- ARC: TDC Control Language, Experion SCM, control strategies, loop tuning
- PLC: ControlLogix, CompactLogix, PLC-5, SLC-500, MicroLogix, Studio 5000, RSLogix
- SIS: Triconex, Trident, Tricon CX, TS1131, Safety Manager, HIMA, BMS
- Turbine: GE Mark VIe, ToolboxST
- Compressor: Woodward Flex500, GAP software, Triconex-based compressor controls
- Alarm: DynAMo, ACM, APO, ASM, HAM, alarm rationalization
- Historian: PHD, PI, PI Vision, data trending, data quality/integrity
- HMI: HMIWeb, GUS, FactoryTalk View, PanelBuilder32, field HMIs, thin clients
- Network: OPC, Modbus, FTE, serial (RS-232/485), MOXA, Blackbox converters
- Integrity: Change management, configuration snapshots, I/O reservations
- APC: Aspen DMC3, Imubit, inferentials, optimization
- Analyzers: Analyzer troubleshooting, environmental data
- SAP: Equipment master, work orders, ERP integration
- Vibration: BN3500, Bently Nevada, System 1
- Other: Only if none of the above apply

Summary: Brief description of what was done (1-2 sentences). REQUIRED - do not leave blank.

Stream: Pick ONE primary category:
- Project: Capital project, AMP, MOC, contractor deliverable, commissioning, cutover
- Day-to-Day: Routine support, troubleshooting, operator/maintenance request, unit support
- Legacy Modernization: Involves obsolete equipment (PLC-5, SLC-500, TDC, end-of-life)
- Diagnostic: Investigated but handed off to another group (Electrical, Mechanical, etc.)
- After-Hours: Work outside 7am-5pm weekdays or on weekends
- Applications: Specialized app support (DynAMo, ACM, Integrity, PHD, PI, alarm rationalization, backups)

Complexity: Effort level (REQUIRED):
- Quick: Less than 1 hour
- Low: 1-2 hours
- Moderate: 2-4 hours
- Medium: Half day
- High: Full day or more
- Major: Multi-day effort

Resolution: Current status (REQUIRED - pick one):
- Fixed: Issue resolved
- Pending: Still in progress
- Handed Off: Transferred to another group
- Escalated: Sent to vendor or higher support
- Workaround: Temporary fix in place

Business Impact: Why this matters (REQUIRED - pick one):
- Safety: Involved safety systems, hazards, or potential incidents
- Production: Affected throughput, yield, or unit operation
- Compliance: Affected regulatory requirements or audit items
- Efficiency: Affected optimization or performance
- Low: Minimal operational impact

INSTRUCTIONS:
- ALL 7 COLUMNS ARE REQUIRED - do not leave any field blank
- Focus on emails where I provided technical assistance or coordination
- Skip routine administrative emails, meeting invites, FYI messages
- If an issue fits multiple streams, pick the PRIMARY driver
- If Resolution is unclear, use "Pending"
- If Business Impact is unclear, infer from keywords (urgent, critical, safety, down)
- Format as a table I can copy to Excel
```

---

## When to Run

**Weekly (Recommended):** Every Friday, 5-10 minutes
- Most accurate results
- Easiest to review and correct
- Prompt: "past 7 days"

**Bi-weekly:** If you miss a week
- Prompt: "past 14 days"

**Monthly:** Last resort if you miss multiple weeks
- Prompt: "December 1-31, 2025" (use explicit dates)
- Review more carefully for missing fields

---

## Follow-Up Prompt: Fix Missing Fields

If Copilot returns rows with blank fields, run this immediately:

```
Review the previous table. For any rows with blank or missing fields:
- Summary: Describe what action was taken based on the email content
- Resolution: If unclear, mark as "Pending"
- Business Impact: Infer from urgency words (safety, production, down, critical)

Return the complete table with all fields filled.
```

---

## Follow-Up Prompt: Get More Detail on Major Items

```
For entries marked as Major or High complexity, provide more detail:
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

### Project — Choose when:
- Issue traces to AMP, capital project, or MOC
- Problem is post-cutover or post-commissioning
- Contractor quality is involved
- FAT/SAT feedback was ignored
- Project handoff was incomplete

### Day-to-Day — Choose when:
- Routine support request
- Operator or Maintenance question
- Standard troubleshooting
- Configuration or tuning work
- Unit-specific support or TAR assistance
- Not tied to a specific project or application

### Legacy Modernization — Choose when:
- Involves PLC-5, SLC-500, MicroLogix
- TDC or other end-of-life systems
- Equipment is 20+ years old
- Migration or replacement planning
- Spare parts unavailable

### Diagnostic — Choose when:
- You investigated but it wasn't a PC issue
- Handed off to Electrical, Mechanical, I&E, etc.
- Root cause was outside PC scope
- You spent time proving what it WASN'T

### After-Hours — Choose when:
- Email sent outside 7am-5pm weekdays
- Weekend work
- Emergency call-out
- Urgent response required

### Applications — Choose when:
- DynAMo or ACM alarm management work
- PAS Integrity or CyberIntegrity work
- PHD or PI historian issues
- Alarm rationalization activities
- Configuration backups and change control
- Specialized application troubleshooting

---

## Tips for Better Results

### Batch Size Matters
- **7 days = best quality** (fastest, most complete)
- **30 days = max** (may need follow-up prompt)
- **Never request 1 year** at once - break into monthly batches

### Be Consistent
- Run every Friday at the same time
- Use the exact prompt (Copilot learns patterns)

### Add Context Copilot Misses
- Phone calls
- Walk-up conversations
- Time spent that wasn't in email

### Verify Required Fields
After Copilot returns results, scan for blank cells. Run the "Fix Missing Fields" follow-up if needed.

---

## Comparison: V1.0 vs V2.1

| Aspect | V1.0 | V2.1 |
|--------|------|------|
| Prompts | 7 different prompts | 1 unified prompt |
| Fields | 12+ scattered | 7 required |
| Business Impact | Follow-up prompt | In main prompt |
| Resolution | Often missing | Required field |
| Stream options | 5 | 6 (added Applications) |
| Batch guidance | None | Max 30 days |

---

## Quick Reference Card

```
REQUIRED COLUMNS (all 7 must be filled):
  Date | System | Summary | Stream | Complexity | Resolution | Business Impact

SYSTEMS:
  DCS:        Experion, C300, Control Builder, TDC, HPM, ControlEdge
  ARC:        TDC Control Language, Experion SCM, loop tuning
  PLC:        ControlLogix, CompactLogix, PLC-5, SLC-500, Studio 5000
  SIS:        Triconex, Trident, TS1131, Safety Manager, HIMA, BMS
  Turbine:    GE Mark VIe, ToolboxST
  Compressor: Woodward Flex500, GAP, Triconex-based
  Alarm:      DynAMo, ACM, APO, ASM, HAM
  Historian:  PHD, PI, PI Vision
  HMI:        HMIWeb, GUS, FactoryTalk View, PanelBuilder32
  Network:    OPC, Modbus, FTE, serial, MOXA, Blackbox
  Integrity:  Change management, config snapshots
  APC:        Aspen DMC3, Imubit
  Analyzers:  Analyzer troubleshooting
  SAP:        Equipment master, work orders
  Vibration:  BN3500, Bently Nevada

STREAMS (pick ONE):
  Project | Day-to-Day | Legacy Modernization |
  Diagnostic | After-Hours | Applications

COMPLEXITY:
  Quick (<1hr) | Low (1-2hr) | Moderate (2-4hr) |
  Medium (half day) | High (full day) | Major (multi-day)

RESOLUTION:
  Fixed | Pending | Handed Off | Escalated | Workaround

BUSINESS IMPACT:
  Safety | Production | Compliance | Efficiency | Low
```

---

## Supervisor After-Hours Prompt

See **[COPILOT_PROMPT_AFTER_HOURS.md](COPILOT_PROMPT_AFTER_HOURS.md)** for the dedicated supervisor prompt.

This separate file is designed to be shared directly with supervisors for tracking:
- After-hours calls and emergencies
- Weekend work
- Call-out response times
- Remote vs onsite resolution

---

## Troubleshooting Copilot Issues

| Problem | Solution |
|---------|----------|
| Copilot is slow/laggy | Reduce date range to 7-14 days |
| Fields are blank | Run "Fix Missing Fields" follow-up |
| Results are truncated | Break into smaller batches |
| Wrong format | Say "format as table for Excel" |
| Missing emails | Try "search sent items" explicitly |

---

*V2.1 — All fields required, batch size guidance, 6 streams, supervisor after-hours prompt.*
