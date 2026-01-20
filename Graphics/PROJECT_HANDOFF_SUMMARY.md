# Experion HMI Graphics FAT Support - Project Handoff

**Document Version:** 1.0  
**Last Updated:** January 20, 2026  
**Project Status:** Completed - Documentation Phase  
**Maintenance Priority:** Medium - Reference documentation for future projects

---

## Executive Summary

This project developed comprehensive Factory Acceptance Test (FAT) documentation for validating Honeywell Experion HMI graphics. The deliverable is a professional, reusable checklist-driven document that ensures graphics meet Marathon Petroleum and Honeywell standards before deployment.

**Primary Deliverable:** `Experion_HMI_FAT_Support_Document_REVISED.md` - A 771-line comprehensive FAT framework with embedded checklists, troubleshooting workflows, and formal acceptance procedures.

---

## Project Context & Purpose

### Business Need

When Marathon Petroleum receives Experion HMI graphics from vendors, there was no standardized process for systematic validation during Factory Acceptance Testing. This led to:
- Inconsistent graphics quality reaching production
- Performance issues discovered late in deployment
- Unclear acceptance criteria causing disputes
- Repeated validation work on similar projects

### Solution Delivered

A comprehensive FAT support document that provides:
1. **Structured checklists** covering static elements, dynamic behavior, navigation, alarms, and performance
2. **Quantitative benchmarks** from Honeywell specifications (call-up times, DOM limits, script performance)
3. **HLV log analysis workflows** for systematic error remediation
4. **Issue tracking framework** with severity classifications
5. **Formal acceptance procedures** with signature blocks
6. **Copilot automation prompts** for accelerated validation

---

## Repository Structure

```
Graphics/
├── Experion_HMI_FAT_Support_Document_REVISED.md    # PRIMARY DELIVERABLE (771 lines)
├── Experion_HMI_FAT_Support_Document_REVISED.pdf   # Print-ready version
├── Experion_HMI_Copilot_Prompts.md                 # AI-assisted validation prompts (154 lines)
├── README_Copilot_Prompts.md                       # Copilot prompt cheat sheet
├── README.md                                        # Project overview and Docker setup
├── Experion_HMI_FAT_Support.txt                    # Original draft/template (136 lines)
├── Experion_HMI_FAT_Support_Document_with_Prompts.md  # Draft version with prompts
├── Checklist.md                                     # Empty placeholder (deprecated)
│
├── AMP-LAR-AUT-SPC-0050 Rev 1 - BPCS HMI Style Guide.pdf  # Reference material
├── Display Performance Analysis Report-Steps.pdf     # Honeywell guidance
├── display_sizingrev3.pdf                           # Display sizing standards
├── pmt-hps-hmiweb-display-building-guide-epdoc-xx54-en-520a.pdf  # HMIWeb reference
└── Station DCG_Rev3.pdf                             # Station design criteria
```

---

## Reference Materials Used

### Primary Standards & Specifications

1. **AMP-LAR-AUT-SPC-0050 Rev 1** - Marathon Petroleum BPCS HMI Style Guide
   - **Source:** Local PDF in Graphics folder
   - **Key Content:**
     - Line thickness: Process=2pt, Instrument=1pt
     - Grayscale/color conventions (ASM compliance)
     - Equipment labeling standards
     - Navigation element placement
   - **Usage:** Cited in 15+ checklist items (SE-03, DE-03, etc.)

2. **Experion PKS R520** - Honeywell Platform Specification
   - **Source:** Honeywell official documentation
   - **Key Content:**
     - HMI specification standards
     - Script performance limits (<100ms execution)
     - System architecture requirements
   - **Usage:** Performance benchmarks (PM-07), scope definition

3. **Display Builder Assistant** - Honeywell Performance Tool
   - **Source:** Honeywell software tool documentation
   - **Key Content:**
     - DOM node count limits (<1500 nodes)
     - Performance analysis methodology
     - Report interpretation guide
   - **Usage:** PM-06, troubleshooting sections (Section 3.2)

