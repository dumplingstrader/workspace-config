# VS Code Copilot Prompt Cheat-Sheet for Experion HMI FAT

This document provides categorized prompts for leveraging GitHub Copilot in VS Code to accelerate Experion HMI FAT analysis, troubleshooting, and documentation tasks.

---

## 1. Quick Audits of Vendor Graphics

### Prompt 1: Style Guide Compliance Scan
```
You are my Experion HMI SME. Scan the workspace for HMIWeb graphics (HTML/HTM, CSS, *.vbs) and report any deviations from our style guide for:
- Line thickness/color conventions
- Font families/sizes
- Alarm iconography and shelving indications
- Window management and navigation patterns

Cite files/lines and propose fixes consistent with AMP-LAR-AUT-SPC-0050 Rev 1.
```

### Prompt 2: Script Performance Analysis
```
Identify VBScript blocks and HMIWeb script usage (OnAlarm, OnNormal, OnAcknowledge, OnTimer, OnChange, OnOperChange). 

Flag any heavy or synchronous operations in these triggers, estimate call-up impact, and recommend refactoring to reduce display load per R520 scripting guidance.
```

### Prompt 3: DOM Complexity & Nesting Analysis
```
Find graphics with large DOM size, nested groups, or excessive bindings. 

Rank by risk to display call-up time. For top 10, suggest specific reductions:
- Flatten nesting
- Consolidate shapes
- Defer non-critical scripts
```

---

## 2. Trend & Performance Constraint Validation

### Prompt 4: Trend Configuration Audit
```
Search all trend configurations. For each display:
- Count pens
- Identify sampling rates
- Note number of concurrent trend widgets

Compare to our recommended limits (≤8 pens, ≥1 sec sampling) and mark offenders. Propose pen consolidation, rate adjustments, or lazy-loading strategies.
```

### Prompt 5: Performance Metrics Aggregation
```
Aggregate per-graphic metrics:
- Script count
- Event triggers
- DOM nodes
- Image resources

Produce a CSV summary and a heat map indicating likely call-up latency contributors.
```

---

## 3. Display Builder Assistant Report Analysis

### Prompt 6: Extract Performance Violations
```
Load all Display Builder Assistant performance reports. 

Extract highlighted parameters exceeding Honeywell recommended limits. Create a per-graphic remediation checklist for the vendor with precise steps and expected performance gain.
```

### Prompt 7: Generate FAT Test Matrix from Reports
```
From the performance and validation findings, generate a Pass/Fail test matrix with columns:
- Item
- Description
- Pass/Fail
- Notes

Order the steps to mirror on-station execution during FAT. Format suitable for signatures.
```

---

## 4. Diagnostics & Message Files Consistency

### Prompt 8: Message File Version Check
```
Search the repo/deployment artifacts for Experion message file versions. 

Compare against site requirements and flag outdated or mismatched diagnostic files. Provide exact replacement steps and verification checks.
```

---

## 5. Refactoring & Remediation Prompts

### Prompt 9: Script Optimization Rewrite
```
For each flagged VBScript or JS block, rewrite a lighter, event-driven version that:
- Avoids blocking calls
- Reduces polling
- Batches parameter reads

Include before/after snippets and explain expected latency reduction.
```

### Prompt 10: Unified CSS Generation
```
Generate a unified CSS for standardized:
- Colors
- Line weights
- Fonts
- Alarm visuals

per AMP-LAR-AUT-SPC-0050 Rev 1. 

Output a diff plan to migrate all graphics to this CSS with minimal disruption.
```

---

## 6. Copilot CLI One-Liners

For quick command-line interactions with Copilot:

```bash
# Scan for heavy event scripts and large DOM nodes
copilot summarize "Scan *.htm *.html *.vbs for heavy event scripts and large DOM nodes; output a ranked list with file paths and reasons."

# Audit trend widgets
copilot suggest "Find trend widgets and list pen counts + sampling rates; compare to recommended limits and mark violations."

# Generate test matrix CSV
copilot generate "Create a CSV test matrix with Item, Description, Pass/Fail, Notes from current analysis results suitable for vendor sign-off."

# Create remediation tasks
copilot tasks "For each violation, produce a remediation task with steps, estimate of impact on call-up time, and acceptance criteria."
```

---

## 7. Document & Evidence Generation

### Prompt 11: Auto-Generate FAT Summary
```
Compose a FAT summary document that:
1. Lists validated graphics (with file paths)
2. Includes performance metrics (call-up time, DOM nodes, script counts)
3. Logs issues with system IDs and severity
4. Appends the signature section

Use our Word template sections and tables format.
```

