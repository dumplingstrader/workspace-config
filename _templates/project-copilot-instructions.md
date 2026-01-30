# Project-Specific Copilot Instructions

> **Purpose**: Project-specific context that adds to (not replaces) global workspace config.
> Keep this minimal—only include what's unique to this project.

## Project Overview

**Name**: [Project Name]  
**Main Entry Point**: `[main_script].py`  
**Primary Output**: `_output/[main_output_file]`  
**Purpose**: [One-sentence description]

## Current Focus

[1-2 sentences about what you're working on right now or what AI should prioritize]

Example:
> Currently refactoring the employee deduplication logic. Focus on preserving manually-entered job duty assignments during data regeneration.

## Project-Specific Rules

[Only include rules unique to THIS project, not general Python or coding standards]

Example:
- Input files must match pattern `BC-LAR-ENGPRO###(-session).xlsx`
- Always preserve the `Job Duty` column when regenerating output
- Use `_scratch/` for all test outputs—never overwrite production file during testing

## Critical Constraints

[Things that will break the project if not followed]

Example:
- Never delete rows from the DCS Training tab
- Employee names must match exactly between input and preserved data (no fuzzy matching)
- Excel file must be closed before script runs (PermissionError otherwise)

## Domain Context

[Any specialized knowledge AI needs for this specific domain]

Example:
- LAR = Learning Activity Record (company training system)
- DCS = Distributed Control System (a type of industrial automation)
- Multi-session courses use `-1`, `-2`, `-3` suffix pattern

## Integration Points

[External systems, APIs, or dependencies specific to this project]

Example:
- Input data comes from HR SharePoint (manual download)
- Output consumed by department heads via Excel (no API)
- Syncs with master employee database nightly (read-only)

## Known Issues

[Current bugs or limitations AI should be aware of]

Example:
- Employees with multiple job duties create duplicate rows (dedup logic in progress)
- Special characters in course names break sheet naming (workaround: sanitize on import)

---

## Notes

This file is **additive**—it supplements global workspace config at `.github/copilot-instructions.md`.

Do not duplicate:
- General Python conventions (already in global config)
- Standard project structure rules (already in global config)
- Universal AI preferences (already in global config)