4. **HMIWeb Display Building Guide** (pmt-hps-hmiweb-display-building-guide-epdoc-xx54-en-520a.pdf)
   - **Source:** Local PDF in Graphics folder
   - **Key Content:**
     - VBScript event handling (OnTimer, OnChange, etc.)
     - DOM structure best practices
     - Image optimization techniques

5. **Display Performance Analysis Report - Steps** (Local PDF)
   - **Source:** Local PDF in Graphics folder
   - **Key Content:**
     - Step-by-step performance testing
     - Metric collection procedures
     - Report generation process

6. **Display Sizing Rev 3** (display_sizingrev3.pdf)
   - **Source:** Local PDF in Graphics folder
   - **Key Content:**
     - Screen resolution standards (1920x1080)
     - Display element sizing guidelines
     - Multi-monitor configurations

7. **Station DCG Rev 3** (Station DCG_Rev3.pdf)
   - **Source:** Local PDF in Graphics folder
   - **Key Content:**
     - Station design criteria
     - Hardware specifications
     - System architecture

### Industry Standards Referenced

8. **Abnormal Situation Management (ASM)** - Industry Best Practices
   - **Source:** General industry knowledge (ASM Consortium, ISA)
   - **Key Principles:**
     - Grayscale for normal operation
     - Color reserved for alarms/abnormal states
     - Screen density limits (<60% coverage)
     - High-contrast alarm visibility

9. **Experion Alarm Philosophy** (Project-Specific)
   - **Source:** Referenced but not included in repo
   - **Key Content:**
     - Alarm priority definitions (Critical/High/Medium/Low)
     - Color coding: Critical=Red, High=Orange, Medium=Yellow
     - Response time requirements

10. **Control Builder Documentation** (Honeywell)
    - **Source:** Honeywell official documentation
    - **Key Content:**
      - Controller configuration procedures
      - Tag structure standards
      - Configuration backup procedures

---

## Document Evolution History

### Initial Version (Experion_HMI_FAT_Support.txt)
- **Purpose:** Basic template with minimal structure
- **Content:** 136 lines, simple checklists
- **Limitations:** 
  - No quantitative benchmarks
  - Limited troubleshooting guidance
  - No HLV log workflows
  - Missing formal acceptance procedures

### Revised Version (Experion_HMI_FAT_Support_Document_REVISED.md)
- **Purpose:** Comprehensive, professional FAT framework
- **Content:** 771 lines with 15 detailed checklist categories
- **Enhancements:**
  - Added 50+ specific checklist items with acceptance criteria
  - Embedded quantitative performance benchmarks
  - Created HLV log analysis workflow with PowerShell examples
  - Added Display Builder Assistant integration
  - Included formal issue tracking matrix
  - Professional formatting with page breaks for printing
  - Signature blocks and acceptance criteria
  - Glossary and revision tracking

### Copilot Integration (Experion_HMI_Copilot_Prompts.md)
- **Purpose:** AI-assisted validation automation
- **Content:** 154 lines of categorized VS Code Copilot prompts
- **Capabilities:**
  - Automated style guide conformance checks
  - Script performance analysis
  - DOM complexity ranking
  - Trend configuration auditing
  - Point mapping integrity validation
  - Refactoring suggestions

---

## Key Design Decisions

### 1. Checklist-Based Approach
**Decision:** Organize validation around comprehensive checklists rather than narrative guidance.

**Rationale:**
- Ensures systematic coverage (nothing skipped)
- Provides clear pass/fail criteria
- Supports formal acceptance signatures
- Enables checklist reuse across projects

**Implementation:**
- 6 major checklist categories
- Pass/Fail columns with Notes
- Reference file/line columns for traceability
- Severity classifications (High/Med/Low)

### 2. Quantitative Performance Benchmarks
**Decision:** Include specific numeric targets from Honeywell documentation.

