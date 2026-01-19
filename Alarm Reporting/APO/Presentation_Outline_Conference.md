# ACM to APO Migration: A Practitioner's Guide
## Conference Presentation Outline (35 minutes)

**Target Audience:** Alarm management professionals, control engineers, operations leadership facing ACM to APO migration

**Presentation Objectives:**
- Raise awareness of migration complexity and common pitfalls
- Share real-world lessons learned from pilot implementations
- Generate interest in comprehensive whitepaper guidance
- Encourage early planning (ACM End of Support: Dec 31, 2027)

---

## Slide Structure (18-20 slides, ~2 min/slide)

### **Opening (Slides 1-3) - 5 minutes**

**Slide 1: Title Slide**
- ACM to APO Migration: A Practitioner's Guide to Alarm Database Migration Excellence
- Your Name, Marathon Petroleum Corporation
- Barbara Schubert, Contributing SME (27 years alarm management)
- Honeywell Users Conference 2026

**Slide 2: The Clock Is Ticking**
- ACM End of Support: December 31, 2027
- Hundreds of plants worldwide face forced migration
- The question: Migration by design or migration by desperation?
- Image/graphic: Countdown clock or calendar

**Slide 3: The Gap Between "Done" and "Operational Excellence"**
- Installation complete ≠ System works well
- "Migration complete" ≠ Achieving alarm management excellence
- This presentation: Honest assessment from early adopters
- What works, what doesn't, what's missing

---

### **Problem Definition (Slides 4-6) - 6 minutes**

**Slide 4: Common Migration Misconceptions (Top 5)**
1. "Migration is just a database copy" - Reality: Extensive transformation required
2. "Takes 2-4 weeks per site" - Reality: 6-12 months preparation needed
3. "Vendor tools handle everything" - Reality: Custom solutions essential
4. "Data quality can be fixed post-migration" - Reality: 10x harder in APO
5. "Licensing will transfer automatically" - Reality: Cannot reclaim excess licenses

**Slide 5: ACM vs. APO - Critical Feature Gaps**
- Missing functionalities (table/bullet list):
  - TagSync (missing in APO)
  - Bulk tag import/export (Excel rationalization only)
  - Easy drag-and-drop hierarchy UI
  - BMA support
  - TagList generation tool
- Message: "Vendor must disclose gaps for comprehensive assessment"

**Slide 6: What We Learned the Hard Way**
- Real pilot implementation challenges:
  - Underestimated pre-migration cleanup (6 months → 12 months)
  - License count 2.5x higher than expected (ghost tags)
  - Standard sync accuracy: 50-95% (not acceptable)
  - Health monitoring: Not included in standard delivery

---

### **Pre-Migration Critical Success Factors (Slides 7-10) - 8 minutes**

**Slide 7: License Crisis - A Cautionary Tale**
- Case Study: Site ordered licenses without database cleanup
- Result: 10,000+ ghost tags from Redirection Index entries
- HAMR databases: 30-40% ghost tags common
- Impact: Unplanned costs + performance degradation
- **Critical lesson: License optimization MUST precede ordering**

**Slide 8: Pre-Migration Assessment Checklist (Visual)**
- Database Health Assessment (traffic light: Red/Yellow/Green)
  - ACM database quality
  - M&R/HAMR ghost tags (30-40%!)
  - EMDB integrity
- Timeline: 6-12 months cleanup before migration
- Key message: "Cannot skip this phase"

**Slide 9: The 8-Step Migration Sequence**
1. Install HAMR (Reporting first!)
2. Cleanup HAMR (needs HAMR 2.3.0+)
3. Cleanup ACM (hierarchy + data quality)
4. Install/Migrate APO (parallel with ACM)
5. Run in parallel (30-90 days minimum)
6. Migrate custom tools
7. Delta migration (handle changes during parallel)
8. Switch (cutover when validated)

**Slide 10: Why This Order Matters**
- HAMR first: Validates data quality before APO
- Cleanup before migration: APO has limited cleanup tools
- Parallel operations: Critical for sites with enforcements
- Message: "Rushing this sequence = guaranteed problems"

---

### **Essential Custom Solutions (Slides 11-13) - 6 minutes**

