# Project Configuration: Documentation Workspace

This file contains all project-specific rules, workflows, and preferences for the Documentation workspace.

## Training Tracker System
- See Training/consolidate_training_data.py for core logic.
- Input: BC-LAR-ENGPRO*.xlsx files (LMS exports)
- Output: Training_Attendance_Tracker.xlsx (multi-sheet analysis)
- Data preservation: Job Duty column and DCS Training tab are preserved across runs.
- Sheet order, formatting, and session handling are enforced as described in the original copilot-instructions.md.

## Python Environment
- Use Python 3.13+ with pandas and openpyxl.
- Setup: python -m venv .venv; .venv\Scripts\activate; pip install pandas openpyxl

## Development Workflows
- Add new training files to Training/ (auto-discovered)
- Multi-session courses: Use -1, -2, -3 suffixes (e.g., BC-LAR-ENGPRO008-1.xlsx)
- Preserve manual data by reading before writing.
- Sheet reordering: Use openpyxl wb.move_sheet().

## File Naming Conventions

### Training System Files
- Training files: BC-LAR-ENGPRO###(-session).xlsx
- Output: Training_Attendance_Tracker.xlsx
- Scripts: lowercase_with_underscores.py

### Markdown Files
When creating markdown files:
- Session handoff → `HANDOFF.md` (overwrite, don't create new)
- Tasks/ideas → append to `_TODO.md`
- Meeting notes → `_scratch/meeting_YYYY-MM-DD.md`
- Temporary analysis → `_scratch/analysis_[topic].md`

### Scripts
When creating scripts:
- Main/production scripts → root level, descriptive name
- Test/debug scripts → `_scratch/test_[what].py`
- Utility scripts → `_scratch/check_[what].py` or `_scratch/debug_[what].py`

## Markdown Documentation Formatting
- For technical docs, add page breaks (<div style="page-break-after: always;"></div>) after major sections for print/PDF.
- Do not add page breaks to README, code docs, or small docs.

## Other Workspace Areas
- Graphics/: Experion HMI FAT docs
- SAP/: Functional location docs
- Integrity/: PTC Integrity docs
- Alarm Reporting/: APO/Dynamo alarm analysis
- Utility scripts: analyze_excel.py, extract_pdf.py

---

For further details, refer to the original copilot-instructions.md (archived).