---

## 8. Prompting Best Practices

✓ **Ground to internal standards:**  
Quote spec name/section (e.g., "AMP-LAR-AUT-SPC-0050 § 3.2") to align Copilot with project constraints

✓ **Request file/line granularity:**  
Ask for specific file paths and line numbers so vendor responses are actionable during FAT

✓ **Prefer refactoring over workarounds:**  
Example: Move logic from OnTimer to change-based events per R520 scripting advice

✓ **Produce structured outputs:**  
Always ask for matrices, CSVs, or tables—mirrors acceptance artifacts in project documentation

✓ **Iterative refinement:**  
Start broad, then narrow focus based on initial results

✓ **Use context from prior analysis:**  
Reference earlier Copilot outputs in follow-up prompts for continuity

---

## 9. Advanced Prompt Templates

### Template 1: Comprehensive Graphics Audit
```
You are my Experion HMI FAT SME. Conduct a comprehensive audit of the graphics package in the workspace:

1. **Style Compliance:**
   - Check against AMP-LAR-AUT-SPC-0050 Rev 1
   - Flag deviations in line thickness, colors, fonts, alarm icons

2. **Performance:**
   - Identify graphics with DOM > 1500 nodes
   - Find scripts with execution time > 100ms
   - List trend displays with > 8 pens

3. **Integration:**
   - Verify controller point bindings
   - Check analog scaling (RAW vs ENG)

4. **Output:**
   - Generate a prioritized remediation list
   - Estimate impact on call-up time for each item
   - Provide before/after code snippets for top 5 issues

Format as a markdown report suitable for vendor review.
```

### Template 2: Point-by-Point Validation
```
For graphic file [FILENAME.htm]:

1. List all data point bindings
2. Cross-reference with controller tag database [DATABASE.csv]
3. Verify:
   - Tag names match
   - PLC addresses correct
   - Data types compatible
   - Scaling parameters identical

Report mismatches in table format with columns:
| Graphic Tag | Expected Controller Tag | Issue | Recommended Fix |
```

### Template 3: Performance Baseline Report
```
Create a performance baseline report for all graphics in workspace:

For each .htm/.html file:
- Count DOM nodes (estimate if source not accessible)
- List event handlers (OnChange, OnTimer, etc.)
- Identify external resources (images, scripts)
- Calculate estimated call-up time based on Honeywell benchmarks

Output as CSV with columns:
Filename, DOM_Nodes, Event_Handlers, Image_Count, Est_CallUp_ms, Severity

Sort by Severity (High > Medium > Low).
```

---

## 10. Troubleshooting-Specific Prompts

### When Points Display Wrong Values:
```
Analyze binding configuration in [FILENAME.htm] for tag [TAGNAME]. 

Compare with expected controller configuration:
- PLC Address: [ADDRESS]
- Algorithm: [ALGORITHM]
- Scaling: RAW [LOW-HIGH], ENG [LOW-HIGH] [UNITS]

Generate corrected HTML binding code and Control Builder parameter update script.
```

### When Display Loads Slowly:
```
Profile [FILENAME.htm] for performance bottlenecks:

1. DOM complexity analysis
2. Script execution cost estimation
3. Resource load time (images, external CSS/JS)
4. Event handler frequency

Rank issues by impact on call-up time and provide optimization roadmap.
```

### When Alarms Don't Display Correctly:
```
Audit alarm integration in [FILENAME.htm]:

1. Check alarm subscription configuration
2. Verify icon/color mappings per AMP-LAR-AUT-SPC-0050 § 4.1
3. Test shelving indicator logic
4. Validate alarm priority and acknowledgment workflows

Document findings with corrected code examples.
```

---

## Quick Reference Summary

| Category | Key Prompts | Use Case |
|----------|-------------|----------|
| **Style Compliance** | Prompt 1 | Initial graphics package review |
| **Performance Analysis** | Prompts 2, 3, 5 | Identify bottlenecks before FAT |
| **Trends** | Prompt 4 | Validate trend configurations |
| **Display Builder** | Prompts 6, 7 | Generate test matrices from reports |
| **Diagnostics** | Prompt 8 | Message file version checks |
| **Script Optimization** | Prompt 9 | Reduce call-up times |
| **CSS Standardization** | Prompt 10 | Enforce style guide compliance |
| **Documentation** | Prompt 11 | Auto-generate FAT summaries |

---

**Document Version:** 1.0  
**Last Updated:** January 7, 2026  
**Compatible with:** Experion R520, VS Code with GitHub Copilot
