# AI Coding Agent Instructions

## Project Overview

This is a technical documentation and training management workspace for industrial control systems (Honeywell Experion, PTC Integrity, SAP functional locations). The primary active component is the **Training Attendance Tracker** system.

## Available Skills

This workspace includes specialized skills for document processing:

- **DOCX** (`.github/skills/docx/`) - Word document creation, editing, tracked changes, and comments
- **XLSX** (`.github/skills/xlsx/`) - Excel spreadsheet operations with formulas, formatting, and data analysis
- **PDF** (`.github/skills/pdf/`) - PDF manipulation, form filling, text/table extraction
- **PPTX** (`.github/skills/pptx/`) - PowerPoint presentation creation and editing

These skills provide comprehensive workflows for working with Office file formats. Refer to each skill's SKILL.md for detailed instructions.

## Available Prompts

Reusable prompt templates are available in `.github/prompts/`:

**Code Quality & Standards:**
- `sql-code-review.prompt.md` - SQL code review guidelines
- `sql-optimization.prompt.md` - SQL query optimization strategies
- `write-coding-standards-from-file.prompt.md` - Extract coding standards from existing code

**Documentation & Learning:**
- `add-educational-comments.prompt.md` - Add explanatory comments to code
- `github-copilot-starter.prompt.md` - Getting started with GitHub Copilot

**Workflow & Meta:**
- `prompt-builder.prompt.md` - Template for creating new prompts
- `remember.prompt.md` - Context retention for long conversations
- `remember-interactive-programming.prompt.md` - Interactive programming workflow
- `model-recommendation.prompt.md` - Guidance on choosing AI models

Reference these prompts when needed: "Use the prompt from .github/prompts/[filename] to..."

## Available Instructions

Specialized instruction files are available in `.github/instructions/` with domain-specific coding standards, best practices, and guidelines:

**AI & Copilot Framework:**
- `agent-skills.instructions.md` - Guidelines for creating GitHub Copilot skills
- `agents.instructions.md` - Custom agent file creation guidelines
- `ai-prompt-engineering-safety-best-practices.instructions.md` - Prompt engineering and responsible AI
- `prompt.instructions.md` - Creating high-quality prompt files
- `tasksync.instructions.md` - TaskSync V4 terminal-based task management protocol

**Code Review & Quality:**
- `code-review-generic.instructions.md` - Comprehensive code review checklist (customizable)
- `performance-optimization.instructions.md` - Performance best practices (all languages/frameworks)

**Python Development:**
- `python.instructions.md` - Python coding conventions and guidelines
- `dataverse-python.instructions.md` - Dataverse SDK basics
- `dataverse-python-sdk.instructions.md` - Official Dataverse SDK quickstart
- `dataverse-python-api-reference.instructions.md` - Complete API reference
- `dataverse-python-authentication-security.instructions.md` - Auth patterns and security
- `dataverse-python-error-handling.instructions.md` - Error handling and troubleshooting
- `dataverse-python-modules.instructions.md` - Module structure and imports
- `dataverse-python-performance-optimization.instructions.md` - Performance tuning
- `dataverse-python-testing-debugging.instructions.md` - Testing strategies
- `dataverse-python-best-practices.instructions.md` - Best practices compilation
- `dataverse-python-advanced-features.instructions.md` - Advanced features
- `dataverse-python-agentic-workflows.instructions.md` - Agentic workflow patterns
- `dataverse-python-file-operations.instructions.md` - File upload/download
- `dataverse-python-pandas-integration.instructions.md` - DataFrame integration
- `dataverse-python-real-world-usecases.instructions.md` - Real-world examples

**Other Languages:**
- `powershell.instructions.md` - PowerShell cmdlet and scripting best practices
- `java.instructions.md` - Java application development guidelines

**DevOps & CI/CD:**
- `github-actions-ci-cd-best-practices.instructions.md` - GitHub Actions workflows

