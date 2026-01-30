# ACM to APO Migration Whitepaper Project - Handoff Summary

**Last Updated**: January 20, 2026  
**Project Status**: Conference submission materials ready; whitepaper outline complete  
**Next Phase**: Presentation slide development and/or whitepaper content writing

---

## Project Overview

### Purpose
Create comprehensive industry guidance whitepaper on ACM (Alarm & Event Manager) to APO (Alarm Performance Optimizer) migration based on real-world Marathon Petroleum Corporation (MPC) pilot implementations. Target: Honeywell Users Conference 2026 presentation and published whitepaper.

### Critical Context
- **ACM End of Support**: December 31, 2027 (drives urgency for hundreds of plants)
- **Subject Matter Expert**: Barbara Schubert (BKS) - 27 years alarm management expertise
- **Honeywell Sensitivity**: Barbara is former Honeywell employee; DO NOT mention her name in conference materials or public documents due to Honeywell relationship sensitivities
- **MPC Pilots**: Real-world implementations at Marathon refineries provide credibility
- **Alternative Active Sync**: Custom methodology developed by BKS achieving near 100% accuracy vs 50-95% standard sync

---

## Current Project State

### Completed Documents

#### 1. **ACM_to_APO_Migration_Whitepaper_Outline.md** (PRIMARY MASTER FILE)
- **Status**: Complete with all Barbara's feedback integrated (40+ changes applied)
- **Format**: Word-compatible (uses ☐ ☑ instead of markdown checkboxes for DOCX conversion)
- **Structure**: 13 main sections + 10 appendices + 7 case studies
- **Character count**: ~60-80 pages estimated when fully written
- **Last major update**: Section 3 "Order of Activities" inserted, all sections renumbered
- **Purpose**: Master outline for both whitepaper writing and presentation development

**Key Structural Elements**:
- Section 1: Introduction (migration landscape, urgency, whitepaper purpose)
- Section 2: Understanding the Migration Landscape (12 myths debunked, stakeholder analysis)
- **Section 3: Order of Activities** (8-step migration sequence - CRITICAL NEW SECTION)
- Section 4: Pre-Migration Assessment (6-12 months, database health, license sizing)
- Section 5: Migration Planning (project structure, tooling, resource planning)
- Section 6: Migration Execution (initial sync, cutover, validation)
- Section 7: Post-Migration Activities (sustainment, enhancement, continuous improvement)
- Section 8: Custom Solutions and Enhancements (health checks, Alternative Active Sync)
- Section 9: Common Pitfalls and Lessons Learned (7 case studies including ghost tags, licensing)
- Section 10-13: Technology topics, future considerations, conclusion, acknowledgments

**Notable Case Studies** (Section 9.4):
1. License Based on Past Count (ordered without evaluating actual usage)
2. Ghost Tag License Crisis (30-40% ghost tags inflating costs and degrading HAMR performance)
3. Redirection Index Mismanagement
4. Dynamic Enforcement Migration
5. Incomplete Post-Cutover Checklist
6. Documentation Confidence Crisis
7. Change Management Resistance

**Appendices**:
- Appendix H: Alternative Active Sync Methodology (detailed implementation guide)
- Other appendices: Pre-migration checklist, health checks, project plan, testing plan, etc.

#### 2. **Executive_Summary_Conference_Submission.txt**
- **Status**: Ready for Honeywell Users Conference website submission
- **Character count**: 1097 characters (under 1100 limit)
- **Format**: All paragraphs (no bullet points per conference requirement)
- **Tone**: Collaborative with Honeywell, high-level, positive framing
- **Key message**: "Working with Honeywell's APO platform" / "complementary strategies"
- **Does NOT mention Barbara Schubert** (Honeywell sensitivity)
- **Audience**: Alarm management professionals, control engineers, operations leadership, project managers

#### 3. **Executive_Summary_Conference_Submission_Paragraph_Format.txt**
- **Status**: Alternative version (longer, more detailed)
- **Character count**: 1197 characters (exceeds conference limit but useful for other contexts)
- **Purpose**: Backup version for non-conference use (journal submission, webpage, brochure)
- **Removed Barbara reference** (Honeywell sensitivity addressed)

