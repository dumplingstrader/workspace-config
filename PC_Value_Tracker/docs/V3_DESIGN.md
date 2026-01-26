# PC Value Tracker V3.0 — Auto-Classification Design

**Purpose:** Automate Resolution, Business Impact, and Stream classification to eliminate manual cleanup and improve metrics accuracy.

**Version:** 3.0
**Updated:** January 2026
**Status:** Rules tested against December 2025 data

---

## Problem Statement

In V2.x, Copilot frequently returns incorrect or missing field values:
- **Resolution**: 30%+ blank/Unknown; most are actually informational/advisory work
- **Business Impact**: Over-tags Safety for alarm management work (should be Compliance)
- **Stream**: Under review

The current field options don't capture the reality of SME work, forcing manual cleanup.

---

## V3.0 Solution Overview

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Outlook Copilot │────▶│  Raw Excel File  │────▶│  aggregate.py   │
│  (improved prompt)│     │  (may have gaps) │     │  + auto-classify│
└─────────────────┘     └──────────────────┘     └────────┬────────┘
                                                          │
                         ┌────────────────────────────────┘
                         ▼
              ┌─────────────────────┐     ┌──────────────────┐
              │  classification_    │     │   master.json    │
              │  rules.json         │────▶│  (corrected,     │
              │  (editable patterns)│     │   flagged)       │
              └─────────────────────┘     └──────────────────┘
```

**Two-layer defense:**
1. **Improved Copilot Prompt** — Better guidance to get it right at source
2. **Python Auto-Classifier** — Pattern-based correction for anything Copilot misses

---

## Key Design Decisions

### Resolution Logic
- **Pending = ONLY when waiting on someone else** (not default for unclear items)
- **Informational = Advisory work** (explaining, clarifying, recommending)
- **Fixed = Completed action** (including completed investigations/diagnoses)
- **Default = Informational** (most SME work is advisory)

### Business Impact Logic
- **Alarm administration work = Compliance** (not Safety)
- **Actual safety systems (SIS, Triconex) = Safety**
- **Items without clear keywords = Low** (acceptable)

---

## Tested Results (December 2025)

### Resolution - BEFORE vs AFTER

| Resolution | V2.x (Original) | V3.0 (Auto-Classified) |
|------------|-----------------|------------------------|
| **Unknown** | 13 (36%) | **0 (0%)** |
| **Informational** | 0 | **14 (39%)** |
| **Fixed** | 3 (8%) | **13 (36%)** |
| Pending | 12 (33%) | 3 (8%) |
| Escalated | 4 (11%) | 3 (8%) |
| Workaround | 4 (11%) | 3 (8%) |

### Business Impact - BEFORE vs AFTER

| Impact | V2.x (Original) | V3.0 (Auto-Classified) |
|--------|-----------------|------------------------|
| **Safety** | 13 (36%) | **4 (11%)** |
| Compliance | 10 (28%) | 14 (39%) |
| Efficiency | 6 (17%) | 4 (11%) |
| Production | 4 (11%) | 2 (6%) |
| Low | 3 (8%) | 12 (33%) |

---

## Resolution Categories (V3.0)

| Resolution | Definition | Example Patterns |
|------------|------------|------------------|
| **Fixed** | Work completed, action taken | "Completed", "Executed", "Enabled", "Verified", "Investigated", "Diagnosed" |
| **Informational** | Advisory/knowledge transfer | "Explained", "Clarified", "Recommended", "Pointed to", "Noted" |
| **Pending** | Waiting on someone else | "Requested files", "P1 troubleshooting", "for follow-up" |
| **Escalated** | Handed to vendor/L3 | "SR submitted", "Escalated", "defects documented" |
| **Workaround** | Temporary fix in place | "workaround", "mitigation", "temporary fix" |

**Default:** Informational

---

## Classification Rules Summary

See `config/classification_rules.json` for full regex patterns.

### Resolution Rules (Priority Order)
1. **Pending** (priority 5): Explicit waiting indicators, P1 troubleshooting
2. **Escalated** (priority 10): SR submitted, vendor escalation, defects documented
3. **Workaround** (priority 15): Workaround, mitigation, temporary fix
4. **Fixed - Delivered** (priority 18): Provided/shared lists, files, procedures
5. **Fixed - Completed** (priority 20): Completed, executed, enabled, verified
6. **Fixed - Confirmed** (priority 21): Self-recovered, confirmed resolved
7. **Fixed - Investigation** (priority 22): Investigated, diagnosed, checked
8. **Informational** (priority 30): Explained, clarified, recommended, etc.

### Business Impact Rules (Priority Order)
1. **Compliance - Alarm Admin** (priority 5): Rationalization, suppression, Tag Sync
2. **Safety** (priority 10): SIS, Triconex, hazard, PSM, SIL
3. **Production** (priority 20): P1, down, trip, PLC install
4. **Compliance - General** (priority 30): MOC, audit, Integrity, migration
5. **Efficiency** (priority 40): Diagnostic, backup, optimization, APO strategy

### Stream Rules (Priority Order)
1. **Applications** (priority 10): APO, ACM, DynAMo, Tag Sync, INHIBIT/DISABLE, suppression, Integrity, alarm discrepancies
2. **Legacy Modernization** (priority 20): TDC, PLC-5, SLC-500, obsolete systems
3. **Diagnostic** (priority 30): Explicitly handed off to Electrical/Mechanical/I&E
4. **Default**: Day-to-Day

### Stream - BEFORE vs AFTER

| Stream | V2.x (Original) | V3.0 (Auto-Classified) |
|--------|-----------------|------------------------|
| **Applications** | 20 (56%) | **25 (69%)** |
| Day-to-Day | 13 (36%) | 10 (28%) |
| Diagnostic | 2 (6%) | 0 (0%) |
| Legacy Modernization | 1 (3%) | 1 (3%) |

**Known Edge Case:** #26 (Experion/TPS + INHIBIT/DISABLE) triggers Applications but should be Day-to-Day. System context matters more than keyword in this case (96% accuracy acceptable).

---

## Updated Copilot Prompt Guidance

Add to `COPILOT_PROMPT.md`:

```
Resolution: Current status (REQUIRED - pick one):
- Fixed: Work completed, action taken, investigation finished
- Informational: Answered a question or provided guidance (no issue to fix)
- Pending: Waiting on someone else to respond or act
- Escalated: Sent to vendor or higher support (SR submitted)
- Workaround: Temporary fix in place