**Frontend & Styling:**
- `html-css-style-color-guide.instructions.md` - HTML/CSS color and styling rules

**Workflow & Documentation:**
- `task-implementation.instructions.md` - Task plans with progressive tracking
- `update-code-from-shorthand.instructions.md` - Shorthand code expansion
- `update-docs-on-code-change.instructions.md` - Auto-update documentation

These instructions are automatically available to GitHub Copilot. When working on specific domains, Copilot will reference the relevant instruction files.

## Model Cost Optimization

This workspace uses cost-optimized AI model selection to minimize premium token usage. See [MODEL_COST_OPTIMIZATION.md](.github/MODEL_COST_OPTIMIZATION.md) for complete details.

### Auto-Selection Strategy

**Default Behavior**: Skills and prompts specify optimal models in frontmatter (`model:` field). GitHub Copilot auto-selection will prefer free models (0x multiplier) unless complexity requires premium models.

**Model Tiers**:
- **Free (0x)**: GPT-4.1, GPT-5 mini - Used for 80% of routine tasks
- **Standard Premium (1x)**: Claude Sonnet 4.5, GPT-5 Codex - Complex code, advanced reasoning
- **Ultra Premium (10x)**: Claude Opus 4.1 - Architecture reviews only (use sparingly)

**Current Configuration**:
- **DOCX/PDF/PPTX**: GPT-4.1 (free) - Simple file operations
- **XLSX**: Claude Sonnet 4.5 (1x) - Complex formulas require accuracy
- **SQL Review**: GPT-5 mini (free) - Pattern-based checks
- **SQL Optimization**: GPT-5 Codex (1x) - Algorithmic tuning
- **Documentation/Comments**: GPT-4.1 (free) - Text additions

**Cost Savings**: Properly configured model selection saves **60-80% on premium tokens** by routing routine tasks to free models while reserving premium capacity for complex work.

**Override When Needed**:
- Force free: "Use GPT-4.1 to review this code"
- Force premium: "Use Claude Sonnet 4.5 for this complex algorithm"
- Auto-select: "Review this code" (model chosen by complexity)

## Architecture

### Training Tracker System (`Training/`)

**Core Script**: `consolidate_training_data.py` - Automated training attendance consolidation
- **Input**: BC-LAR-ENGPRO*.xlsx files (enrollment/assignment exports from LMS)
- **Output**: `Training_Attendance_Tracker.xlsx` with multiple analysis sheets
- **Technology**: Python 3.13+ with pandas, openpyxl

**Key Design Patterns**:
1. **Auto-discovery**: Uses `glob` to find all BC-LAR-ENGPRO*.xlsx files automatically
2. **Data preservation**: Reads existing tracker before regeneration to preserve manual entries
3. **Dual sheet types**: Handles both "View Learning Content Enrollmen" and "View Learning Content Assignmen" sheets
4. **Session detection**: Detects `-\d+` suffix in filenames (e.g., `BC-LAR-ENGPRO008-1`) to track multi-session courses separately

### Data Preservation Strategy (Critical)

The script MUST preserve user-entered data across regenerations:

```python
# Before writing, read existing data
existing_job_duties = {}  # Employee -> Job Duty mapping
df_dcs_existing = None    # DCS Training tab data

if Path(output_file).exists():
    df_existing = pd.read_excel(output_file, sheet_name='Employee-Course Matrix')
    # Build mappings from existing data
    df_dcs_existing = pd.read_excel(output_file, sheet_name='DCS Training')
```

**Preserved Fields**:
- `Job Duty` column in Employee-Course Matrix (38 assignments)
- Entire `DCS Training` tab (manual course entries)

### Employee Consolidation Logic

The Employee-Course Matrix combines employees from multiple sources:

1. LAR training files (BC-LAR-ENGPRO*.xlsx) via pivot table
2. DCS Training tab manual entries (adds new employees not in LAR courses)

