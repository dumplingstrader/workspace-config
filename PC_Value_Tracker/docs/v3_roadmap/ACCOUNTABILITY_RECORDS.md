# V3.0 — Accountability Records

**Status:** Planning / Future Development

---

## Concept

An Accountability Record transforms a logged issue into formal documentation that:
- Identifies the responsible party
- Requests a specific response
- Sets a deadline
- Documents the actual response (or lack thereof)
- Triggers escalation if ignored

---

## Record Format

### Standard Accountability Record

```
═══════════════════════════════════════════════════════════════════
ACCOUNTABILITY RECORD #[YYYY-NNN]
═══════════════════════════════════════════════════════════════════

ISSUE DETAILS
─────────────────────────────────────────────────────────────────
Record ID:        [YYYY-NNN]
Date Occurred:    [YYYY-MM-DD]
Stream:           [Project Handoff / Technical Debt / After-Hours]
System:           [Platform/equipment involved]
Location:         [Unit/Area]

Summary:
[2-3 sentence description of the issue]

Root Cause:
[What caused this issue]

Preventable:      [Yes/No]
If Yes, How:      [What could have prevented this]

IMPACT ASSESSMENT
─────────────────────────────────────────────────────────────────
PC Hours Spent:           [X hours]
PC Cost (loaded):         $[X × hourly rate]
Production Impact:        $[estimated]
Safety Impact:            [None / Near-miss / Incident]
Total Estimated Impact:   $[sum]

Impact Calculation Notes:
[How estimates were derived]

ACCOUNTABILITY
─────────────────────────────────────────────────────────────────
Responsible Party:   [Name, Title]
Department:          [Projects / Operations / Maintenance / etc.]
Notified Via:        [Email / Meeting / Formal Memo]
Notification Date:   [YYYY-MM-DD]
Response Due:        [YYYY-MM-DD]

Response Requested:
□ Acknowledge issue as documented
□ Dispute findings (provide specifics)
□ Commit to corrective action (describe)
□ Accept risk with no action (provide rationale)

RESPONSE TRACKING
─────────────────────────────────────────────────────────────────
Response Received:   [Yes / No]
Response Date:       [YYYY-MM-DD or "None"]
Response Type:       [Acknowledged / Disputed / Action Planned / No Action / No Response]

Response Details:
[What they said, or "No response received by deadline"]

ESCALATION (if applicable)
─────────────────────────────────────────────────────────────────
Escalated:           [Yes / No]
Escalation Level:    [1 / 2 / 3 / 4]
Escalated To:        [Name, Title]
Escalation Date:     [YYYY-MM-DD]
Escalation Response: [Summary]

RESOLUTION
─────────────────────────────────────────────────────────────────
Final Status:        [Resolved / Accepted Risk / Unresolved]
Resolution Date:     [YYYY-MM-DD]
Resolution Notes:
[How this was ultimately addressed, or current state if unresolved]

═══════════════════════════════════════════════════════════════════
Record Created:    [YYYY-MM-DD] by [Name]
Last Updated:      [YYYY-MM-DD]
═══════════════════════════════════════════════════════════════════
```

---

## Example: Project Handoff Record

```
═══════════════════════════════════════════════════════════════════
ACCOUNTABILITY RECORD #2026-037
═══════════════════════════════════════════════════════════════════

ISSUE DETAILS
─────────────────────────────────────────────────────────────────
Record ID:        2026-037
Date Occurred:    2026-01-15
Stream:           Project Handoff
System:           Experion HMI Graphics
Location:         Unit 5 - FCC

Summary:
47 Experion graphics screens delivered by AMP Phase 3 contractor
contained incorrect tag references. Operators reported alarms not
displaying and trends showing wrong values. PC spent 12 hours
identifying and correcting tag mapping errors.

Root Cause:
Contractor used P&ID revision from June 2025. Current revision
(October 2025) had 23 tag renaming changes from MOC-2025-142.

Preventable:      Yes
If Yes, How:      PC review during FAT would have caught tag
                  mismatches. PC requested FAT participation but
                  was told timeline didn't allow.

IMPACT ASSESSMENT
─────────────────────────────────────────────────────────────────
PC Hours Spent:           12 hours
PC Cost (loaded):         $3,060 (12 × $255/hr)
Production Impact:        $5,500 (delayed startup, operator confusion)
Safety Impact:            Near-miss (2 unreported due to workaround)
Total Estimated Impact:   $8,560

Impact Calculation Notes:
Production impact estimated with Operations shift supervisor.
Near-miss events documented in operator log 2026-01-15.

ACCOUNTABILITY
─────────────────────────────────────────────────────────────────
Responsible Party:   James Smith, AMP Phase 3 Project Manager
Department:          Capital Projects
Notified Via:        Email (attached)
Notification Date:   2026-01-16
Response Due:        2026-01-30

Response Requested:
☑ Acknowledge issue as documented
□ Dispute findings (provide specifics)
☑ Commit to corrective action (describe)
□ Accept risk with no action (provide rationale)

RESPONSE TRACKING
─────────────────────────────────────────────────────────────────
Response Received:   No
Response Date:       None
Response Type:       No Response

Response Details:
No response received by 2026-01-30 deadline. Follow-up email sent
2026-02-01, no reply.

ESCALATION (if applicable)
─────────────────────────────────────────────────────────────────
Escalated:           Yes
Escalation Level:    2
Escalated To:        Robert Johnson, Capital Projects Director
Escalation Date:     2026-02-05
Escalation Response: "Will discuss with project team and respond
                     by Feb 15."

RESOLUTION
─────────────────────────────────────────────────────────────────
Final Status:        Pending
Resolution Date:     --
Resolution Notes:
Awaiting response from Capital Projects Director. Phase 4 planning
is underway; PC acceptance gate remains unimplemented.

═══════════════════════════════════════════════════════════════════
Record Created:    2026-01-16 by T. Chiu
Last Updated:      2026-02-05
═══════════════════════════════════════════════════════════════════
```