#### 4. **Presentation_Outline_Conference.md**
- **Status**: Complete comprehensive structure for 35-minute presentation + 15-minute Q&A
- **Slide count**: 20 slides with detailed speaker notes
- **Structure**:
  - Opening (3 slides, 5 min): Urgency, presenter background, overview
  - Problem Definition (3 slides, 6 min): Misconceptions, vendor gaps, why this matters
  - Pre-Migration (4 slides, 8 min): Order of Activities, license crisis, database health, timeline reality
  - Custom Solutions (3 slides, 6 min): Health checks, Alternative Active Sync, maintenance tools
  - Execution (2 slides, 4 min): Sync validation, cutover checklist
  - Lessons Learned (2 slides, 4 min): Top 5 pitfalls, case study highlights
  - Closing (3 slides, 6 min): Call to action, Q&A setup, contact/resources

**Key Features**:
- Timing checkpoints every 6 minutes
- Visual recommendations (countdown clock, traffic lights, line charts, decision tree)
- Audience engagement points (3 interactive questions)

#### 5. **ACM_to_APO_Migration_Comprehensive_Checklist.xlsx** (NEW - January 27, 2026)
- **Status**: Complete and ready for use
- **Format**: 11-sheet Excel workbook with Barbara's preferred structure
- **Sheet count**: Executive Summary + 9 phase sheets (Phase 0-9)
- **Task count**: 250+ comprehensive tasks covering full migration lifecycle

