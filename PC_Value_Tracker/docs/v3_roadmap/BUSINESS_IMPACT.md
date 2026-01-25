# V3.0 — Business Impact Quantification

**Status:** Planning / Future Development

---

## Purpose

Convert Process Controls work into business language (dollars) rather than technical language (hours). Leadership responds to financial impact, not effort metrics.

---

## The Problem with Hours

| What We Say | What Leadership Hears |
|-------------|----------------------|
| "We spent 47 hours on AMP issues" | "That's your job" |
| "PC fixed 14 post-cutover problems" | "Thanks, I guess?" |
| "Team worked 34 after-hours" | "Everyone's busy" |

**Hours don't communicate impact.** Dollars do.

---

## Impact Categories

### 1. Direct PC Cost

The loaded cost of PC time spent on an issue.

```
PC Cost = Hours Spent × Loaded Hourly Rate

Example:
12 hours × $255/hr = $3,060
```

**Loaded hourly rate** includes:
- Base salary
- Benefits (typically 30-40% of salary)
- Overhead allocation

**How to get your rate:** Ask HR or Finance for the fully-loaded cost per hour for your job classification. If unavailable, estimate:
- Salary ÷ 2080 hours = base hourly
- Base hourly × 1.4 = approximate loaded rate

---

### 2. Production Impact

Lost production value due to downtime, delays, or reduced throughput.

```
Production Impact = Downtime Hours × Production Value per Hour
```

**How to get production value:**
- Ask Operations or Planning for "cost of downtime" per unit
- Ask Reliability Engineering — they use this for risk assessments
- Check turnaround planning documents — they calculate daily revenue loss

**Typical ranges (refinery context):**
| Unit Type | Downtime Cost ($/hr) |
|-----------|---------------------|
| Major process unit (FCC, Crude) | $50,000 - $150,000 |
| Medium unit (Reformer, Alky) | $20,000 - $50,000 |
| Small unit / utility | $5,000 - $20,000 |

**Example:**
```
Unit 12 Alkylation down 45 minutes due to PLC fault
Downtime cost: $60,000/hr
Impact: 0.75 hr × $60,000 = $45,000
```

---

### 3. Safety Impact

Translate safety events into risk exposure.

| Event Type | Typical Valuation |
|------------|------------------|
| Near-miss (no injury) | $5,000 - $25,000 (investigation cost + risk) |
| First aid case | $10,000 - $50,000 |
| Recordable injury | $50,000 - $200,000 |
| Lost time injury | $200,000 - $1,000,000+ |
| Process safety event | $500,000 - $10,000,000+ |

**Source:** Ask your HSE department or insurance/risk management for standard valuations.

**Note:** Be conservative with safety valuations. Overstatement damages credibility.

---

### 4. Contractor Rework Cost

If contractor deliverables required PC rework:

```
Rework Cost = PC Hours × Loaded Rate + Re-inspection Cost + Delay Cost
```

**For project issues:**
- Reference the original contractor cost for comparison
- "Contractor delivered at $X, required $Y in PC rework"

---

### 5. Risk Exposure (Technical Debt)

For legacy equipment, quantify the risk of failure:

```
Risk Exposure = Probability of Failure × Cost of Failure

Example:
PLC-5 failure probability: 15% per year (based on 3 faults in 3 years)
Cost of catastrophic failure: $2,000,000 (extended downtime + replacement)
Annual risk exposure: 0.15 × $2,000,000 = $300,000
```

**How to estimate failure cost:**
- Emergency replacement cost (premium pricing, expedited shipping)
- Extended downtime (vs. planned replacement during turnaround)
- Consequential damage (if failure causes other equipment damage)

---

## Impact Calculation Worksheet

Use this template for each accountability record:

```
IMPACT CALCULATION — Record #2026-XXX

1. DIRECT PC COST
   Hours spent:           ___ hrs
   Loaded rate:           $___ /hr
   PC Cost:               $___

2. PRODUCTION IMPACT
   Downtime:              ___ hrs
   Unit rate:             $___ /hr
   Production Impact:     $___

   Throughput reduction:  ___ %
   Duration:              ___ hrs
   Throughput Impact:     $___

3. SAFETY IMPACT
   Event type:            ___
   Standard valuation:    $___
   Safety Impact:         $___

4. REWORK / OTHER
   Description:           ___
   Cost:                  $___

─────────────────────────────────
TOTAL ESTIMATED IMPACT:   $___

Calculation Notes:
[Document sources and assumptions]
```