**Slide 11: Standard Delivery Is Not Enough**
- Honeywell's own words: "APO is currently mainly enhanced Rationalization tool"
- Gap between installation and operational excellence
- Required custom solutions:
  1. Daily automated health checks (vendor doesn't provide)
  2. Enhanced Active Sync (standard = 50-95% accuracy)
  3. Full Suppressed Sync (missing key data)
  4. ACM maintenance tools

**Slide 12: Alternative Active Sync - A Game Changer**
- **Standard Sync Issues:**
  - Experion: 95% accuracy (70% for system alarms)
  - TPS: 50-93% accuracy (degrades over time)
  - Hybrid systems: No sync available
- **Alternative Active Sync (Barbara Schubert Method):**
  - File-based sync using notifdump
  - Near 100% accuracy, does not degrade
  - Successfully deployed: 6 major sites
- Comparison chart/graphic showing accuracy over time

**Slide 13: Case Study - When Standard Sync Fails**
- TPS site: Started 85% accuracy, degraded to 50% in 6 months
- Management decisions based on inaccurate KPIs
- Compliance risk, operator confidence lost
- Solution: Implemented Alternative Active Sync
- Result: 100% accuracy, consistently maintained

---

### **Migration Execution (Slides 14-15) - 4 minutes**

**Slide 14: Realistic Timeline Expectations**
- Phase 1: Pre-migration (6-12 months)
  - Assessment, cleanup, tool development
- Phase 2: Migration execution (2-4 weeks per site)
  - Data migration, testing, parallel operations
- Phase 3: Stabilization (30-90 days)
  - Monitoring, optimization, validation
- Buffer: 25-30% contingency time
- Total: 9-18 months project duration

**Slide 15: Testing - The Non-Negotiable Checklist**
- ☑ Hierarchy verification
- ☑ Tag count reconciliation (ACM vs APO)
- ☑ Enforcement testing (static + dynamic)
- ☑ Alarm Help validation
- ☑ Reporting integration (M&R/HAMR ↔ APO)
- ☑ Health checks operational
- ☑ Operator acceptance testing
- Message: "Go-live readiness = All checkboxes completed"

---

### **Lessons Learned (Slides 16-17) - 4 minutes**

**Slide 16: Top 5 Migration Pitfalls (with Icons)**
1. **Ghost Tag Crisis** - 30-40% license bloat + performance hit
2. **Skipping Parallel Operations** - Dynamic enforcements fail
3. **Inadequate Health Monitoring** - Issues undetected for weeks
4. **Over-reliance on Vendor** - Missing critical functionality
5. **Rushed Timeline** - Quality compromised, technical debt

**Slide 17: What Would We Do Differently?**
- Start database cleanup 12 months earlier
- Order licenses ONLY after database evaluation (not past license count)
- Implement Alternative Active Sync from day one
- Build custom health checks before go-live
- Allocate 50% more time for parallel operations
- Message: "Learn from our experience"

---

### **Closing (Slides 18-20) - 6 minutes**

**Slide 18: Call to Action - The Choice Is Yours**
- Migration by Design:
  - Start planning now (18+ months before deadline)
  - Comprehensive pre-migration cleanup
  - Essential custom solutions in place
  - Extended parallel operations
- Migration by Desperation:
  - Wait until 2027 deadline pressure
  - Rushed implementation
  - Technical debt and operational issues
  - Higher costs and risks

**Slide 19: Resources Available**
- **Comprehensive Whitepaper** (60-80 pages)
  - Detailed assessment checklists
  - Step-by-step cleanup procedures
  - Custom solution implementation guides
  - Case studies and lessons learned
  - Project timeline templates
- **Subject Matter Expertise**
  - Barbara Schubert consulting (27 years experience)
  - Alternative Active Sync implementation
  - Site assessments and audits
- Contact information / QR code to whitepaper

**Slide 20: Questions?**
- Contact information
- Email: [your email]
- Whitepaper download: [link or QR code]
- "Thank you - Happy to discuss your specific migration challenges"

---

## Presentation Delivery Notes

**Opening Impact (First 2 minutes):**
- Start with deadline urgency - immediate relevance
- Personal story: "Our first pilot taught us..."
- Set expectation: "Honest assessment, real challenges"

**Key Messages to Emphasize:**
1. **Timeline Reality:** 6-12 months pre-migration (not weeks)
2. **License Trap:** Cannot reclaim excess - optimize before ordering
3. **Standard Delivery Gap:** Vendor tools insufficient for excellence
4. **Alternative Active Sync:** Game-changing solution (100% vs 50-95%)
5. **Early Planning:** Start now to avoid desperation mode

**Audience Engagement Points:**
- Slide 4: "How many here think migration takes 2-4 weeks?" (show of hands)
- Slide 7: "Who has evaluated their ghost tag count?" (engagement)
- Slide 16: "Anyone facing these same pitfalls?" (relate to audience)

**Visual Recommendations:**
- Slide 2: Countdown clock graphic
- Slide 5: Red/yellow/green status indicators
- Slide 7: Cost impact graphic ($$$ visual)
- Slide 9: Process flow diagram (8 steps)
- Slide 12: Line chart (accuracy degradation vs constant)
- Slide 16: Icon-based infographic
- Slide 18: Two-path decision tree

**Timing Checkpoints:**
- 5 min: Through Slide 3
- 11 min: Through Slide 6
- 19 min: Through Slide 10
- 25 min: Through Slide 13
- 29 min: Through Slide 15
- 33 min: Through Slide 17
- 35 min: Questions begin

**Anticipated Questions (Prepare answers):**
1. "What's the typical cost for custom solutions?"
2. "Can we use your Alternative Active Sync scripts?"
3. "How do we convince management to allocate 6-12 months?"
4. "What if we're already behind schedule?"
5. "Does Honeywell support Alternative Active Sync?"
6. "What about sites with BMA requirements?"
7. "Can you share the whitepaper now?"

---

## Post-Presentation Follow-Up

**Immediate:**
- Whitepaper available for download (QR code / link)
- Business cards for one-on-one discussions
- Barbara Schubert contact info for consulting inquiries

**Within 1 Week:**
- Email slide deck to attendees
- Share whitepaper download link
- Offer 30-minute consultation calls

**Long-Term:**
- User group formation (shared lessons learned)
- Quarterly webinars on specific topics
- Case study contributions from other sites

---

**Total Slide Count:** 20 slides
**Estimated Duration:** 35 minutes + 15 min Q&A
**Presentation Style:** Practitioner-focused, honest, solution-oriented