**Rationale:**
- Eliminates ambiguity ("fast enough" → "< 2 seconds")
- Enables objective testing
- Provides vendor accountability
- Supports performance regression detection

**Benchmarks Included:**
- Display call-up time: <2s (simple) / <5s (complex)
- DOM node count: <1500 nodes
- Script execution: <100ms for events
- Trend pens: ≤8 per display
- Data update rate: 1-2 seconds
- Navigation response: <500ms
- Trend update latency: <2 seconds

### 3. HLV Log Workflow Integration
**Decision:** Embed detailed HLV log analysis as a core pre-FAT requirement.

**Rationale:**
- HLV logs catch 80%+ of graphics errors before FAT
- Clean logs are mandatory for Honeywell best practices
- Systematic workflow prevents "whack-a-mole" debugging

**Workflow Steps:**
1. Extract and filter ERROR entries
2. Categorize by display
3. Create remediation matrix
4. Fix, test, verify
5. Archive clean log as deliverable

### 4. Page Break Formatting
**Decision:** Insert page breaks after major sections for professional printing.

**Rationale:**
- Document used in formal FAT meetings (printed copies)
- PDF export to clients and vendors
- Professional appearance for stakeholder review
- Section isolation for signature pages

**Implementation:**
```markdown
<div style="page-break-after: always;"></div>
```
Inserted after: Executive Summary, Pre-Test Setup, each major checklist, troubleshooting, signatures

### 5. Copilot Prompt Separation
**Decision:** Create separate Copilot prompts document rather than embedding in FAT doc.

**Rationale:**
- Different audiences (engineers vs. AI)
- Allows independent updates
- Cleaner FAT document for client review
- Enables prompt library reuse

---

## Performance Benchmark Reference Table

| Metric                       | Target                     | Source                  | Checklist Item |
| ---------------------------- | -------------------------- | ----------------------- | -------------- |
| Display Call-Up (Simple)     | < 2 seconds                | Experion R520           | PM-01          |
| Display Call-Up (Complex)    | < 5 seconds                | Experion R520           | PM-01          |
| Data Update Rate             | 1-2 seconds                | Experion R520           | PM-02          |
| Trend Update Latency         | < 2 seconds                | Experion R520           | PM-03          |
| Max Trend Pens per Display   | ≤ 8 pens                  | Honeywell Guidance      | PM-04          |
| Trend Sampling Rate          | ≥ 1 second intervals      | Honeywell Guidance      | PM-05          |
| DOM Node Count               | < 1500 nodes               | Display Builder Asst.   | PM-06          |
| Script Execution Time        | < 100ms                    | Experion R520           | PM-07          |
| Memory Usage per Display     | Baseline + 20% max         | Project Standard        | PM-08          |
| Navigation Responsiveness    | < 500ms                    | Project Standard        | PM-10          |
| Screen Coverage Density      | < 60% coverage             | ASM Best Practices      | SE-12          |
| Alarm Color Standards        | Critical=Red, High=Orange  | ASM / Alarm Philosophy  | AE-09          |
| Process Line Thickness       | 2pt                        | AMP-LAR-AUT-SPC-0050    | SE-03          |
| Instrument Line Thickness    | 1pt                        | AMP-LAR-AUT-SPC-0050    | SE-03          |

---

## Critical Workflows

### Workflow 1: HLV Log Analysis & Remediation

**Purpose:** Systematic error elimination before FAT

**Steps:**

1. **Extract Errors:**
   ```powershell
   Get-Content "C:\ProgramData\Honeywell\HMIWebLog\Log.txt" | 
   Select-String "ERROR" | 
   Out-File "HLV_Errors_Summary.txt"
   ```

2. **Categorize by Display:**
   - Group errors by graphic file name
   - Prioritize displays with multiple errors
   - Identify patterns (same error across multiple displays)