```python
# After pivot table creation, add DCS-only employees
dcs_employees = df_dcs_existing['Employee'].dropna().unique()
new_employees = [emp for emp in dcs_employees if emp not in matrix_employees]
# Create empty rows for new employees
```

## Excel Output Structure

**Sheet Order** (intentional):
1. **Employee-Course Matrix** (PRIMARY VIEW) - Pivot table with Job Duty + DCS Training columns
2. Master Data - All enrollment records
3. Employee Training Detail - Per-person summaries
4. Completion Timeline - Chronological data
5. Summary - Statistics positioned before individual course sheets
6. DCS Training - Manual input sheet for DCS courses
7. Individual course sheets (LAR 8901C, LAR ControlLogix, etc.) - Reference rosters

**Formatting Rules**:
- Employee-Course Matrix columns: Employee=20, Job Duty=15, DCS Training=25, Courses=12 (characters)
- Header row height=45 for wrapped text
- DCS Training column uses `\n` for multi-course entries with wrap_text=True
- Status format: `✓ (Mon YYYY)` for completed, `✗ Dropped` for dropped

## Python Environment

**Setup** (required before first run):
```powershell
python -m venv .venv
.venv\Scripts\activate
pip install pandas openpyxl
```

**Run Training Tracker**:
```powershell
C:/Users/GF99/Documentation/.venv/Scripts/python.exe Training\consolidate_training_data.py
```

## Development Workflows

### Adding New Training Files
1. Drop BC-LAR-ENGPRO*.xlsx into `Training/` folder
2. Script auto-discovers on next run (no code changes needed)
3. Multi-session courses: Use `-1`, `-2`, `-3` suffix (e.g., BC-LAR-ENGPRO008-1.xlsx)

### Modifying Preserved Data
When adding fields that users manually edit:
1. Read existing file BEFORE `pd.ExcelWriter()` context
2. Create mapping: `{key: value}` for scalar data or DataFrame for tabular
3. Apply mapping AFTER regenerating core data
4. Confirm in output: "Preserved X existing [field] assignments"

### Sheet Reordering
Use `wb.move_sheet()` after `openpyxl.load_workbook()`:
```python
wb.move_sheet(sheet, offset=target_position - current_position)
```

## Common Pitfalls

1. **File locked**: User must close Excel file before script runs (PermissionError)
2. **Empty DCS Training preservation**: `dropna(how='all')` removes blank rows but preserves empty DataFrame
3. **Session merging**: Without session suffix detection, multi-session courses appear as single column
4. **Column order dependencies**: Insert Job Duty at position 1, DCS Training at position 2 (after Job Duty)

## Other Workspace Areas

- **Graphics/**: Experion HMI FAT documentation (markdown, not active development)
- **SAP/**: Functional location structure documentation
- **Integrity/**: PTC Integrity system documentation
- **Alarm Reporting/**: APO/Dynamo alarm analysis files
- `analyze_excel.py`, `extract_pdf.py`: One-off utility scripts

## File Naming Conventions

- Training files: `BC-LAR-ENGPRO###(-session).xlsx` pattern
- Output: `Training_Attendance_Tracker.xlsx` (singular, underscores)
- Utility scripts: lowercase with underscores (e.g., `consolidate_training_data.py`)

## User Preferences

### Markdown Documentation Formatting

When creating or editing markdown files that are **technical documentation** (reports, analysis, vendor feedback, system documentation), automatically include page breaks for better printing and PDF conversion:

- **Add page breaks** using `<div style="page-break-after: always;"></div>` 
- **Placement**: After major sections (executive summary, site visits, analysis sections, corrective actions, conclusions)
- **Purpose**: Professional formatting for printing or converting to PDF/Word
- **Pattern**: Insert after the `---` horizontal rule and before the next `##` heading

**Example:**
```markdown
---

<div style="page-break-after: always;"></div>

## Next Major Section
```

**When NOT to add page breaks:**
- README files or general project documentation
- Code documentation or API references
- Small documents (< 3 major sections)
- When user explicitly requests no page breaks