---

## Example: Full Impact Calculation

### Scenario: AMP Phase 3 Graphics Issues

```
IMPACT CALCULATION — Record #2026-037

1. DIRECT PC COST
   Hours spent:           12 hrs
   Loaded rate:           $255/hr
   PC Cost:               $3,060

2. PRODUCTION IMPACT
   Startup delay:         2 hrs
   Unit rate:             $2,500/hr (partial unit impact)
   Production Impact:     $5,000

   Operator inefficiency: Minor (not quantified)

3. SAFETY IMPACT
   Event type:            2 near-miss events (workarounds)
   Standard valuation:    $250 each (minor near-miss)
   Safety Impact:         $500

4. REWORK / OTHER
   None additional

─────────────────────────────────
TOTAL ESTIMATED IMPACT:   $8,560

Calculation Notes:
- Startup delay estimated by Operations shift supervisor
- Near-miss valuation is conservative (no injury potential)
- PC loaded rate from HR 2025 data
```

---

## Cumulative Impact Tracking

For recurring issues (especially Technical Debt), track cumulative impact:

```
CUMULATIVE IMPACT — Unit 12 PLC-5

Incident 1 (2025-03-15): $42,000
Incident 2 (2025-08-22): $38,000
Incident 3 (2026-01-08): $45,765

Cumulative Impact (12 months): $125,765

Replacement Cost: $85,000
ROI if Replaced: $125,765 ÷ $85,000 = 148%

RECOMMENDATION: Replacement would have paid for itself
in less than 12 months based on actual failure costs.
```

---

## Partnerships Required

To get accurate dollar values, build relationships with:

| Group | What They Provide |
|-------|------------------|
| **Operations / Planning** | Downtime cost per unit, throughput values |
| **Finance** | Loaded labor rates, standard cost models |
| **Reliability Engineering** | Risk assessment data, failure cost estimates |
| **HSE** | Safety event valuations, incident cost data |
| **Project Controls** | Contractor cost data, budget variances |
| **Insurance / Risk Mgmt** | Actuarial data, risk exposure models |

**Approach:** Frame as "We want to report impact in business terms. Can you help us use the right numbers?"

---

## Credibility Guidelines

### DO:
- Use documented sources (cite where numbers come from)
- Be conservative (understate rather than overstate)
- Show your math (calculation notes)
- Acknowledge uncertainty ("estimated," "approximately")
- Get buy-in on methodology from Finance/Operations

### DON'T:
- Inflate numbers to make a point
- Use numbers without sources
- Include speculative "what if" scenarios as actual impact
- Double-count (e.g., counting both downtime AND lost margin)

**Credibility is everything.** One inflated number discredits all your data.

---

## Standard Rates Reference

Maintain a reference sheet of standard rates (update annually):

```
PC VALUE TRACKER — STANDARD RATES (2026)

PC Loaded Hourly Rate:     $255/hr
Contractor Hourly Rate:    $175/hr (average)

Unit Downtime Costs ($/hr):
  FCC:                     $85,000
  Crude Unit:              $120,000
  Alkylation:              $60,000
  Reformer:                $45,000
  Utilities:               $8,000

Safety Event Valuations:
  Minor near-miss:         $250
  Significant near-miss:   $5,000
  First aid:               $15,000
  Recordable:              $75,000

Source: [Finance/Operations/HSE - Date obtained]
Last Updated: [Date]
```

---

## Presenting Impact Data

When presenting to leadership, lead with dollars:

### Before (V2.0 style):
> "PC spent 47 hours remediating AMP Phase 3 issues this month."

### After (V3.0 style):
> "AMP Phase 3 handoff failures cost approximately $97,000:
> - $12,000 in PC remediation time
> - $85,000 in production delays and startup issues
>
> 79% of these issues were preventable with PC involvement at FAT."

---

*V3.0 — Speak the language leadership understands.*