3. **Create Remediation Matrix:**
   | Display           | Error Type         | Line # | Severity | Status | Assigned | Target Date |
   | ----------------- | ------------------ | ------ | -------- | ------ | -------- | ----------- |
   | P101_Overview.htm | Undefined Variable | 127    | ERROR    | Open   | Dev      | 2026-01-10  |

4. **Fix-Test-Verify Loop:**
   - Implement fix in Display Builder
   - Save and deploy updated graphic
   - Re-run HLV validation
   - Check HLV log for clearance
   - Document fix in change log

5. **Final Verification:**
   - Run full HLV validation on all graphics
   - Confirm zero ERROR entries
   - Archive clean HLV log as FAT deliverable

### Workflow 2: Display Builder Assistant Performance Analysis

**Purpose:** Identify overloaded graphics before FAT

**Steps:**

1. **Run Analysis:** Tools → Display Builder Assistant → Analyze All Displays
2. **Review Report:** `<Project>\Reports\DisplayPerformance_<timestamp>.xml`
3. **Flag Violations:**
   - DOM nodes > 1500
   - Heavy scripts in OnTimer/OnChange
   - Excessive trend pens
   - Large image files
4. **Implement Fixes:**
   - Flatten nested groups
   - Consolidate shapes
   - Move logic from OnTimer to change-based events
   - Optimize/compress images
5. **Re-test:** Confirm metrics within targets

### Workflow 3: FAT Execution

**Purpose:** Formal acceptance testing procedure

**Steps:**

1. **Pre-Test Setup (Section 1):**
   - Validation reports with green checks
   - Clean HLV logs
   - Design approvals signed-off
   - Test environment prepared

2. **Execute Checklists (Section 2):**
   - Static Elements (15 items)
   - Dynamic Elements (15 items)
   - Navigation & Usability (11 items)
   - Alarm & Event Management (9 items)
   - Performance Metrics (10 items)
   - Compliance & Standards (varies)

3. **Log Issues (Section 6):**
   - Issue tracking matrix
   - Severity classification
   - Root cause analysis
   - Resolution documentation

4. **Verify Deliverables (Section 5):**
   - Test logs and results
   - Issue resolution summary
   - Performance metrics report
   - Updated graphics package
   - As-built documentation

5. **Formal Acceptance (Section 7):**
   - Signature collection
   - Pass/Conditional Pass/Fail determination
   - Comments documentation
   - Archive acceptance package

---

## AI Agent Instructions for Maintenance

### For Future AI Agents Working with This Content

**Context Awareness:**
- This is a **reference document** for industrial control system graphics validation
- Content is based on **Honeywell Experion R520** platform specifics
- Standards are derived from **AMP-LAR-AUT-SPC-0050 Rev 1** (Marathon Petroleum internal)
- Document must remain **platform-specific** to Experion HMI technology

**When Updating This Document:**

