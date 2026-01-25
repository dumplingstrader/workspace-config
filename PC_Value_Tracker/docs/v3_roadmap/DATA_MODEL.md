# V3.0 — Extended Data Model

**Status:** Planning / Future Development

---

## Overview

V3.0 extends the V2.0 data model with accountability tracking fields. The schema is backward-compatible — V2.0 records remain valid.

---

## Schema Comparison

| Field | V2.0 | V3.0 | Notes |
|-------|------|------|-------|
| `id` | - | Required | Unique record identifier |
| `date` | Required | Required | |
| `system` | Required | Required | |
| `summary` | Required | Required | |
| `stream` | Required | Required | Reduced to 3 streams in V3.0 |
| `complexity` | Required | Required | |
| `resolution` | Required | Required | |
| `requester_dept` | Optional | Optional | |
| `area_unit` | Optional | Optional | |
| `hours_spent` | Optional | Required* | *Required for accountability records |
| `business_impact` | Optional | Optional | Categorical |
| `business_impact_usd` | - | Required* | Dollar amount |
| `project_name` | Optional | Optional | |
| `preventable` | Optional | Optional | |
| `handed_off_to` | Optional | Optional | |
| `equipment_id` | Optional | Optional | |
| `record_type` | - | Required | "standard" or "accountability" |
| `accountability.*` | - | Conditional | See below |

---

## V3.0 Full Schema

### Core Fields (All Records)

```json
{
  "id": "2026-037",
  "date": "2026-01-15",
  "system": "Experion",
  "summary": "47 graphics screens with incorrect tag references",
  "stream": "Project",
  "complexity": "Major",
  "resolution": "Fixed",
  "record_type": "accountability",

  "hours_spent": 12,
  "area_unit": "Unit 5 - FCC",
  "requester_dept": "Operations"
}
```

### Impact Fields (Accountability Records)

```json
{
  "impact": {
    "pc_hours": 12,
    "pc_cost_usd": 3060,
    "production_impact_usd": 5000,
    "safety_impact": "near-miss",
    "safety_impact_usd": 500,
    "other_impact_usd": 0,
    "total_impact_usd": 8560,
    "calculation_notes": "Production delay estimated with Ops supervisor"
  }
}
```

### Accountability Fields (Accountability Records Only)

```json
{
  "accountability": {
    "root_cause": "Contractor used outdated P&ID revision",
    "preventable": true,
    "preventable_how": "PC review at FAT would have caught tag mismatches",

    "responsible_party": {
      "name": "James Smith",
      "title": "AMP Phase 3 Project Manager",
      "department": "Capital Projects"
    },

    "notification": {
      "method": "email",
      "date": "2026-01-16",
      "response_due": "2026-01-30"
    },

    "response": {
      "received": false,
      "date": null,
      "type": "no_response",
      "details": "No response received by deadline"
    },

    "escalation": {
      "escalated": true,
      "level": 2,
      "escalated_to": {
        "name": "Robert Johnson",
        "title": "Capital Projects Director"
      },
      "escalation_date": "2026-02-05",
      "escalation_response": "Will discuss with project team"
    },

    "final_status": "pending",
    "resolution_date": null,
    "resolution_notes": "Awaiting response from Capital Projects Director"
  }
}
```

---

## Complete V3.0 Record Example

```json
{
  "id": "2026-037",
  "date": "2026-01-15",
  "system": "Experion",
  "summary": "47 graphics screens delivered with incorrect tag references post-AMP Phase 3 cutover",
  "stream": "Project",
  "complexity": "Major",
  "resolution": "Fixed",
  "record_type": "accountability",

  "hours_spent": 12,
  "area_unit": "Unit 5 - FCC",
  "requester_dept": "Operations",
  "project_name": "AMP Phase 3",

  "impact": {
    "pc_hours": 12,
    "pc_cost_usd": 3060,
    "production_impact_usd": 5000,
    "safety_impact": "near-miss",
    "safety_impact_usd": 500,
    "other_impact_usd": 0,
    "total_impact_usd": 8560,
    "calculation_notes": "Startup delay estimated with Operations shift supervisor. Near-miss events documented in operator log."
  },

  "accountability": {
    "root_cause": "Contractor used P&ID revision from June 2025; current revision (October 2025) had 23 tag changes from MOC-2025-142",
    "preventable": true,
    "preventable_how": "PC review during FAT would have identified tag mismatches. PC requested participation but was declined due to schedule.",

    "responsible_party": {
      "name": "James Smith",
      "title": "AMP Phase 3 Project Manager",
      "department": "Capital Projects"
    },

    "notification": {
      "method": "email",
      "date": "2026-01-16",
      "response_due": "2026-01-30"
    },

    "response": {
      "received": false,
      "date": null,
      "type": "no_response",
      "details": "No response received by 2026-01-30 deadline. Follow-up sent 2026-02-01, no reply."
    },

    "escalation": {
      "escalated": true,
      "level": 2,
      "escalated_to": {
        "name": "Robert Johnson",
        "title": "Capital Projects Director"
      },
      "escalation_date": "2026-02-05",
      "escalation_response": "Will discuss with project team and respond by Feb 15"
    },

    "final_status": "pending",
    "resolution_date": null,
    "resolution_notes": "Awaiting response from Capital Projects Director. Phase 4 planning underway; PC acceptance gate remains unimplemented."
  },

  "metadata": {
    "created_date": "2026-01-16",
    "created_by": "T. Chiu",
    "last_updated": "2026-02-05",
    "version": "3.0"
  }
}
```

