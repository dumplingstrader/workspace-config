Experion HMI Graphics – FAT Support Document

Project Name: __________________________

Date: _________________________________

Vendor: _______________________________

1. Pre-Test Setup

Confirm project scope and application parameters using the latest Parameter Value report.

Verify all tags and associated functionality are configured in the controller.

Ensure Experion Station and Safety Manager systems are online and synchronized.

2. HMI Graphic Validation Checklist

Static Elements

| Item | Description | Pass/Fail | Notes |
| ---- | ----------- | --------- | ----- |
|      |             |           |       |
|      |             |           |       |
|      |             |           |       |

Dynamic Elements

| Item | Description | Pass/Fail | Notes |
| ---- | ----------- | --------- | ----- |
|      |             |           |       |
|      |             |           |       |
|      |             |           |       |

Performance

| Item | Description | Pass/Fail | Notes |
| ---- | ----------- | --------- | ----- |
|      |             |           |       |
|      |             |           |       |
|      |             |           |       |

Compliance

| Item | Description | Pass/Fail | Notes |
| ---- | ----------- | --------- | ----- |
|      |             |           |       |
|      |             |           |       |
|      |             |           |       |

3. Troubleshooting Guide

Common Issues & Fixes

Issue: Digital/Numeric Points Incorrect

Fix: Check PLC address mapping between Safety Manager and Experion. Correct in Control Builder and download updated configuration.

Issue: Analog Signal Errors

Fix: Verify RAW and engineering scale values match Safety Manager settings. Update scaling parameters in Experion.

Issue: Diagnostic Messages Wrong

Fix: Refresh diagnostic files on Experion server per Honeywell instructions.

Persistent Anomalies

Review Experion Safety Manager Integration Guide for advanced troubleshooting. Escalate to Honeywell support if errors persist after configuration updates.

4. Best Practices

Limit graphics complexity to maintain operator station performance.

Use Honeywell Display Builder Assistant for performance analysis.

Maintain version control for all graphics and configuration files.

5. Deliverables

Completed FAT checklist with Pass/Fail status.

Log of issues and corrective actions taken.

Performance metrics report for all tested graphics.

Signatures

Tester: __________________________ Date: __________

Vendor Representative: _____________ Date: __________

Appendix: VS Code Copilot Prompt Cheat-Sheet

This cheat-sheet provides categorized prompts for VS Code Copilot to assist in Experion HMI FAT analysis and troubleshooting.

Quick Audits of Vendor Graphics

You are my Experion HMI SME. Scan the workspace for HMIWeb graphics (HTML/HTM, CSS, *.vbs) and report any deviations from our style guide for: line thickness/color conventions, font families/sizes, alarm iconography and shelving indications, SafeView layouts and window management. Cite files/lines and propose fixes consistent with AMP-LAR-AUT-SPC-0050 Rev 1.

Identify VBScript blocks and HMIWeb script usage (OnAlarm, OnNormal, OnAcknowledge, OnTimer, OnChange, OnOperChange). Flag any heavy or synchronous operations in these triggers, estimate call-up impact, and recommend refactoring to reduce display load per R530 scripting guidance.

Find graphics with large DOM size, nested groups, or excessive bindings. Rank by risk to display call-up time. For top 10, suggest specific reductions (e.g., flatten nesting, consolidate shapes, defer non-critical scripts).

Trend & Performance Constraints

Search all trend configurations. For each display: count pens, sampling rates, and the number of concurrent trend widgets. Compare to our recommended limits and mark offenders. Propose pen consolidation, rate adjustments, or lazy-loading.

Aggregate per-graphic metrics (script count, event triggers, DOM nodes, image resources). Produce a CSV summary and a heat map indicating likely call-up latency contributors.

Safety Manager / Point Mapping Integrity

Parse point bindings to confirm PLC addresses and read-out algorithms match Safety Manager definitions. Flag mismatches and generate a patch list for Control Builder (addresses, algorithms, scaling).

For all analog points, verify RAW and ENG scale values match Safety Manager standards (e.g., 0–3276 for 0–20 mA). Report any gaps and the exact file/line to fix.

Display Builder Assistant Reports

Load all Display Builder Assistant performance reports. Extract highlighted parameters exceeding Honeywell recommended limits. Create a per-graphic remediation checklist for the vendor with precise steps and expected performance gain.

From the performance and validation findings, generate a Pass/Fail test matrix (columns: Item, Description, Pass/Fail, Notes) suitable for signatures. Order the steps to mirror on-station execution during FAT.

Diagnostics & Message Files Consistency

Search the repo/deployment artifacts for Experion message file versions. Compare against site requirements and flag outdated or mismatched diagnostic files. Provide the exact replacement steps and verification checks.

Refactoring & Remediation Prompts

For each flagged VBScript or JS block, rewrite a lighter, event-driven version that avoids blocking calls, reduces polling, and batches parameter reads. Include before/after snippets and explain expected latency reduction.

Generate a unified CSS for standardized colors, line weights, fonts, and alarm visuals per AMP-LAR-AUT-SPC-0050 Rev 1. Output a diff plan to migrate all graphics to this CSS with minimal disruption.

Copilot CLI One-liners

copilot summarize "Scan *.htm *.html *.vbs for heavy event scripts and large DOM nodes; output a ranked list with file paths and reasons."

copilot suggest "Find trend widgets and list pen counts + sampling rates; compare to recommended limits and mark violations."

copilot generate "Create a CSV test matrix with Item, Description, Pass/Fail, Notes from current analysis results suitable for vendor sign-off."

copilot tasks "For each violation, produce a remediation task with steps, estimate of impact on call-up time, and acceptance criteria."

Document & Evidence Generation

Compose a FAT summary document that: (1) lists validated graphics, (2) includes performance metrics, (3) logs issues with system IDs, and (4) appends the signature section. Use our Word template sections and tables.

Prompting Tips

Ground to internal standards in every prompt (quote the spec name/section when possible) to get Copilot to align with our constraints.

Ask for file/line granularity so vendor responses are actionable in FAT.

Prefer refactors that reduce triggers (e.g., move logic from OnTimer to change-based events) per R530 scripting advice.

Always produce a matrix or CSV; it mirrors acceptance artifacts in our project docs.

* 
* 
* Go to[ ] Page
