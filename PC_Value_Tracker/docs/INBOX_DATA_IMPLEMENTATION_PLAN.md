# Inbox Data Implementation Plan

**Decision Date:** January 2026
**Status:** Approved
**Version:** 1.0

---

## Background

Two data science perspectives were evaluated regarding the PC Value Tracker data collection strategy:

| Position | Argument | Verdict |
|----------|----------|---------|
| **Include Inbox** | Sent-only misses request context, response times, backlog visibility, and creates survivorship bias | Valid for specific metrics |
| **Sent-Only** | Inbox adds 5-10x noise, degrades Copilot performance, sent emails represent actual outputs | Valid for primary workflow |

---

## Decision

**Primary workflow remains sent-only.** Supplementary inbox queries added for specific metrics.

### Rationale

1. **Sent emails = clean signal** — Every sent email represents actual work output
2. **Inbox = noise-heavy** — Automated alerts, FYIs, CCs dominate inbox
3. **Copilot constraints** — Already struggles with 30+ days; inbox would multiply volume
4. **Targeted queries solve gaps** — Response time, backlog, after-hours burden can be measured with focused prompts

---

## Implementation Phases

### Phase 1: Status Quo (Complete)
- `COPILOT_PROMPT.md` remains sent-only
- Primary value demonstration unchanged
- No disruption to existing workflow

### Phase 2: Supplementary Prompts (This Phase)
- Create `COPILOT_PROMPT_METRICS.md` with three targeted prompts:
  1. **Response Time Prompt** — Measure time from request to response
  2. **Backlog Visibility Prompt** — Identify unanswered requests
  3. **Enhanced After-Hours Prompt** — Capture when requests arrived, not just responses

### Phase 3: Testing and Validation (Future)
- Pilot supplementary prompts on 7-day windows
- Measure noise ratio (relevant vs irrelevant inbox items)
- Validate no double-counting with primary data
- Assess effort vs value for each prompt

### Phase 4: Integration (Future, If Validated)
- Add response time metrics to quarterly insights
- Add backlog summary to monthly reports
- Enhance after-hours burden calculations

---

## Files Created/Modified

| File | Action | Purpose |
|------|--------|---------|
| `docs/INBOX_DATA_IMPLEMENTATION_PLAN.md` | Created | This document |
| `docs/COPILOT_PROMPT_METRICS.md` | Created | Supplementary inbox prompts |
| `docs/COPILOT_PROMPT.md` | Unchanged | Primary sent-only prompt |
| `docs/COPILOT_PROMPT_AFTER_HOURS.md` | Unchanged | Supervisor after-hours prompt |

---

## Success Criteria

| Metric | Target |
|--------|--------|
| Response time data captured | 80%+ of replied-to requests |
| Backlog visibility | Identify requests with >48hr no response |
| Noise ratio acceptable | <30% irrelevant items in filtered results |
| No double-counting | 0 duplicates between primary and supplementary |
| Copilot performance | Supplementary prompts complete in <2 minutes |

---

## Usage Guidelines

### When to Use Primary Prompt (COPILOT_PROMPT.md)
- Weekly value tracking (every Friday)
- Monthly aggregation
- Standard workflow

### When to Use Supplementary Prompts (COPILOT_PROMPT_METRICS.md)
- Monthly or quarterly (not weekly)
- When preparing metrics for leadership
- When response time SLAs are questioned
- When backlog/capacity discussions arise

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Copilot performance degradation | Medium | High | Limit to 7-14 day ranges |
| Double-counting issues | Low | Medium | Clear deduplication guidance |
| Excessive manual cleanup | Medium | Medium | Strict filtering in prompts |
| Team confusion (too many prompts) | Low | Low | Clear documentation, optional use |

---

## Rollback Plan

If supplementary prompts prove too noisy or time-consuming:
1. Discontinue use of `COPILOT_PROMPT_METRICS.md`
2. Document lessons learned
3. Consider alternative data sources (calendar, ticketing system)

---

*Approved by: Applications Engineering Review*
*Date: January 2026*