---

## Field Definitions

### Core Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier (YYYY-NNN format) |
| `date` | date | When the issue occurred (YYYY-MM-DD) |
| `system` | string | Platform/technology involved |
| `summary` | string | Brief description (1-2 sentences) |
| `stream` | enum | "Project", "Legacy", "After-Hours" |
| `complexity` | enum | "Quick", "Moderate", "Major" |
| `resolution` | enum | "Fixed", "Handed Off", "Escalated", "Workaround", "Pending" |
| `record_type` | enum | "standard" or "accountability" |

### Impact Fields

| Field | Type | Description |
|-------|------|-------------|
| `impact.pc_hours` | number | Hours spent by PC |
| `impact.pc_cost_usd` | number | PC hours × loaded rate |
| `impact.production_impact_usd` | number | Production/downtime cost |
| `impact.safety_impact` | string | "none", "near-miss", "first-aid", "recordable" |
| `impact.safety_impact_usd` | number | Safety event valuation |
| `impact.other_impact_usd` | number | Other costs |
| `impact.total_impact_usd` | number | Sum of all impact |
| `impact.calculation_notes` | string | How estimates were derived |

### Accountability Fields

| Field | Type | Description |
|-------|------|-------------|
| `accountability.root_cause` | string | What caused the issue |
| `accountability.preventable` | boolean | Could this have been prevented? |
| `accountability.preventable_how` | string | How it could have been prevented |
| `accountability.responsible_party` | object | Who is accountable |
| `accountability.notification` | object | How/when they were notified |
| `accountability.response` | object | Their response (or lack thereof) |
| `accountability.escalation` | object | Escalation details if applicable |
| `accountability.final_status` | enum | "pending", "resolved", "accepted_risk", "unresolved" |

### Response Types

| Value | Meaning |
|-------|---------|
| `acknowledged` | Issue accepted as documented |
| `disputed` | Findings contested |
| `action_planned` | Corrective action committed |
| `no_action` | Risk accepted, no action planned |
| `no_response` | No reply by deadline |

---

## V3.0 Streams (Simplified)

V3.0 consolidates to three accountability streams:

| Stream | V2.0 Equivalent | Focus |
|--------|-----------------|-------|
| `Project` | Project Handoff | Capital project delivery failures |
| `Legacy` | Technical Debt | Obsolete equipment issues |
| `After-Hours` | After-Hours Burden | Off-hours work |

**Merged streams:**
- Day-to-Day → Baseline metrics (not accountability tracked)
- Diagnostic → Captured in summary, not separate stream

---

## File Structure

```
data/
├── master.json              ← All standard records (V2.0 compatible)
├── accountability/          ← V3.0 accountability records
│   ├── 2026-001.json
│   ├── 2026-002.json
│   └── ...
├── accountability_register.json  ← Summary index of all accountability records
└── raw/                     ← Weekly Copilot exports
```

### accountability_register.json

```json
{
  "records": [
    {
      "id": "2026-037",
      "date": "2026-01-15",
      "stream": "Project",
      "summary": "AMP Phase 3 graphics issues",
      "total_impact_usd": 8560,
      "status": "pending",
      "escalation_level": 2
    }
  ],
  "summary": {
    "total_records": 15,
    "total_impact_usd": 245000,
    "by_status": {
      "pending": 3,
      "resolved": 8,
      "accepted_risk": 2,
      "unresolved": 2
    },
    "by_stream": {
      "Project": 8,
      "Legacy": 5,
      "After-Hours": 2
    }
  },
  "last_updated": "2026-02-05"
}
```

---

## Migration from V2.0

V2.0 records remain valid in V3.0. To upgrade a record to accountability status:

1. Add `"record_type": "accountability"`
2. Add `impact` object with dollar values
3. Add `accountability` object with tracking fields
4. Move to `data/accountability/` folder
5. Update `accountability_register.json`

**Not all V2.0 records need upgrading.** Only significant issues warrant full accountability treatment.

---

## Validation Rules

### Required for all records:
- `id`, `date`, `system`, `summary`, `stream`, `complexity`, `resolution`, `record_type`

### Required for accountability records:
- All core fields
- `impact.total_impact_usd`
- `accountability.responsible_party`
- `accountability.notification.date`
- `accountability.response.type`

### Business rules:
- `id` must be unique
- `date` must be valid ISO date
- `stream` must be one of: "Project", "Legacy", "After-Hours"
- If `escalation.escalated` is true, `escalation.level` must be 1-4

---

*V3.0 — Structured data for structured accountability.*