1. **Always Preserve:**
   - Quantitative benchmarks (don't generalize "< 2 seconds" to "fast")
   - Specific reference citations (AMP-LAR-AUT-SPC-0050, R520, etc.)
   - Checklist structure and numbering (SE-01, DE-01, etc.)
   - Page break formatting (for printing/PDF export)
   - Signature blocks and acceptance criteria
   - HLV log file paths and PowerShell commands

2. **Reference Before Changes:**
   - Read `AMP-LAR-AUT-SPC-0050 Rev 1 - BPCS HMI Style Guide.pdf` for style standards
   - Check `pmt-hps-hmiweb-display-building-guide-epdoc-xx54-en-520a.pdf` for technical accuracy
   - Verify performance numbers against Honeywell documentation

3. **Update Triggers:**
   - New Experion release (update R520 references to R530, R600, etc.)
   - Revised Marathon style guide (update AMP-LAR-AUT-SPC-0050 revision number)
   - New performance benchmarks from Honeywell
   - Lessons learned from actual FAT execution

4. **Version Control:**
   - Update "Document Revision History" table at end of document
   - Increment version number in Document Control table
   - Document specific changes in revision notes

5. **Consistency Requirements:**
   - Maintain parallel structure across all checklist sections
   - Keep table column headers consistent (Pass/Fail/Notes/Ref. File/Line)
   - Use same severity levels (High/Med/Low) throughout
   - Preserve glossary entries when adding new technical terms

### Common Update Scenarios

**Scenario 1: New Experion Release (e.g., R530)**
```markdown
ACTION: Global find/replace "R520" → "R530"
VERIFY: Check if benchmarks changed (review Honeywell release notes)
UPDATE: Document Control table (Experion Version field)
UPDATE: References section with new documentation titles
```

**Scenario 2: Updated Style Guide (e.g., Rev 2)**
```markdown
ACTION: Review new style guide for changed standards
UPDATE: Affected checklist items (especially Static Elements section)
UPDATE: All citations "AMP-LAR-AUT-SPC-0050 Rev 1" → "Rev 2"
VERIFY: Line thickness, color codes, navigation standards still accurate
```

**Scenario 3: New Performance Benchmark from Honeywell**
```markdown
ACTION: Update affected checklist item (PM-XX)
ADD: New row to Performance Benchmark Reference Table in this handoff
UPDATE: Troubleshooting guide with new optimization strategies
VERIFY: Acceptance criteria still achievable with new benchmark
```

**Scenario 4: Field Feedback from Actual FAT**
```markdown
ACTION: Review issues encountered in real FAT execution
ADD: New troubleshooting entries to Section 3
EXPAND: Checklist items if gaps identified
UPDATE: Best practices section with lessons learned
```

### AI Prompt Templates for Updates

**For Adding New Checklist Items:**
```
Add a new checklist item to the [Section Name] section of 
Experion_HMI_FAT_Support_Document_REVISED.md:

Item ID: [XX-YY] (follow numbering sequence)
Description: [Brief description]
Acceptance Criteria: [Specific, measurable criteria]
Reference: [Standard or specification source]

Maintain table formatting consistency with existing items.
```

**For Updating Performance Benchmarks:**
```
Update the performance benchmark for [Metric Name] in 
Experion_HMI_FAT_Support_Document_REVISED.md:

Current Value: [old benchmark]
New Value: [new benchmark]
Source: [Honeywell doc/standard]

Update these locations:
1. Section 2.5 Performance Metrics table
2. Troubleshooting guide optimization targets
3. Document revision history with change note
```

**For Adding Troubleshooting Guidance:**
```
Add a new troubleshooting entry to Section 3.2 of 
Experion_HMI_FAT_Support_Document_REVISED.md:

Symptoms: [Observable issues]
Root Causes: [Technical explanation]
Resolution Steps: [Numbered action items]
Verification: [How to confirm fix]

Base format on existing Issue 1 and Issue 2 structure.
```

---

## Docker Environment (Optional)

The repository includes Docker setup for documentation tooling:

**Files:**
- `Dockerfile` - Container definition
- `docker-compose.yml` - Service orchestration

**Tools Included:**
- markdownlint-cli (markdown linting)
- markdown-pdf (PDF generation)
- Node.js environment

**Usage:**
```powershell
# Build and start
docker-compose up -d

# Access container
docker-compose exec documentation bash

# Generate PDF
markdown-pdf Experion_HMI_FAT_Support_Document_REVISED.md

# Stop container
docker-compose down
```

**Note:** Docker is **optional**. Primary workflow uses standard markdown editors (VS Code, Obsidian, etc.).

---

## Copilot Integration Guide

### Using Experion_HMI_Copilot_Prompts.md

The Copilot prompts document provides ready-to-use validation automation for:

1. **Quick Audits:**
   - Style guide conformance scanning
   - Script performance analysis
   - DOM complexity ranking

2. **Performance Analysis:**
   - Trend configuration auditing
   - Per-graphic metrics aggregation
   - Heat map generation

3. **Integrity Checks:**
   - Point mapping validation
   - RAW/ENG scale verification
   - Safety Manager alignment

4. **Refactoring:**
   - Script optimization
   - CSS standardization
   - Display Builder Assistant remediation

**Example Workflow:**
1. Open project in VS Code
2. Open Copilot Chat (Ctrl+I)
3. Paste prompt from Experion_HMI_Copilot_Prompts.md
4. Review results
5. Log findings in FAT checklist

**Prompt Categories:**
- Quick Audits (3 prompts)
- Trend & Performance (2 prompts)
- Safety Manager Integrity (2 prompts)
- Display Builder Assistant (2 prompts)
- Diagnostics (1 prompt)
- Refactoring (2 prompts)
- CLI One-liners (4 prompts)
- Documentation (1 prompt)

---

## File Dependencies

### Critical Files (DO NOT DELETE)

1. **Experion_HMI_FAT_Support_Document_REVISED.md** - Primary deliverable
2. **AMP-LAR-AUT-SPC-0050 Rev 1 - BPCS HMI Style Guide.pdf** - Standards reference
3. **pmt-hps-hmiweb-display-building-guide-epdoc-xx54-en-520a.pdf** - Technical reference

### Supporting Files (Enhance Understanding)

4. **Display Performance Analysis Report-Steps.pdf** - Testing methodology
5. **display_sizingrev3.pdf** - Sizing standards
6. **Station DCG_Rev3.pdf** - System architecture

### Derivative Files (Can Regenerate)

7. **Experion_HMI_FAT_Support_Document_REVISED.pdf** - Generated from .md
8. **Experion_HMI_Copilot_Prompts.md** - Standalone reference
9. **README.md** - Project overview

### Deprecated Files (Historical Reference Only)

10. **Experion_HMI_FAT_Support.txt** - Original draft
11. **Experion_HMI_FAT_Support_Document_with_Prompts.md** - Intermediate version
12. **Experion_HMI_FAT_Support_Document_with_Prompts.docx** - Word version (outdated)
13. **Checklist.md** - Empty placeholder

---

## Known Limitations & Future Enhancements

### Current Limitations

1. **Platform-Specific:** Document is Experion-only (not applicable to DeltaV, PCS 7, etc.)
2. **Static Benchmarks:** Performance targets may change with new Experion releases
3. **Manual Execution:** Checklists require manual validation (not automated)
4. **Single Project Focus:** Not multi-project tracking system
5. **No Integration:** Standalone document (not integrated with JIRA, SharePoint, etc.)

### Potential Future Enhancements

1. **Automated Validation:**
   - Python script to parse HMIWeb files and check style compliance
   - Automated DOM node counting
   - Script complexity analysis tool

2. **Digital Checklist:**
   - Excel version with automated Pass/Fail tracking
   - Dashboard for progress visualization
   - Integration with project management tools

3. **Multi-Platform Support:**
   - Adapt checklist structure for DeltaV, PCS 7, Centum VP
   - Create platform-agnostic base template
   - Platform-specific supplemental sections

4. **Lessons Learned Repository:**
   - Database of actual FAT issues encountered
   - Common failure patterns
   - Vendor-specific quirks and workarounds

5. **Training Materials:**
   - Video walkthrough of FAT execution
   - Example completed checklists
   - Troubleshooting decision trees

---

## Maintenance Schedule

### Regular Reviews (Every 6 Months)

- [ ] Check for new Experion releases
- [ ] Review Honeywell documentation updates
- [ ] Verify benchmark accuracy
- [ ] Collect field feedback from FAT executions
- [ ] Update troubleshooting guide with new issues

### Major Reviews (Annually)

- [ ] Full document revision for content accuracy
- [ ] Style guide alignment check
- [ ] Benchmark validation against current industry practice
- [ ] Copilot prompt effectiveness review
- [ ] Consider enhancements based on user feedback

### Triggered Updates (As Needed)

- [ ] New Experion release → Update version references
- [ ] Revised AMP-LAR-AUT-SPC-0050 → Update citations
- [ ] New Honeywell guidance → Update benchmarks
- [ ] Critical FAT failure → Update troubleshooting
- [ ] User confusion → Clarify documentation

---

## Success Metrics

### Document Quality Indicators

- **Completeness:** All major validation areas covered (static, dynamic, performance, alarms)
- **Specificity:** Quantitative acceptance criteria (not subjective)
- **Traceability:** Clear references to source standards
- **Usability:** Can be executed by engineer unfamiliar with Experion
- **Professional:** Suitable for client and vendor review

### Usage Indicators

- **Reuse Rate:** Document used on multiple FAT projects without major modifications
- **Issue Detection:** Catches > 80% of graphics issues before site deployment
- **Time Savings:** Reduces FAT execution time by 30%+ vs. ad-hoc validation
- **Acceptance Rate:** Vendor acceptance without disputes over unclear criteria

### Maintenance Indicators

- **Update Frequency:** Document kept current with Experion releases
- **Field Feedback:** Continuous improvement from actual FAT executions
- **AI Agent Success:** Other agents can maintain document with minimal context

---

## Contact & Support

**Document Owner:** Marathon Petroleum Control Systems Engineering

**Primary Use Cases:**
- Factory Acceptance Testing of vendor-supplied HMI graphics
- Internal validation of graphics before deployment
- Training new engineers on Experion HMI standards
- Vendor specification document (what will be tested)

**Related Documentation:**
- AMP-LAR-AUT-SPC-0050 (HMI Style Guide) - Primary standards reference
- Project-specific Alarm Philosophy - Alarm-related criteria
- Experion System Architecture Documents - Context for graphics role

**Support Resources:**
- Honeywell Technical Support (for platform questions)
- Display Builder Assistant (built-in performance tool)
- Internal Control Systems team (for style guide interpretation)

---

## Appendix: Quick Reference

### Critical File Locations

| File                                              | Purpose                    | Location        |
| ------------------------------------------------- | -------------------------- | --------------- |
| Experion_HMI_FAT_Support_Document_REVISED.md     | Primary FAT document       | Graphics/       |
| AMP-LAR-AUT-SPC-0050 Rev 1 - BPCS HMI Style.pdf  | Style guide reference      | Graphics/       |
| pmt-hps-hmiweb-display-building-guide...pdf      | HMIWeb technical reference | Graphics/       |
| Display Performance Analysis Report-Steps.pdf    | Testing methodology        | Graphics/       |
| Experion_HMI_Copilot_Prompts.md                  | AI validation prompts      | Graphics/       |
| HLV Log                                           | Validation errors          | C:\ProgramData\ |

### Key Performance Benchmarks (Quick Reference)

- Display call-up: **< 2s** (simple) / **< 5s** (complex)
- DOM nodes: **< 1500** per graphic
- Script execution: **< 100ms**
- Trend pens: **≤ 8** per display
- Navigation response: **< 500ms**
- Screen density: **< 60%** coverage

### FAT Checklist Section Summary

| Section | Items | Purpose                       |
| ------- | ----- | ----------------------------- |
| SE      | 15    | Static elements & layout      |
| DE      | 15    | Dynamic behavior & data       |
| NU      | 11    | Navigation & usability        |
| AE      | 9     | Alarm & event management      |
| PM      | 10    | Performance metrics           |
| CS      | Var   | Compliance & standards        |

### Document Change Log Format

```markdown
| Version | Date       | Author | Changes                             |
| ------- | ---------- | ------ | ----------------------------------- |
| 1.1     | YYYY-MM-DD | [Name] | Updated R520 → R530 references      |
| 1.2     | YYYY-MM-DD | [Name] | Added new performance benchmark PM-11|
```

---

**END OF HANDOFF DOCUMENT**

*This handoff document is designed to prevent knowledge rot and enable AI agents to maintain, update, and extend the Experion HMI FAT documentation with full context and understanding of design decisions, reference materials, and maintenance workflows.*