RESOLUTION GUIDANCE:
- If you EXPLAINED, CLARIFIED, or PROVIDED GUIDANCE → Informational
- If you COMPLETED, INVESTIGATED, or DIAGNOSED → Fixed
- If you are WAITING ON SOMEONE → Pending
- If unclear, default to Informational (advisory work is valuable)
```

---

## Implementation Status

### Completed
- [x] Create `config/classification_rules.json`
- [x] Test regex patterns against December 2025 data
- [x] Validate priority ordering
- [x] Document Resolution rules
- [x] Document Business Impact rules
- [x] Review and document Stream rules
- [x] Update `aggregate_raw_data.py` with auto-classify function
- [x] Add `corrected` field tracking
- [x] Update `COPILOT_PROMPT.md` with V3.0 guidance

### Pending
- [ ] Test full pipeline with historical data
- [ ] Re-run aggregation on existing data to apply classifications
- [ ] Commit all V3.0 changes

---

## Files

| File | Purpose |
|------|---------|
| `config/classification_rules.json` | Editable regex rules for all fields |
| `docs/V3_DESIGN.md` | This design document |
| `docs/COPILOT_PROMPT.md` | Prompt for Outlook Copilot (to be updated) |
| `scripts/collect/aggregate_raw_data.py` | Aggregation script (to be updated) |

---

## Rollback Plan

If auto-classification causes problems:
1. Set `"enabled": false` in classification_rules.json
2. Script falls back to Copilot values only
3. Review misclassified patterns
4. Adjust rules and re-enable

---

*V3.0 — Rules tested, pending Stream review and implementation*