---

## Example: Technical Debt Record

```
═══════════════════════════════════════════════════════════════════
ACCOUNTABILITY RECORD #2026-012
═══════════════════════════════════════════════════════════════════

ISSUE DETAILS
─────────────────────────────────────────────────────────────────
Record ID:        2026-012
Date Occurred:    2026-01-08
Stream:           Technical Debt
System:           Allen-Bradley PLC-5/40
Location:         Unit 12 - Alkylation

Summary:
PLC-5 processor faulted due to memory corruption. System was down
for 45 minutes while PC performed recovery procedure. This is the
third fault in 12 months for this 34-year-old controller. No spare
processor available; recovery relied on backup program file.

Root Cause:
Age-related hardware degradation. PLC-5 platform is 34 years old,
discontinued by vendor in 2017, no firmware updates available.

Preventable:      Yes
If Yes, How:      PLC-5 replacement was in AMP scope but deferred
                  due to budget constraints (2023 decision).

IMPACT ASSESSMENT
─────────────────────────────────────────────────────────────────
PC Hours Spent:           3 hours
PC Cost (loaded):         $765 (3 × $255/hr)
Production Impact:        $45,000 (45 min downtime × $60K/hr)
Safety Impact:            None (safe shutdown achieved)
Total Estimated Impact:   $45,765

Impact Calculation Notes:
Downtime cost per Operations standard costing model.
This is the 3rd incident in 12 months; cumulative impact ~$140K.

ACCOUNTABILITY
─────────────────────────────────────────────────────────────────
Responsible Party:   Maria Garcia, Capital Planning Manager
Department:          Capital Planning
Notified Via:        Formal memo with Technical Debt Register
Notification Date:   2026-01-10
Response Due:        2026-01-31

Response Requested:
□ Acknowledge issue as documented
□ Dispute findings (provide specifics)
☑ Commit to corrective action (describe)
□ Accept risk with no action (provide rationale)

RESPONSE TRACKING
─────────────────────────────────────────────────────────────────
Response Received:   Yes
Response Date:       2026-01-22
Response Type:       Acknowledged, Risk Accepted

Response Details:
"Capital Planning acknowledges the risk. Unit 12 PLC-5 replacement
is on the 5-year capital plan (2028). Current year budget is fully
allocated. We accept the interim risk."

ESCALATION (if applicable)
─────────────────────────────────────────────────────────────────
Escalated:           No
Escalation Level:    --
Escalated To:        --
Escalation Date:     --
Escalation Response: --

RESOLUTION
─────────────────────────────────────────────────────────────────
Final Status:        Accepted Risk
Resolution Date:     2026-01-22
Resolution Notes:
Capital Planning formally accepted risk. Response documented.
PLC-5 remains on Technical Debt Register as Critical Risk.
If catastrophic failure occurs, this record documents that
the risk was known and accepted.

═══════════════════════════════════════════════════════════════════
Record Created:    2026-01-10 by T. Chiu
Last Updated:      2026-01-22
═══════════════════════════════════════════════════════════════════
```

---

## When to Create Accountability Records

Not every V2.0 issue needs a full accountability record. Create them for:

| Criteria | Threshold |
|----------|-----------|
| Business impact | > $5,000 estimated |
| Complexity | Major (4+ hours) |
| Safety | Any near-miss or incident |
| Repeat issue | Third occurrence of same problem |
| Preventability | Clearly preventable at handoff |
| Political value | High visibility or strategic importance |

**Estimated volume:** 2-5 accountability records per month (not every issue)

---

## Notification Templates

### Initial Notification Email

```
Subject: PC Accountability Record #2026-037 — AMP Phase 3 Graphics Issues

James,

Process Controls has documented the following issue for formal tracking:

Issue: 47 Experion graphics screens with incorrect tag references
Impact: $8,560 estimated (PC remediation + production delay)
Root Cause: Contractor used outdated P&ID revision
Preventable: Yes — PC review at FAT would have identified

Full documentation is attached.

We request your response by January 30, 2026:
□ Acknowledge issue as documented
□ Dispute findings
□ Commit to corrective action for Phase 4
□ Accept risk with no action

If no response is received, this record will be escalated per
PC department accountability policy.

Regards,
[Name]
Process Controls
```

### Escalation Notification Email

```
Subject: ESCALATION — PC Accountability Record #2026-037 (No Response)

Robert,

This issue is being escalated to you because no response was received
from the initial notification.

Original notification: January 16, 2026 to James Smith
Response deadline: January 30, 2026
Response received: None

Issue Summary:
AMP Phase 3 delivered 47 graphics screens with incorrect tags.
Estimated impact: $8,560. Root cause: outdated P&ID revision.

We request your response by February 15, 2026.

Full accountability record attached.

Regards,
[Name]
Process Controls
```

---

## Record Storage

Accountability records should be stored:

1. **Individual files:** `data/accountability/2026-037.md`
2. **Summary register:** `data/accountability_register.json`
3. **Backup:** Retain email notifications as evidence

---

*V3.0 — Every significant issue becomes a formal record.*
