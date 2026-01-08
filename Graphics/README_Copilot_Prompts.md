
# Experion HMI Graphics – FAT Copilot Prompt Cheat‑Sheet (VS Code)

This README provides ready-to-use prompts for **VS Code Copilot Chat** and **Copilot CLI** to support Factory Acceptance Testing (FAT) of **Experion HMI graphics**. Prompts are organized by activity and reference our internal standards and Honeywell guidance.

> **Use guidance**: Paste prompts into Copilot Chat (`Ctrl+I`) or run via Copilot CLI in the terminal. Customize spec/section references as needed.

---

## 1) Quick Audits of Vendor Graphics

### A. Baseline conformance to style guide
```
You are my Experion HMI SME. Scan the workspace for HMIWeb graphics (HTML/HTM, CSS, *.vbs) and report any deviations from our style guide for:
- line thickness/color conventions
- font families/sizes
- alarm iconography and shelving indications
- SafeView layouts and window management
Cite files/lines and propose fixes consistent with AMP-LAR-AUT-SPC-0050 Rev 1.
```

### B. Dynamic behavior and script triggers
```
Identify VBScript blocks and HMIWeb script usage (OnAlarm, OnNormal, OnAcknowledge, OnTimer, OnChange, OnOperChange).
Flag any heavy or synchronous operations in these triggers, estimate call-up impact, and recommend refactoring to reduce display load per R530 scripting guidance.
```

### C. Display call-up time risk hotspots
```
Find graphics with large DOM size, nested groups, or excessive bindings. Rank by risk to display call-up time.
For top 10, suggest specific reductions (e.g., flatten nesting, consolidate shapes, defer non-critical scripts).
```

---

## 2) Trend & Performance Constraints (Station Overload Prevention)

### D. Trending limits & heavy displays
```
Search all trend configurations. For each display: count pens, sampling rates, and the number of concurrent trend widgets.
Compare to our recommended limits and mark offenders. Propose pen consolidation, rate adjustments, or lazy-loading.
```

### E. Automated performance profile
```
Aggregate per-graphic metrics (script count, event triggers, DOM nodes, image resources).
Produce a CSV summary and a heat map indicating likely call-up latency contributors.
```

---

## 3) Safety Manager / Point Mapping Integrity

### F. PLC address congruence checks
```
Parse point bindings to confirm PLC addresses and read-out algorithms match Safety Manager definitions.
Flag mismatches and generate a patch list for Control Builder (addresses, algorithms, scaling).
```

### G. RAW/Engineering scale alignment
```
For all analog points, verify RAW and ENG scale values match Safety Manager standards (e.g., 0–3276 for 0–20 mA).
Report any gaps and the exact file/line to fix.
```

---

## 4) Display Builder Assistant Reports (Vendor FAT Evidence)

### H. Import & interpret performance analysis reports
```
Load all Display Builder Assistant performance reports. Extract highlighted parameters exceeding Honeywell recommended limits.
Create a per-graphic remediation checklist for the vendor with precise steps and expected performance gain.
```

### I. Generate FAT-ready test matrix
```
From the performance and validation findings, generate a Pass/Fail test matrix (columns: Item, Description, Pass/Fail, Notes) suitable for signatures.
Order the steps to mirror on-station execution during FAT.
```

---

## 5) Diagnostics & Message Files Consistency

### J. Verify diagnostic message files on Experion servers
```
Search the repo/deployment artifacts for Experion message file versions.
Compare against site requirements and flag outdated or mismatched diagnostic files.
Provide the exact replacement steps and verification checks.
```

---

## 6) Refactoring & Remediation Prompts

### K. Refactor heavy scripts
```
For each flagged VBScript or JS block, rewrite a lighter, event-driven version that avoids blocking calls, reduces polling, and batches parameter reads.
Include before/after snippets and explain expected latency reduction.
```

### L. Style normalization
```
Generate a unified CSS for standardized colors, line weights, fonts, and alarm visuals per AMP-LAR-AUT-SPC-0050 Rev 1.
Output a diff plan to migrate all graphics to this CSS with minimal disruption.
```

---

## 7) Copilot CLI (Terminal) One‑liners

```
# Summarize graphics performance hotspots
copilot summarize "Scan *.htm *.html *.vbs for heavy event scripts and large DOM nodes; output a ranked list with file paths and reasons."

# Extract trend configurations and pen counts
copilot suggest "Find trend widgets and list pen counts + sampling rates; compare to recommended limits and mark violations."

# Build a FAT test matrix from findings
copilot generate "Create a CSV test matrix with Item, Description, Pass/Fail, Notes from current analysis results suitable for vendor sign-off."

# Create remediation tasks
copilot tasks "For each violation, produce a remediation task with steps, estimate of impact on call-up time, and acceptance criteria."
```

---

## 8) Document & Evidence Generation in VS Code

### M. FAT report assembly
```
Compose a FAT summary document that: (1) lists validated graphics, (2) includes performance metrics, (3) logs issues with system IDs, and (4) appends the signature section.
Use our Word template sections and tables.
```

---

## 9) Prompting Tips (Specific to Our Environment)

- **Ground to internal standards** in every prompt (quote the spec name/section when possible) to align Copilot with constraints.
- **Ask for file/line granularity** so vendor responses are actionable in FAT.
- **Prefer refactors that reduce triggers** (e.g., move logic from `OnTimer` to change-based events) per R530 scripting guidance.
- **Always produce a matrix or CSV**; it mirrors acceptance artifacts in our project docs.

---

### Attribution & References (for internal use)
- AMP-LAR-AUT-SPC-0050 Rev 1 — BPCS HMI Style Guide
- Experion HMI Specification R530 — Scripting & point behavior
- Email: BPCS Loading Design Criteria — Station performance guidance
- FAT matrices and checklists — Project docs