**Structure** (Barbara's chart method):
- Owner column (Site, Vendor, Custom, IT/OT)
- Status dropdown (☐ Not Started, ⏳ In Progress, ✓ Complete, ✗ Blocked, ⚠️ On Hold)
- Notes column for lessons learned
- Prerequisites column for dependencies
- Auto-numbering system (1.1, 1.2, 2.1, etc.)
- Collapsible sections with Excel grouping/outlining
- Color-coded headers and critical tasks

**Phase Structure**:
- Phase 0: Pre-Migration Assessment (6-12 months)
- Phase 1: Database Cleanup (Before License Order)
- Phase 2: Custom Solutions & Gap Mitigation
- Phase 3: APO Installation Planning
- Phase 4: OSW Completion
- Phase 5: Migration Execution Readiness
- Phase 6: APO Migration Execution
- Phase 7: Validation & Parallel Operations
- Phase 8: Cutover & Decommission
- Phase 9: Post-Migration Optimization

**Key Features**:
- Executive Summary with top 5 failure reasons and Critical Success Factors
- 30-40% ghost tag license savings documented
- ACM→APO feature gaps enumerated (8 major gaps)
- Marathon custom solutions list (9 proven tools)
- Training requirements ("what was lost" focus)
- Standards compliance checkpoints (ISA 18.2, EEMUA 191)

**Barbara's Feedback**: "I really like Excel format!!!" - Preferred over Word for tracking/checklist purposes
- Anticipated Q&A with 7 prepared responses
- Post-presentation follow-up strategy (QR code, email deck, consultation offers)

#### 5. **BKS_edits_extracted.txt** (Reference Only)
- **Status**: Archive/reference
- **Content**: Extracted text from Barbara's edited DOCX (1,006 lines)
- **Purpose**: Original source of Barbara's feedback; used to validate integration
- **Finding**: Structure nearly identical to original; Barbara approved overall approach

#### 6. **PPTX_extracted.txt** (Reference Only)
- **Status**: Archive/reference
- **Content**: 77 slides from "DynAMo Standard Sync and Alternative Active Sync v3.2.pptx"
- **Purpose**: Source material for Alternative Active Sync methodology
- **Key data**: Quality metrics (50-100% accuracy), deployment history (6 sites)

---

## Key Decisions and Rationale

### Title Evolution
**Final Title**: "Solving the Alarm Database Migration Challenge: A Practical Guide to ACM to APO Migration"

**Rationale**:
- Problem-framing approach ("solving the challenge") resonates with practitioners
- "Practical Guide" signals actionable content vs academic paper
- Balances professional credibility with compelling hook
- SEO-friendly with key terms (ACM, APO, migration, alarm, database)

**Previous titles considered**:
- "ACM to APO Migration: A Practitioner's Guide to Alarm Database Migration Excellence" (too generic)
- "Beyond the Vendor Promise" (too adversarial for Honeywell conference)

### Barbara Schubert Name Removal
**Decision**: Remove all references to Barbara Schubert from conference materials and public documents

**Rationale**:
- Barbara is former Honeywell employee
- Honeywell sensitive about former employees critiquing their products/tools
- Conference submission more likely to be accepted without potential controversy
- Changed to "decades of alarm management expertise across multiple Fortune 500 refineries"

**Files affected**:
- Executive_Summary_Conference_Submission.txt (updated)
- Executive_Summary_Conference_Submission_Paragraph_Format.txt (updated)
- Presentation_Outline_Conference.md (may need review for any mentions)

**Note**: Barbara CAN be acknowledged in final whitepaper appendix/acknowledgments section as technical contributor (not in main content or conference materials)

### Word-Compatible Format
**Decision**: Use Word-compatible checkbox symbols (☐ ☑) instead of markdown syntax (- [ ] - [x])

**Rationale**:
- Markdown checkboxes render as blank squares when converted to DOCX
- Word users need visible checkbox symbols
- Maintains usability across markdown editors and Word

### Section 3 Insertion
**Decision**: Insert new "Section 3: Order of Activities" showing 8-step migration sequence

**Rationale**:
- Barbara emphasized importance of activity sequencing
- Readers need high-level roadmap before diving into detailed sections
- Provides framework for understanding interdependencies
- All subsequent sections renumbered (original Section 3→4, etc.)

### Collaborative Tone for Conference
**Decision**: Rewrite executive summary with collaborative tone emphasizing partnership with Honeywell

**Rationale**:
- Conference review board looks favorably on collaborative vs adversarial presentations
- "Working with Honeywell's APO platform" vs "vendor tools are insufficient"
- "Complementary strategies that enhance" vs "gaps in standard delivery"
- Increases acceptance probability while maintaining technical value

---

## Technical Details

### Python Environment
- **Location**: C:/Users/GF99/Documentation/.venv
- **Python Version**: 3.13+
- **Packages Installed**: python-pptx, python-docx, pdfplumber, pypdf, pandas, openpyxl, pillow, pytesseract

### Document Extraction Process
1. **DOCX Extraction**: Used python-docx to extract Barbara's edited whitepaper
   - Issue: Unicode encoding error for '≠' character
   - Solution: sys.stdout.reconfigure(encoding='utf-8')
   - Output: BKS_edits_extracted.txt (1,006 lines)

2. **PPTX Extraction**: Used python-pptx to extract Alternative Active Sync presentation
   - Package installation required: pip install python-pptx
   - Output: PPTX_extracted.txt (77 slides)
   - Key slides identified: 14, 16, 50, 56-57 (for future figure extraction)

### Integration Workflow
1. Extracted Barbara's DOCX and PPTX
2. Analyzed differences (structure nearly identical, minor wording changes)
3. Identified high-value content: Alternative Active Sync methodology, quality metrics, case studies
4. Integrated into outline using multi_replace_string_in_file (5 initial replacements)
5. User provided 40+ detailed section-by-section updates (recorded while tools disabled)
6. Applied all 40+ changes in batch operations
7. Fixed section numbering after Section 3 insertion
8. Consolidated to single Word-compatible file
9. Updated case studies (added licensing case study, updated ghost tags with 30-40% impact)
10. Created conference materials (executive summary, presentation outline)

---

## Character Count Constraints

### Conference Submission Limit: 1100 characters
- **Current executive summary**: 1097 characters (3 under limit) ✅
- **Paragraph format version**: 1197 characters (97 over limit) ⚠️ (for non-conference use)

### Counting Method
Total characters including:
- Title
- All body text
- Spaces and punctuation
- Line breaks count as 1 character each

**Exclude from count**:
- Separator lines (---)
- Character count notation line itself
- Any metadata below separator

---

## Important Context for AI Agents

### User's Communication Style
- Prefers direct, actionable communication
- Values efficiency (multi_replace_string_in_file over sequential edits)
- Iterative refinement approach (provide options, get feedback, adjust)
- Appreciates title/heading recommendations with multiple alternatives
- Likes "mix" approach when combining multiple suggestions

### Project Constraints
1. **Honeywell Sensitivity**: Barbara Schubert cannot be mentioned in conference/public materials
2. **Character Limits**: Conference submission strictly under 1100 characters
3. **No Bullet Points**: Conference website form explicitly prohibits bullet points
4. **Collaborative Tone**: Conference materials must position work as complementary to Honeywell, not critical
5. **Word Compatibility**: Use ☐ ☑ symbols, not markdown checkbox syntax

### Technical Accuracy Requirements
- All technical content validated by Barbara (27 years expertise)
- Marathon Petroleum pilot implementations provide real-world credibility
- Specific metrics must be accurate (e.g., 30-40% ghost tags, 50-95% vs 100% sync accuracy)
- Case studies based on actual pilot experiences

### File Management Rules
- **Primary file**: ACM_to_APO_Migration_Whitepaper_Outline.md (Word-compatible format)
- **Archive files**: Keep BKS_edits_extracted.txt and PPTX_extracted.txt for reference
- **Conference files**: Two executive summaries (under 1100 for submission, longer for other use)
- **No duplicate formats**: Consolidated to single primary file (removed original markdown version)

---

## Next Steps / Pending Work

### Immediate Priority: Conference Submission
1. **Submit Executive_Summary_Conference_Submission.txt** to Honeywell Users Conference website
2. Prepare speaker bio and headshot
3. Confirm presentation slot preferences and A/V requirements
4. Register Barbara Schubert as contributing co-author (if allowed; check with her first)

### Phase 1: Presentation Development (After Acceptance)
1. **Create PowerPoint slides** from Presentation_Outline_Conference.md
   - 20 slides with recommended visuals:
     - Countdown clock graphic (Slide 2)
     - Traffic light indicators for database health (Slide 8)
     - 8-step process flow diagram (Slide 9)
     - Line chart: sync accuracy degradation vs constant (Slide 12)
     - Cost impact visualization (Slide 7)
     - Icon-based infographic for top 5 pitfalls (Slide 16)
     - Two-path decision tree: design vs desperation (Slide 18)
   - Add QR code linking to whitepaper download
   - Practice with timing checkpoints (5, 11, 19, 25, 29, 33, 35 minutes)

2. **Extract PPTX Diagrams for Presentation**
   - Slides 14, 16, 50, 56-57 from Alternative Active Sync PPTX
   - Convert to high-quality images (PNG/SVG)
   - Add to presentation slides

### Phase 2: Comprehensive Checklist Validation
1. **Review with Barbara** (When she returns)
   - Share ACM_to_APO_Migration_Comprehensive_Checklist.xlsx for validation
   - Verify custom solutions match Marathon's actual tools
   - Confirm timeline estimates (6-12 months Phase 0, etc.)
   - Get final approval before any public sharing

2. **Optional Excel Hierarchy Documentation** (If Barbara requests)
   - Create additional spreadsheet showing section hierarchy
   - Purpose: Visual roadmap of checklist structure
   - Format: Tree/outline view with phase dependencies

### Phase 3: Whitepaper Content Writing
1. **Expand outline sections into full prose** (priority order):
   - Section 1: Introduction (2-3 pages)
   - Section 2: Understanding Migration Landscape (4-5 pages)
   - Section 3: Order of Activities (2-3 pages)
   - Section 9: Common Pitfalls with 7 case studies (4-5 pages)
   - Sections 4-8: Core technical content (30-40 pages)
   - Sections 10-13: Conclusion and forward-looking (5-7 pages)

2. **Develop Appendices**:
   - Appendix A: Pre-Migration Assessment Checklist (~100 items)
   - Appendix D: Daily Health Check Configuration Examples (sample scripts)
   - Appendix E: Sample Migration Project Plan (Gantt chart template)
   - Appendix H: Alternative Active Sync Implementation Guide (step-by-step with screenshots)
   - Other appendices as outlined

3. **Add Figures and Tables**:
   - Extract diagrams from Alternative Active Sync PPTX
   - Create process flow diagrams for 8-step sequence
   - Add tables for comparison matrices (standard vs enhanced sync, etc.)
   - Create figure captions and cross-references

4. **Technical Validation**:
   - Review draft sections with Barbara Schubert
   - Validate all technical claims and metrics
   - Confirm case study details with MPC team
   - Peer review by other alarm management experts

### Phase 3: Publication and Distribution
1. Professional editing and formatting
2. Create PDF version for distribution
3. Upload to conference website / user group portal
4. Develop companion materials (cheat sheets, quick reference guides)
5. Plan follow-up webinar or workshop series

---

## Reference Information

### Alternative Active Sync Methodology
**Key Achievement**: Near 100% accuracy vs 50-95% standard sync

**Deployment History**: 6 sites successfully implemented

**Quality Metrics**:
- Standard sync: 50-95% accuracy (degrades over time)
- Alternative Active Sync: Maintains near 100% accuracy
- Critical for accurate KPIs and alarm performance tracking

**Implementation**: See Appendix H in whitepaper outline (to be developed)

**Source**: 77-slide presentation by Barbara Schubert

### Migration Timeline Reality
- **Vendor claim**: 2-4 weeks
- **Actual reality**: 6-12 months for proper migration
- **Pre-migration work**: 6-12 months minimum (database cleanup, assessment, planning)
- **Execution**: Several weeks to months (depending on database size and complexity)
- **Post-migration sustainment**: Ongoing commitment

### License Sizing Critical Lesson
- **Problem**: Cannot reclaim excess licenses after ordering
- **Root cause**: License orders based on past counts without evaluating actual current usage
- **Ghost tags**: 30-40% of database may be orphaned tags (not in active use)
- **Impact**: Both cost inflation and performance degradation (especially HAMR)
- **Solution**: Must evaluate actual current database usage before ordering

### Migration Myths Debunked (Section 2.2)
Expanded from 5 to 12 myths based on Barbara's feedback:
1. Migration is quick and straightforward
2. Pre-migration cleanup can be done post-migration
3. Standard sync is sufficient
4. Vendor tools handle everything
5. Testing can be abbreviated
6. Documentation is optional
7. Change management is just training
8. Old enforcements work in APO
9. License sizing is simple
10. Cutover can be rushed
11. Post-migration is just monitoring
12. One-size-fits-all approach works

---

## File Locations and Purposes

### Active Project Files
```
C:\Users\GF99\Documentation\Alarm Reporting\APO\
├── ACM_to_APO_Migration_Whitepaper_Outline.md (PRIMARY - Word-compatible)
├── Executive_Summary_Conference_Submission.txt (1097 chars - for conference)
├── Executive_Summary_Conference_Submission_Paragraph_Format.txt (1197 chars - backup)
├── Presentation_Outline_Conference.md (20 slides, 35 min)
├── ACM_to_APO_Migration_Comprehensive_Checklist.xlsx (11 sheets, 250+ tasks)
├── CHECKLIST_CREATION_SUMMARY.md (checklist documentation)
└── PROJECT_HANDOFF_SUMMARY.md (this document)
```

### Reference/Archive Files
```
C:\Users\GF99\Documentation\Alarm Reporting\APO\
├── BKS_edits_extracted.txt (Barbara's DOCX extraction - 1,006 lines)
├── PPTX_extracted.txt (Alternative Active Sync presentation - 77 slides)
└── APO_Documentation_Analysis_Summary.md (early analysis)
```

### Source Documents (Not in Git)
- ACM_to_APO_Migration_Whitepaper_Outline_BKS edits.docx (Barbara's edited outline)
- DynAMo Standard Sync and Alternative Active Sync v3.2.pptx (methodology presentation)

---

## Git Repository Status

**Last Commit**: "Update executive summaries: remove Barbara reference, add paragraph format version"
- Date: January 19, 2026
- Changes: Executive summaries updated, title changed, several alarm reporting files added

**Branch**: main

**Key Changes History**:
1. Initial outline creation
2. DOCX and PPTX extraction
3. Integration of Alternative Active Sync methodology (5 replacements)
4. Application of 40+ granular updates from Barbara's review
5. Section 3 insertion and renumbering
6. File consolidation to Word-compatible format
7. Case study additions and updates
8. Conference materials creation
9. Executive summary Barbara reference removal
10. Title update to current version
11. Collaborative tone revision for conference

---

## Contact and Collaboration

### Key Stakeholders
- **Barbara Schubert (BKS)**: Subject matter expert, 27 years alarm management expertise (former Honeywell)
- **Marathon Petroleum Corporation**: Pilot implementation sites (credibility source)
- **Honeywell Users Conference**: Target venue for presentation
- **Alarm management community**: Target audience for whitepaper

### Presentation Venue
- **Event**: Honeywell Users Conference 2026
- **Format**: 35-minute presentation + 15-minute Q&A (50 minutes total)
- **Audience**: Alarm management professionals, control engineers, operations leadership, project managers
- **Submission deadline**: TBD (likely early 2026 for fall conference)

---

## AI Agent Instructions

### When Working on This Project:

1. **Always check Barbara name sensitivity**: DO NOT mention Barbara Schubert in conference materials or public documents. Use generic phrasing like "decades of alarm management expertise" or "experienced practitioners."

2. **Respect character limits**: Conference executive summary MUST be under 1100 characters. Count carefully including title, body, spaces, punctuation, line breaks.

3. **Maintain collaborative tone for Honeywell**: When working on conference materials, frame content as "working with Honeywell's APO platform" and "complementary strategies" rather than "vendor gaps" or "insufficient tools."

4. **Use Word-compatible format**: When editing whitepaper outline, use ☐ and ☑ symbols, not markdown checkbox syntax (- [ ] or - [x]).

5. **Verify section numbering**: After any section insertions or deletions, check that ALL section numbers are sequential (1-13 currently) throughout document.

6. **Preserve case study details**: 7 case studies in Section 9.4 with specific lessons (ghost tags 30-40%, licensing crisis, etc.). Don't lose these details.

7. **Reference presentation outline for slide development**: Presentation_Outline_Conference.md has detailed speaker notes, timing, visual recommendations - use as blueprint.

8. **Check character counts after ANY edit**: Executive summaries must stay under limits. Recount and update character count line after edits.

9. **Maintain technical accuracy**: All metrics, percentages, and technical claims validated by Barbara. Don't change without verification.

10. **Use multi-replace for efficiency**: When making multiple independent edits, use multi_replace_string_in_file tool rather than sequential replace_string_in_file calls.

11. **Excel formatting best practices** (from checklist creation):
    - **Avoid openpyxl conditional formatting**: Causes XML errors when opening in Excel. Use manual color highlighting instead.
    - **Use data validation dropdowns**: Reliable for status columns and controlled vocabularies.
    - **Use Excel grouping/outlining**: `ws.row_dimensions.group()` for collapsible sections works perfectly.
    - **Test in Excel**: Always verify generated files open without recovery prompts.
    - **Hierarchical numbering**: Maintain auto-numbering systems (1.1, 1.2, 2.1) for easy add/rearrange.

### Common User Requests to Anticipate:
- "Create PowerPoint slides from presentation outline"
- "Start writing Section [X] of whitepaper"
- "Extract diagrams from PPTX"
- "Review executive summary character count"
- "Update title across all documents"
- "Make conference materials more/less collaborative"
- "Add case study about [topic]"
- "Develop Appendix [X]"
- "Create/modify Excel checklist" (uses create_comprehensive_checklist.py with openpyxl)

---

## Version History

**v1.2** - January 27, 2026
- Added comprehensive checklist spreadsheet (11 sheets, 250+ tasks)
- Enhanced with Barbara's feedback: auto-numbering, dropdowns, collapsible sections
- Fixed Excel XML errors by removing conditional formatting
- Added Excel formatting best practices to AI Agent Instructions

**v1.1** - January 25, 2026
- Minor documentation updates
- Conference submission preparation

**v1.0** - January 20, 2026
- Initial handoff summary created
- All major decisions and context documented
- Conference submission materials ready
- Whitepaper outline complete with 40+ Barbara updates integrated

---

## Quick Reference: Character Counts

| Document | Current Count | Limit | Status |
|----------|---------------|-------|--------|
| Executive_Summary_Conference_Submission.txt | 1097 | 1100 | ✅ Ready |
| Executive_Summary_Conference_Submission_Paragraph_Format.txt | 1197 | N/A | ℹ️ Backup version |

---

## Quick Reference: Section Structure

**Whitepaper Sections** (13 total):
1. Introduction
2. Understanding the Migration Landscape
3. Order of Activities *(NEW - inserted)*
4. Pre-Migration Assessment
5. Migration Planning
6. Migration Execution
7. Post-Migration Activities
8. Custom Solutions and Enhancements
9. Common Pitfalls and Lessons Learned (7 case studies)
10. Technology Considerations
11. Future Considerations
12. Conclusion
13. Acknowledgments and Contributors

**Appendices** (10 total): A through J
- **Appendix H**: Alternative Active Sync (most detailed)

---

**End of Handoff Summary**
