# Best Practices for AI-Assisted Development Environments

> A practical guide for structuring projects, managing context, and optimizing AI tool usage.

---

## 🎯 Quick Reference: Documentation Standards

**Required Files (every project):**
- `README.md` — What this project does, how to run it
- `HANDOFF.md` — Current state, for continuing in fresh AI sessions
- `_TODO.md` — Tasks, ideas, parking lot

**Folder Conventions:**
- `_scratch/` — Work in progress, experiments, temporary files
- `_archive/` — Old stuff you might need someday (optional)

**The Key Habit:**
Before closing a session: update HANDOFF.md with current state and next steps.
This lets you (or anyone) start a fresh AI conversation and pick up where you left off.

---

## 📋 Document Status & Handoff

**Last Updated:** January 30, 2026
**Status:** Implementation complete — Live in production workspace

### Section Progress

| Section | Status | Notes |
|---------|--------|-------|
| 1. Understanding Your AI Tools | ✅ Complete | "Used X references" explained, config file types, load behavior |
| 2. Auditing Your Current Setup | ✅ Complete | Real case study included |
| 3. Folder Structure Strategy | ✅ Complete | Flat-within-projects principle, workspace vs project structure |
| 4. Context Engineering | ✅ Complete | Token paradox, phantom tools documented |
| 5. Model Selection Strategy | ✅ Complete | Manual transmission insight, cheat sheet |
| 6. Token Optimization | ✅ Complete | Token tax concept, reduction strategies, checklist |
| 7. Hooks & Automation | ✅ Complete + Deployed | cleanup_check.py, bootstrap_core_three.ps1, pre-commit hook, unused imports detection |
| 8. Markdown Standards | ✅ Complete + Deployed | Core Three in 12 projects, file naming conventions, 33 files organized |
| 9. Workflow Patterns | ✅ Complete | Session lifecycle, start/during/end habits, degradation signals |
| 10. MCP & Tool Integration | ✅ Complete | MCP explained, server types, security, audit homework |
| 10.5 Environment Management | ✅ Complete | Shared venv recommendation |
| 10.6 Agents & Autonomous Workflows | ✅ Complete | Agent spectrum, guardrails, patterns |
| 11. Security & Boundaries | ✅ Complete | Work vs. home, secrets management, colleague briefing |
| 12. Git & Multi-Machine Workflow | ✅ Complete | Mental model, sync workflow, error messages explained |
| Appendix | 🟡 Partial | Open questions listed |

### Key Discoveries Made

1. **Model selection is manual** — `model:` frontmatter in skills is ignored by Copilot
2. **Skills add tokens, not save them** — 4 skills × ~2,500 tokens = ~10,000 tokens before you type anything
3. **The "13 references" revealed** — Includes 4+ Dataverse files loading on every interaction (quarterly use!)
4. **Phantom tool references** — `recalc.py` referenced in xlsx skill doesn't exist
5. **Per-project venvs causing confusion** — Recommend shared venv at workspace root
6. **Handoffs are for AI, not humans** — You remember; the AI doesn't (Section 8)
7. **Flat within projects** — Add folders when you hit pain, not before (Section 3)
8. **The token tax** — ~13,000 tokens consumed before typing; explains 2.5-week exhaustion (Section 6)
9. **Instructions auto-load, prompts don't** — Files in `.github/instructions/` always load; prompts wait until invoked (Section 1)
10. **MCP ≠ token cost** — Unlike Copilot refs, MCP servers don't consume tokens when idle (Section 10)
11. **Home git structure is fine** — 5 sibling repos, not nested; confusing messages are from sync issues (Section 12)
12. **Bootstrap automation works** — Created 33 Core Three files across 12 projects in minutes; manual setup would take hours
13. **Unused imports detection valuable** — Found 54 unused imports across workspace; enabled by default, opt-out with --skip-imports
14. **On-demand folders better than pre-creation** — _scratch/_output created automatically when needed; no empty folder clutter

### Artifacts Created

**Automation Tools (Production):**
- `cleanup_check.py` — File organization + unused imports detection (Python, 470 lines)
- `bootstrap_core_three.ps1` — Automated Core Three file creation (PowerShell, 85 lines)
- `.git/hooks/pre-commit` — Automatic cleanup checks before commits
- `.vscode/settings.json` — File watcher exclusions for _scratch/_output/_archive

**Documentation:**
- `ai-dev-guide-outline.md` → `.github/AI_WORKSPACE_GUIDE.md` (**THIS FILE**)
- `.github/project-config.md` — Workspace-specific rules including file naming conventions
- Section 1 (Understanding AI Tools) — "Used X references" explained, config types, auto-load behavior
- Section 3 (Folder Structure) — Workspace/project templates, naming conventions
- Section 6 (Token Optimization) — Token tax concept, reduction strategies, optimization checklist
- Section 8 (Markdown Standards) — Core Three files, _scratch pattern, HANDOFF format
- Section 9 (Workflow Patterns) — Session lifecycle, degradation signals, weekly maintenance
- Section 10 (MCP) — MCP demystified, server types, security considerations, audit homework
- Section 10.6 (Agents) — Agent spectrum, guardrails, Claude CLI patterns, colleague ground rules
- Section 11 (Security & Boundaries) — Work vs. home, secrets patterns, colleague security briefing
- Section 12 (Git & Multi-Machine) — Mental model, push/pull workflow, error messages decoded

### User's Environment

- **Work:** VS Code + GitHub Copilot, local git only, `_Documentation/` parent folder
- **Home:** VS Code + Claude CLI, GitHub remote, 3 machines
- **Pain points:** Token exhaustion (2.5 of 4 weeks), file sprawl, unclear config scope

### Open Homework for User

- [x] ~~Click "13 items" in Copilot to see what's actually loading~~ ✅ Done — Dataverse files confirmed loading
- [ ] Change Copilot dropdown to GPT-4.1 as default
- [ ] Run `cleanup_check.py` on Training/ folder
- [ ] Consolidate to shared venv at `_Documentation/.venv`
- [ ] Add or remove `recalc.py` reference in xlsx skill
- [ ] **NEW:** Move Dataverse files from `.github/instructions/` to `_reference/dataverse/`
- [ ] **NEW:** Run `claude mcp list` to see your 7 connected MCP servers
- [ ] **NEW:** Practice push-before-leave, pull-when-arrive git workflow

### Implementation Results (January 30, 2026)

**✅ Completed:**
1. ✅ Moved Dataverse files from `.github/instructions/` to `_reference/dataverse/`
2. ✅ Slimmed `copilot-instructions.md` from 800+ lines to 28 lines (96% reduction)
3. ✅ Moved 3 rarely-used skills to `_reference/` (saved ~7,500 tokens/session)
4. ✅ Created `bootstrap_core_three.ps1` and deployed Core Three to 12 projects
5. ✅ Enhanced `cleanup_check.py` with unused imports detection (AST-based)
6. ✅ Organized 33 files across workspace using cleanup_check.py
7. ✅ Established file naming conventions in project-config.md
8. ✅ Consolidated SAP/PROJECT_HANDOFF.md into standard HANDOFF.md pattern
9. ✅ Created pre-commit git hook for automatic cleanup checks
10. ✅ Added VS Code file watcher exclusions for performance

**Metrics:**
- **Token savings:** ~7,500 tokens/session (75% reduction in skill overhead)
- **Projects standardized:** 12 (8 main + 4 Alarm Reporting subprojects)
- **Files organized:** 33 (moved to _scratch/_output/)
- **Unused imports found:** 54 across 12 Python files
- **Time saved:** Core Three setup automated from ~2 hours to 2 minutes

**Still TODO:**
- [ ] Run `claude mcp list` to audit MCP servers (home setup)
- [ ] Change Copilot dropdown to GPT-4.1 as default model
4. [ ] Verify Copilot "Used X references" decreases after cleanup
5. [ ] Practice git workflow: push before leaving, pull when arriving
6. [ ] Test token budget improvement over next week
7. [ ] Share guide with Process Controls colleagues for feedback

---

## About This Guide

**Author's Context:**
- Work: VS Code + GitHub Copilot (local repository only)
- Home: VS Code + Claude CLI (GitHub remote, 3 machines)
- Primary work: Documentation-heavy projects
- Current pain: Token exhaustion, file sprawl, unclear config scope

---

## Table of Contents

1. [Understanding Your AI Tools](#1-understanding-your-ai-tools)
2. [Auditing Your Current Setup](#2-auditing-your-current-setup) ⭐ NEW
3. [Folder Structure Strategy](#3-folder-structure-strategy)
4. [Context Engineering](#4-context-engineering)
5. [Model Selection Strategy](#5-model-selection-strategy)
6. [Token Optimization](#6-token-optimization)
7. [Hooks & Automation](#7-hooks--automation)
8. [Markdown & Documentation Standards](#8-markdown--documentation-standards)
9. [Workflow Patterns](#9-workflow-patterns)
10. [MCP & Tool Integration](#10-mcp--tool-integration)
10.5. [Environment Management (Python)](#105-environment-management-python)
10.6. [Agents & Autonomous Workflows](#106-agents--autonomous-workflows) ⭐ NEW
11. [Security & Boundaries](#11-security--boundaries)
12. [Git & Multi-Machine Workflow](#12-git--multi-machine-workflow) ⭐ NEW
12. [Appendix: Open Questions & Research](#appendix-open-questions--research)

---

## 1. Understanding Your AI Tools

**Goal:** Know exactly what each config file does and when it loads.

### The "Used X References" Indicator (Copilot)

When Copilot shows "Used 13 references," those are files loaded into context for that interaction. Every reference consumes tokens.

**Your actual 13 references (from screenshot):**
```
1. copilot-instructions.md          ← Main instructions (expected)
2. code-review-generic.instructions.md
3. dataverse-python-api-reference.instructions.md
4. dataverse-python-authentication-secu...
5. dataverse-python-error-handling.instructions.md
6. dataverse-python-modules.instructions.md
7-13. [Additional files not visible in screenshot]
```

**The problem:** At least 4-5 Dataverse instruction files load on *every* interaction, even though Dataverse work happens once a quarter. This is your token tax.

### GitHub Copilot Configuration Files

Copilot uses three types of configuration, each with different purposes:

| Type | File Pattern | Purpose | Loads When? |
|------|--------------|---------|-------------|
| **Instructions** | `*.instructions.md` | Coding guidelines, context | Automatically (if in `.github/instructions/`) |
| **Prompts** | `*.prompt.md` | Reusable prompt templates | On-demand (you invoke them) |
| **Skills** | `skill-name/` folder with files | Complex multi-step capabilities | Varies (may auto-load) |

**Instructions (.instructions.md):**
- Live in `.github/instructions/` folder
- Provide context about coding standards, project specifics, conventions
- **Load automatically** when present in the instructions folder
- This is why your Dataverse files are loading—they're in the auto-load location

**The main instructions file:**
- `.github/copilot-instructions.md` — Always loads for the repo
- This is your 800+ line file that needs slimming (Section 6)

**Prompts (.prompt.md):**
- Live in `.github/prompts/` folder
- Templates you invoke explicitly (e.g., "use the code-review prompt")
- **Do NOT auto-load** — they wait until called
- Safe to have many; they don't cost tokens until used

**Skills (folders):**
- Live in `.github/skills/` folder
- Each skill is a folder containing instructions + potentially scripts
- Loading behavior is less clear—may auto-load based on context
- Your xlsx, docx, pdf, pptx skills likely load when working with those file types

### How Files Get Into "References"

Based on observation, Copilot loads references from:

1. **Always loaded:**
   - `.github/copilot-instructions.md` (main instructions)
   - Files in `.github/instructions/` folder (all of them, apparently)

2. **Contextually loaded:**
   - Skills relevant to current file type
   - Files you have open in editor
   - Files explicitly referenced in instructions

3. **On-demand only:**
   - Prompts (`.prompt.md` files)
   - Files in other folders not in the load path

**The key insight:** Putting a file in `.github/instructions/` means it loads *every time*. That's why moving rarely-used instructions elsewhere (like `_reference/`) saves tokens.

### Controlling What Loads

**To reduce auto-loaded references:**

1. **Move rarely-used instructions out of `.github/instructions/`**
   ```
   # Before (all load automatically)
   .github/
   └── instructions/
       ├── python.instructions.md      ← Use daily
       ├── dataverse-*.md (16 files)   ← Use quarterly
   
   # After (only daily-use loads)
   .github/
   └── instructions/
       ├── python.instructions.md      ← Loads automatically
   
   _reference/
   └── dataverse/
       ├── dataverse-*.md (16 files)   ← Dormant until needed
   ```

2. **Slim the main instructions file**
   - Current: 800+ lines (~6,000+ tokens)
   - Target: <50 lines (~500 tokens)
   - Move project-specific content to project-level config

3. **Use prompts instead of instructions for occasional tasks**
   - Instructions = always loaded
   - Prompts = loaded when invoked
   - If you only need something sometimes, make it a prompt

**To load something on-demand:**
```
"Use the dataverse instructions from _reference/dataverse/ for this task"
```
Copilot can read files when asked—you don't need them pre-loaded.

### Claude CLI Configuration (Home Setup)

Claude CLI uses a different structure:

```
project/
├── .claude/
│   └── settings.json     ← Project-level settings
├── CLAUDE.md             ← Project instructions (like copilot-instructions.md)
└── ...
```

**CLAUDE.md:**
- Equivalent to `copilot-instructions.md`
- Lives at project root (not in a subfolder)
- Loads automatically for that project
- Same token considerations apply—keep it lean

**Scope hierarchy:**
```
~/.claude/settings.json          ← Global (all projects)
    ↓ overridden by
project/.claude/settings.json    ← Project-specific
    ↓ augmented by
project/CLAUDE.md                ← Project instructions
```

**Key differences from Copilot:**

| Aspect | Copilot | Claude CLI |
|--------|---------|------------|
| Main instructions | `.github/copilot-instructions.md` | `CLAUDE.md` at root |
| Auto-load folder | `.github/instructions/` | None (explicit only) |
| Skills location | `.github/skills/` | Not applicable (different model) |
| Ignore patterns | No `.copilotignore` | `.claude/settings.json` ignore array |

### The Scope Hierarchy

Both tools follow a hierarchy where more specific config adds to (or overrides) more general config:

```
┌─────────────────────────────────────────────────────────┐
│ User/Global Settings                                     │
│ (VS Code settings, ~/.claude/)                          │
├─────────────────────────────────────────────────────────┤
│ Workspace Root                                           │
│ (_Documentation/.github/, _Documentation/CLAUDE.md)     │
├─────────────────────────────────────────────────────────┤
│ Project Folder                                           │
│ (Training/.github/, Training/CLAUDE.md)                 │
└─────────────────────────────────────────────────────────┘
        ↑ More specific = higher priority
```

**Important:** In Copilot, project-level instructions are *additive*—they don't replace workspace-level, they add to it. So if workspace loads 13 references, project-level only adds more.

This is why fixing the workspace root config matters most—everything inherits from it.

### Quick Reference: File Types and Behavior

| File/Folder | Location | Auto-loads? | Token cost |
|-------------|----------|-------------|------------|
| `copilot-instructions.md` | `.github/` | ✅ Always | High (your main file) |
| `*.instructions.md` | `.github/instructions/` | ✅ Always | High (all files load!) |
| `*.prompt.md` | `.github/prompts/` | ❌ On-demand | Zero until used |
| `skill-name/` | `.github/skills/` | ⚠️ Contextual | Varies |
| `CLAUDE.md` | Project root | ✅ Always | High |
| Files in `_reference/` | Anywhere outside `.github/` | ❌ On-demand | Zero until requested |

### Your Action Items

Based on the "13 references" screenshot:

- [ ] **Immediate:** Move Dataverse instruction files from `.github/instructions/` to `_reference/dataverse/`
- [ ] **Immediate:** Check what else is in `.github/instructions/` — move anything not used daily
- [ ] **This week:** Slim `copilot-instructions.md` to <50 lines (Section 6 guidance)
- [ ] **Verify:** After changes, check if "Used X references" decreases

**Expected result:** Reducing from 13 references to 3-5 should noticeably extend your token budget.

### Questions Answered

| Question | Answer |
|----------|--------|
| What exactly are the 13 items Copilot shows? | Files loaded into context: main instructions + everything in `.github/instructions/` + contextual skills. Your Dataverse files are in there. |
| How do you activate/deactivate specific instructions? | Move out of `.github/instructions/` to deactivate auto-load. Reference on-demand when needed. |
| Can you have project-specific overrides? | Yes—create `ProjectName/.github/copilot-instructions.md`. But it's additive, not replacement. Fix workspace root first. |

---

## 2. Auditing Your Current Setup

**Goal:** Understand what's actually loading and identify waste before restructuring.

> ⭐ This section uses a real-world case study from the author's work environment.

### Case Study: The "Awesome Copilot" Trap

**Situation:** Downloaded comprehensive resources from awesome-copilot GitHub repo. Placed everything at root level. Result: bloated context on every interaction.

**Discovered Structure:**
```
_Documentation/                        ← Root (all projects inherit)
├── .github/
│   ├── copilot-instructions.md       ← 800+ line file with everything
│   │
│   ├── instructions/                 ← 30+ downloaded instruction files
│   │   ├── python.instructions.md
│   │   ├── java.instructions.md           ← Never used
│   │   ├── dataverse-python-*.md (16 files) ← Rarely used
│   │   ├── powershell.instructions.md
│   │   └── ... many more
│   │
│   ├── prompts/                      ← 10+ prompt templates
│   │   ├── sql-code-review.prompt.md
│   │   ├── remember.prompt.md
│   │   └── ... more
│   │
│   └── skills/                       ← 4 skill folders
│       ├── docx/
│       ├── xlsx/
│       ├── pdf/
│       └── pptx/
│
├── Training/                         ← Active project (pays full context tax)
├── Graphics/                         ← Inactive (still pays full tax)
├── SAP/                              ← Inactive (still pays full tax)
└── Integrity/                        ← Inactive (still pays full tax)
```

**Symptoms:**
- "13 items" indicator on every Copilot interaction
- Token budget exhausted in 2.5 weeks (of 4-week cycle)
- Slow initial responses (loading time)
- Irrelevant suggestions (Java hints in Python project)

### The Audit Process

**Step 1: Inventory what exists**
```
Count files by type:
- Instructions: ___ files
- Prompts: ___ files  
- Skills: ___ folders
- Total estimated tokens: ___
```

**Step 2: Categorize by actual usage**

| Category | Files | Action |
|----------|-------|--------|
| Use daily | ??? | Keep at root |
| Use weekly | ??? | Keep at root or project level |
| Use monthly | ??? | Move to project level, load on-demand |
| Never used | ??? | Archive or delete |

**Step 3: Identify the "always loaded" items**

Copilot loads these automatically:
- `.github/copilot-instructions.md` (if exists)
- Files referenced in instructions
- Skills marked as active (how? TBD)

**Step 4: Measure the cost**

Questions to answer:
- [ ] What is the token count of `copilot-instructions.md`?
- [ ] Which instruction files are being loaded automatically?
- [ ] Can you see per-session token usage breakdown?

### Common Audit Findings

**The Catalog Problem:**
Your instructions file lists every available resource—but listing them may cause them to load. 

❌ **Anti-pattern:**
```markdown
## Available Instructions
- `python.instructions.md` - Python coding conventions
- `java.instructions.md` - Java guidelines
- `dataverse-python-*.md` - 16 Dataverse files
```

✅ **Better pattern:**
```markdown
## Active Instructions (always loaded)
- `python.instructions.md` - Our primary language

## Available on Request (not auto-loaded)
See `.github/instructions/README.md` for full catalog
```

**The Project Bleed Problem:**
Project-specific content (Training Tracker architecture) in global config means every project loads it.

❌ **Anti-pattern:** Training Tracker code examples in root `copilot-instructions.md`

✅ **Better pattern:** Training Tracker details in `Training/.github/copilot-instructions.md`

**The "Just In Case" Problem:**
Downloaded resources that *might* be useful someday, but cost tokens today.

❌ **Anti-pattern:** 16 Dataverse instruction files when Dataverse work happens once a quarter

✅ **Better pattern:** Dataverse files in `_reference/dataverse/` folder, copied to project when needed

### Restructuring Strategies

**Option A: Minimal Root + Rich Projects**
```
_Documentation/
├── .github/
│   ├── copilot-instructions.md    ← Tiny: just universal rules
│   └── skills/                    ← Keep, these are lightweight
│
├── _templates/                    ← Downloadable resources stored here
│   ├── instructions/
│   └── prompts/
│
└── Training/
    └── .github/
        ├── copilot-instructions.md  ← Project-specific context
        └── instructions/            ← Only what this project needs
```

**Option B: Workspace Root + Activation System**
```
_Documentation/
├── .github/
│   ├── copilot-instructions.md    ← Index with activation syntax
│   ├── instructions/
│   │   ├── _active/               ← Symlinks or copies of what's loaded
│   │   └── _available/            ← Everything else
```

**Option C: Keep Structure, Slim the Instructions File**
- Don't move files
- Drastically reduce `copilot-instructions.md` to essentials only
- Stop cataloging available files (Copilot can find them when asked)

### Your Audit Homework

Before restructuring, gather data:

1. [ ] Click on Copilot's "13 items" — what exactly is listed?
2. [ ] Count: How many instruction files exist in `.github/instructions/`?
3. [ ] Estimate: Of those, how many have you used in the past month?
4. [ ] Test: Comment out sections of `copilot-instructions.md` — does "13 items" decrease?
5. [ ] Measure: Does response time improve with a slimmer config?

---

## 3. Folder Structure Strategy

**Goal:** Consistent, predictable structure that scales—without creating a maze you can't navigate.

### The Core Tension

**Too flat:** Everything at project root → sprawl, can't find things  
**Too deep:** Nested folders for everything → hunting, "where did I put that?"

**The sweet spot:** Flat within projects, with only 2-3 designated zones for specific purposes.

### Guiding Principles

1. **You should be able to guess where something is.** If you have to search, the structure failed.

2. **Folders are for *categories*, not *stages*.** Don't create folders like `v1/`, `v2/`, `final/`, `final-final/`. Use `_archive/` for old stuff, root for current.

3. **Prefixes signal purpose:**
   - `_underscore` = internal/meta (sorts to top, signals "system folder")
   - No prefix = project content

4. **AI config lives at the level it applies to.** Global rules at workspace root. Project-specific rules in project folder.

5. **When in doubt, stay flat.** You can always add structure later. Removing structure is harder.

### Workspace-Level Structure

Your `_Documentation/` folder is the workspace root. Here's what belongs here:

```
_Documentation/                      ← Workspace root
│
├── .venv/                          ← Shared Python environment (Section 10.5)
├── requirements.txt                ← Shared dependencies
│
├── .github/                        ← Global Copilot config
│   ├── copilot-instructions.md    ← Universal rules only (keep small!)
│   └── skills/                    ← Shared skills (if any)
│
├── .claude/                        ← Global Claude config (if using Claude CLI)
│
├── _templates/                     ← Starter files for new projects
│   ├── project-readme.md
│   └── project-handoff.md
│
├── _reference/                     ← Resources you might need someday
│   ├── dataverse-instructions/    ← Quarterly Dataverse work
│   └── archived-skills/           ← Skills you removed but might restore
│
├── Training/                       ← Active project
├── Graphics/                       ← Active project
├── SAP/                           ← Active project
└── Integrity/                      ← Active project
```

**What's at workspace level:**
- Shared environment (`.venv/`, `requirements.txt`)
- Global AI config (`.github/`, `.claude/`)
- Templates for new projects (`_templates/`)
- Reference materials not tied to one project (`_reference/`)
- Project folders

**What's NOT at workspace level:**
- Project-specific files (those go in their project folder)
- Work in progress (use `_scratch/` inside projects)
- Output files (each project manages its own outputs)

### Project-Level Structure (The Template)

Every project gets this structure. Memorize it once, use it everywhere.

```
Training/                           ← Project root
│
├── README.md                      ← What this is, how to use it (for humans)
├── HANDOFF.md                     ← Current state (for AI)
├── _TODO.md                       ← Tasks, ideas, parking lot
│
├── .github/                       ← Project-specific Copilot config (optional)
│   └── copilot-instructions.md   ← Overrides/additions to global config
│
├── [main script or entry point]   ← e.g., create_training_tracker.py
├── [other production files]       ← Config files, data files
│
├── _scratch/                      ← Work in progress, experiments
│   ├── test_merge.py
│   └── debug_output.xlsx
│
├── _output/                       ← Generated deliverables (optional)
│   └── training_tracker.xlsx
│
└── _archive/                      ← Old versions, abandoned approaches (optional)
    └── 2024-q4-approach/
```

**The three tiers:**

| Tier | Location | What goes here |
|------|----------|----------------|
| **Root** | Project folder | Production files, the Core Three markdown files |
| **_scratch/** | Subfolder | Experiments, tests, work in progress |
| **_archive/** | Subfolder | Old stuff you might need, superseded versions |

**Why only these subfolders?**

You might think you need `inputs/`, `outputs/`, `documents/`, `scripts/`, etc. Usually you don't.

- **inputs/** → Just put input files at root. If you have many, then add the folder.
- **outputs/** → `_output/` only if you're generating files. Many projects don't need it.
- **documents/** → If it's reference material, it's probably in your working files already.
- **scripts/** → If you have one script, it lives at root. Multiple related scripts? Still probably root.

**Add folders when you hit pain, not before.**

### The "Do I Need a Folder?" Test

Before creating a subfolder, ask:

1. **Do I have 5+ files of this type?** No → Keep at root.
2. **Will I look for files by this category?** No → Keep at root.
3. **Does the folder name answer "where would X be?"** No → Rethink the name.

**Example decisions:**

| Situation | Decision |
|-----------|----------|
| 2 Python scripts | Root level |
| 8 Python scripts | Maybe `scripts/`, or split into separate projects |
| 3 input CSVs | Root level |
| 15 input CSVs | `_input/` folder |
| Test scripts for debugging | `_scratch/` (they're temporary) |
| Old version of main script | `_archive/` |

### Naming Conventions

**Folders:**
- Lowercase with hyphens: `training-tracker/`, `employee-data/`
- Underscore prefix for system folders: `_scratch/`, `_archive/`, `_output/`
- No spaces, no special characters

**Files:**
- Scripts: `verb_noun.py` (e.g., `create_training_tracker.py`, `extract_course_names.py`)
- Data: descriptive name (e.g., `job_duties.csv`, `employee_list.xlsx`)
- Markdown: Standard names from Section 8 (`README.md`, `HANDOFF.md`, `_TODO.md`)

**What to avoid:**
- ❌ `final.py`, `final_v2.py`, `final_v2_fixed.py` → Use `_archive/` for old versions
- ❌ `test.py`, `test2.py`, `test3.py` → Use `_scratch/test_[what].py`
- ❌ `New folder/`, `Copy of X/` → Name it properly or delete it

### AI Config Placement

**The rule:** Config at the level it applies to.

| Scope | Location | Contains |
|-------|----------|----------|
| All projects | `_Documentation/.github/copilot-instructions.md` | Universal rules, Python environment info, your preferences |
| One project | `Training/.github/copilot-instructions.md` | Project context, specific constraints, current focus |

**What goes in global config:**
```markdown
## Universal Rules
- Python environment at workspace root: `_Documentation/.venv`
- Pre-installed: pandas, openpyxl, python-pptx, python-docx, PyPDF2
- No pip install commands in scripts

## Conventions
- Experiments go in `_scratch/`
- Update HANDOFF.md with current state
```

**What goes in project config:**
```markdown
## Project: Training Tracker
- Main script: `create_training_tracker.py`
- Output: `_output/training_tracker.xlsx`
- Input data comes from HR SharePoint (manually downloaded)

## Current Focus
Deduplication logic for employees with multiple job duties.
```

**Does project config override global?** 
In Copilot: Project-level instructions are *additive*—they don't replace global, they add to it. Put project-specific context here, not repeated global rules.

### Navigating Multiple Machines (Home Setup)

You mentioned syncing across 3 machines at home. Key considerations:

**What syncs via GitHub:**
- Code (scripts, configs)
- Markdown files
- `.github/` folder (AI config)

**What doesn't sync (and shouldn't):**
- `.venv/` (recreate per machine from `requirements.txt`)
- `_output/` contents (generated files)
- Large data files (use `.gitignore`)

**Folder structure stays identical across machines.** The structure IS the sync strategy—same folders, same conventions, same locations.

**`.gitignore` at workspace root:**
```
.venv/
_output/
_scratch/
*.xlsx
*.csv
__pycache__/
```

Adjust based on what you actually want to sync. Some projects might want `_output/` tracked; others won't.

### Starting a New Project (The 2-Minute Setup)

1. **Create the folder:**
   ```
   _Documentation/
   └── NewProject/
   ```

2. **Add the Core Three:**
   ```
   NewProject/
   ├── README.md      ← "# NewProject\n\nPurpose: [one sentence]"
   ├── HANDOFF.md     ← "# HANDOFF — NewProject\n\n> Just started."
   └── _TODO.md       ← Empty or first task
   ```

3. **Add _scratch/:**
   ```
   NewProject/
   └── _scratch/      ← Create it now, even if empty
   ```

4. **Start working.** Add other folders only when needed.

**Optional:** Create once, reuse forever:
```
_Documentation/
└── _templates/
    ├── README-template.md
    ├── HANDOFF-template.md
    └── new-project-checklist.md
```

### When Structure Fails: Recovery Patterns

**Symptom:** Can't find a file you know exists.  
**Fix:** Your structure is too deep or names are too vague. Flatten and rename.

**Symptom:** Project root has 20+ files.  
**Fix:** Time to add `_scratch/` and `_archive/` if missing, or split into multiple projects.

**Symptom:** Same file exists in multiple places.  
**Fix:** Pick one source of truth. Delete or archive duplicates.

**Symptom:** Folder named `old/` or `backup/` with unclear contents.  
**Fix:** Rename to `_archive/[description]/` or delete if you can't identify why it exists.

### Questions Answered

| Question | Answer |
|----------|--------|
| Does .github at parent level apply to all child projects? | Yes—Copilot reads parent `.github/` config. Project-level adds to it, doesn't replace. |
| Best practice for _scratch cleanup? | Manual weekly review (Section 9). The `cleanup_check.py` from Section 7 can help identify stale files. |
| Should AI config be at parent level, project level, or both? | Both. Global config for universal rules; project config for project context. Keep global small. |

---

## 4. Context Engineering

**Goal:** Give AI exactly what it needs—no more, no less.

### ⚠️ The Skills Token Paradox

> **The Myth:** Adding skills pre-explains things, so the AI doesn't waste tokens figuring them out. More skills = more efficiency.
>
> **The Reality:** Every skill file loads into context and consumes tokens. A 200-line skill = ~2,500 tokens. Four skills = ~10,000 tokens consumed before you even ask a question.
>
> **The Math:**
> ```
> Your current setup (estimated):
>   copilot-instructions.md     ~3,000 tokens
>   xlsx skill                  ~2,500 tokens
>   docx skill                  ~2,500 tokens
>   pdf skill                   ~2,500 tokens
>   pptx skill                  ~2,500 tokens
>   ─────────────────────────────────────────
>   TOTAL                       ~13,000 tokens (before you type anything)
> ```

**When skills ADD value:**
- Complex domain-specific workflows the AI wouldn't know
- Strict formatting requirements (like your financial model color coding)
- Integration with custom tools that actually exist

**When skills WASTE tokens:**
- Teaching the AI things it already knows (pandas, openpyxl basics)
- Referencing tools that don't exist (phantom `recalc.py`)
- Loading for every session when only needed occasionally

**The fix:** Audit your skills. Keep domain-specific rules, remove generic coding tutorials.

### ⚠️ Phantom Tool References

A skill that references a tool that doesn't exist creates problems:

**Example from xlsx skill:**
```markdown
5. **Recalculate formulas (MANDATORY)**: Use the recalc.py script
   python recalc.py output.xlsx
```

**But `recalc.py` doesn't exist in the skill folder.**

**What happens:**
- AI follows instructions literally → Code fails with "file not found"
- AI improvises → Creates `recalc.py` on the fly (wasting tokens, inconsistent results)
- AI skips the step → Formulas not recalculated, broken output

**The fix:** Every tool referenced in a skill must either:
1. Exist in the skill folder (and be documented)
2. Be a standard system tool (python, pip, git)
3. Be removed from the skill

**Audit question:** For each tool/script mentioned in your skills, does it actually exist?

### Topics to Cover

- **Instructions files**
  - What to put in `copilot-instructions.md`
  - What to put in `CLAUDE.md`
  - Writing effective, concise instructions

- **Skills**
  - What is a skill? (A reusable bundle of knowledge/instructions)
  - Where skills live
  - How to activate skills per-project vs. globally
  - Creating your own skills

- **Reference documents**
  - When to point AI at external docs
  - How to structure docs for AI consumption
  - Keeping reference docs current

- **Context scoping**
  - Including only relevant files
  - Excluding noise (logs, generated files, node_modules)
  - .gitignore vs. AI-specific ignore patterns

### Your Current State
- Skills downloaded but parked "waiting"
- No activation strategy
- Unclear global vs. project scope

### Questions to Answer
- [ ] How to audit which skills are actually being used?
- [ ] Can skills be turned on/off per conversation or session?
- [ ] What's the optimal size/scope for a skill file?

---

## 5. Model Selection Strategy

**Goal:** Use expensive models only when they provide value.

### ⚠️ Critical Misconception: "I Thought It Was Automatic"

> **The Myth:** Many engineers (including this guide's author) assume that AI tools automatically route tasks to appropriate models based on complexity, configuration files, or frontmatter metadata.
>
> **The Reality:** In GitHub Copilot (as of January 2026), model selection is **entirely manual**. The dropdown selector in the chat panel is the only control. Your `model:` frontmatter, your optimization configs, your careful documentation—none of it influences which model Copilot actually uses.
>
> **The Cost:** If you set the dropdown to Claude Opus 4.5 and leave it there, you'll burn premium tokens on every single interaction, including trivial tasks that a free model could handle.

**How to verify this:** 
1. Set your dropdown to GPT-4.1 (cheap)
2. Invoke a skill that has `model: Claude Sonnet 4.5` in its frontmatter
3. Check what model actually responds—it will be GPT-4.1

**The fix:** Treat model selection like a manual gear shift. Default to the cheapest model. Escalate manually when you hit limitations.

### The Manual Transmission Approach

Since auto-routing doesn't exist, build manual habits:

**Session Start Ritual:**
1. Open Copilot chat
2. Check the dropdown → Set to GPT-4.1 (cheapest)
3. Work normally
4. Only upgrade when the model fails you

**Escalation Triggers:**
- GPT-4.1 gives wrong/shallow answers → Try Sonnet
- Sonnet struggles with complexity → Try Opus
- Task complete → **Downgrade back to GPT-4.1**

**The Key Discipline:** Always downshift after completing a complex task. Never leave it in Opus.

### Topics to Cover

- **Model tiers (Copilot example)**
  - Opus 4.5 — deep reasoning, architecture, complex refactoring (expensive)
  - Sonnet — general coding, explanations, writing (balanced)
  - Haiku/faster models — autocomplete, simple edits, boilerplate (cheap)

- **Task-to-model mapping**
  | Task Type | Recommended Model | Rationale |
  |-----------|------------------|-----------|
  | Architecture decisions | Opus | Needs broad reasoning |
  | Writing new functions | Sonnet | Good enough, saves tokens |
  | Debugging with context | Sonnet/Opus | Depends on complexity |
  | Autocomplete | Haiku | Speed over depth |
  | Documentation | Sonnet | Quality writing, cheaper |
  | Code review | Sonnet | Pattern matching |
  | Complex refactoring | Opus | Needs to hold large context |

- **Budget awareness**
  - Tracking token usage
  - Recognizing when you're burning tokens
  - Mid-cycle adjustments

### Your Current State
- Opus 4.5 as default (**was left in dropdown, never switched**)
- Token budget exhausted in 2.5 of 4 weeks (**because everything used Opus**)
- No task-based model switching strategy (**thought it was automatic**)
- `model:` frontmatter in skills (**does nothing—just documentation**)
- `MODEL_COST_OPTIMIZATION.md` (**useful reference, but AI ignores it**)

### Quick Reference Cheat Sheet (Keep Visible)

Post this near your monitor or in a pinned note:

```
┌─────────────────────────────────────────────────────────────┐
│  COPILOT MODEL SELECTION - CHECK THE DROPDOWN!              │
├─────────────────────────────────────────────────────────────┤
│  DEFAULT (start here):                                      │
│    → GPT-4.1 (free/0.33X)                                   │
│                                                             │
│  UPGRADE when stuck:                                        │
│    → Sonnet 4 (1X) - complex code, debugging                │
│    → Opus 4.5 (3X) - architecture only, then DOWNGRADE      │
│                                                             │
│  ALWAYS DOWNGRADE after complex task!                       │
└─────────────────────────────────────────────────────────────┘
```

### Questions to Answer
- [ ] Does Copilot allow per-task model selection?
- [ ] Can you set a default to Sonnet and escalate to Opus manually?
- [ ] How to track which tasks consumed the most tokens?

---

## 6. Token Optimization

**Goal:** Reduce waste, extend your budget, maintain quality.

### Why Tokens Matter

**The budget reality:**
- You've hit exhaustion at 2.5 weeks into a 4-week cycle
- That's ~37% of your potential usage time lost
- Root cause: context bloat eating tokens before you even type

**Where tokens go:**

| Category | Who controls it | Your leverage |
|----------|-----------------|---------------|
| System context (skills, instructions) | You | **High** — audit and prune |
| Conversation history | Accumulates automatically | **Medium** — restart strategically |
| Your prompts | You | **Medium** — be concise |
| AI responses | AI | **Low** — but you can ask for brevity |

The biggest win is system context—stuff that loads *every single time*.

### The Token Tax: What Loads Automatically

Every Copilot interaction pays a "tax" before you say anything:

```
Your estimated current tax:
┌─────────────────────────────────────────────────────┐
│ copilot-instructions.md (800+ lines)    ~3,000 tokens │
│ xlsx skill                              ~2,500 tokens │
│ docx skill                              ~2,500 tokens │
│ pdf skill                               ~2,500 tokens │
│ pptx skill                              ~2,500 tokens │
├─────────────────────────────────────────────────────┤
│ TOTAL BEFORE YOU TYPE                  ~13,000 tokens │
└─────────────────────────────────────────────────────┘
```

**Comparison:**
- A typical back-and-forth exchange: ~500-2,000 tokens
- Your per-interaction tax: ~13,000 tokens
- You're spending 6-26x more on *setup* than on *actual work*

### Reducing the Token Tax

**Strategy 1: Slim the global instructions**

Your `copilot-instructions.md` is 800+ lines. Most of it probably isn't needed on every interaction.

**Before (bloated):**
```markdown
## Python Guidelines
[200 lines of Python best practices AI already knows]

## Available Instructions
- python.instructions.md
- java.instructions.md
- dataverse-python-*.md (16 files!)
[Full catalog of everything you downloaded]

## Training Tracker Architecture
[Project-specific details in global config]
```

**After (lean):**
```markdown
## Environment
- Python venv: `_Documentation/.venv`
- Pre-installed: pandas, openpyxl, python-pptx, python-docx, PyPDF2
- Do not include pip install commands

## Conventions
- Work in progress → `_scratch/`
- Session state → `HANDOFF.md`
- Follow existing code style in each project
```

**Target:** Global instructions under 50 lines (~500 tokens).

**Strategy 2: Move project context to project config**

Training Tracker details don't belong in global config—they load for *every* project.

**Move to `Training/.github/copilot-instructions.md`:**
```markdown
## Training Tracker Project
- Main script: create_training_tracker.py
- Output: _output/training_tracker.xlsx
- Current focus: deduplication logic
```

Now this only loads when you're in the Training folder.

**Strategy 3: Audit your skills**

For each skill, ask:
1. **Do I use this weekly?** No → Consider removing or moving to `_reference/`
2. **Does it teach AI something it doesn't know?** No → Remove (pandas basics, etc.)
3. **Does it reference tools that exist?** No → Fix or remove phantom references

**The hard question:** Do you actually need all four document skills (xlsx, docx, pdf, pptx) loaded globally? If you only do Excel work in one project, that skill could be project-level.

**Strategy 4: Stop cataloging available resources**

Listing files in your instructions may cause them to load (or at least wastes tokens listing them).

**Don't do this:**
```markdown
## Available Instructions
- python.instructions.md - Python conventions
- java.instructions.md - Java guidelines  
- powershell.instructions.md - PowerShell help
[etc.]
```

**Do this instead:**
```markdown
## Additional Resources
See `_reference/` folder for specialized instructions.
Load on-demand by asking: "Use the dataverse instructions for this task."
```

### Conversation-Level Optimization

Even with a lean setup, conversations accumulate tokens.

**The degradation curve:**
```
Tokens
  │
  │    ┌── Tax (skills, instructions)
  │    │
  │    │     Conversation history grows
  │    │    ╱
  │    │   ╱
  │    │  ╱
  │    │ ╱
  │    │╱
  └────┴─────────────────────────────────► Time
       Start                    Degradation
```

**When to restart** (from Section 9):
- Scroll bar is tiny (lots of accumulated content)
- AI repeating itself or forgetting details
- Response times noticeably slower
- You've been chatting for 30+ minutes on complex topics

**The restart isn't waste—it's investment.** A fresh conversation with good HANDOFF.md context is more efficient than pushing through a degraded one.

### Prompt Efficiency

**Be specific upfront:**

❌ **Expensive (multiple rounds):**
```
"Can you help me with my Python script?"
[AI asks clarifying questions]
"It's for processing Excel files"
[AI asks more questions]
"I need to deduplicate rows based on employee ID"
```

✅ **Efficient (one round):**
```
"In create_training_tracker.py, the merge on line 145 creates 
duplicate rows when an employee has multiple job duties. 
Help me deduplicate while keeping all job duty associations."
```

**The formula:** [File] + [Location] + [Problem] + [Desired outcome]

**Ask for brevity when appropriate:**

```
"Give me a quick answer—don't explain the basics."
"Just the code, no explanation needed."
"Summarize in 2-3 sentences."
```

AI defaults to thorough explanations. You can override that.

### Exclusion Patterns

Some files should never enter AI context.

**Files to exclude:**

| Category | Examples | Why |
|----------|----------|-----|
| Generated output | `_output/*.xlsx` | Large, changes frequently |
| Dependencies | `node_modules/`, `.venv/` | Huge, AI doesn't need them |
| Build artifacts | `__pycache__/`, `*.pyc` | Noise |
| Large data | `*.csv` over 1MB | Use summary or sample instead |
| Secrets | `.env`, credentials | Security + wasted tokens |

**For Copilot:**
There's no `.copilotignore` file (yet). Exclusion is implicit—don't reference these files, don't open them, keep them out of your working set.

**For Claude CLI:**
You can configure ignore patterns in `.claude/settings.json`:
```json
{
  "ignore": [
    "_output/",
    "*.xlsx",
    "__pycache__/"
  ]
}
```

### Measuring Your Token Usage

**The frustrating truth:** Neither Copilot nor Claude CLI currently show per-session token breakdowns in consumer interfaces.

**What you can observe:**
- Conversation length before degradation
- Time until monthly budget exhaustion
- Response time changes during a session

**Proxy measurements:**
- Count lines in your instructions file (~7-10 tokens per line)
- Count lines in your skills (~7-10 tokens per line)
- Add them up for your approximate "tax"

**Your rough formula:**
```
Daily capacity ≈ Monthly budget ÷ Working days
Per-session capacity ≈ Daily capacity ÷ Sessions per day
Usable per session ≈ Per-session capacity - Token tax
```

If your tax is high and your usable capacity is low, that explains the 2.5-week exhaustion.

### The Token Optimization Checklist

**One-time setup (do once, benefit forever):**
- [ ] Slim global `copilot-instructions.md` to <50 lines
- [ ] Move project-specific content to project-level config
- [ ] Audit skills—remove generic ones, fix phantom references
- [ ] Stop cataloging available resources in instructions
- [ ] Set up ignore patterns for large/generated files

**Per-session habits:**
- [ ] Start with specific, complete prompts
- [ ] Ask for brevity when you don't need explanations
- [ ] Restart when conversation degrades (don't push through)
- [ ] Use HANDOFF.md to restore context cheaply

**Weekly review:**
- [ ] Are you hitting budget limits? If so, audit again.
- [ ] Any new skills or instructions added? Check their size.
- [ ] Conversation patterns—are you restarting enough?

### Questions Answered

| Question | Answer |
|----------|--------|
| How to see exactly what's in context? | No direct visibility in Copilot. Click "X items" indicator for partial view. For instructions, count lines × ~8 tokens. |
| Can you exclude specific files from Copilot's context? | No `.copilotignore` exists. Exclude implicitly by not referencing them and keeping them closed. |
| What's the token cost of your current global instructions? | Estimate: 800 lines × 8 tokens ≈ 6,400 tokens for instructions alone. With skills: ~13,000 tokens. |

---

## 7. Hooks & Automation

**Goal:** Prevent chaos before it happens, automate cleanup with minimal friction.

### Understanding Hooks

| Hook Type | Trigger | Available To You? |
|-----------|---------|-------------------|
| **Git hooks** | Git events (commit, push) | ✓ Yes (you commit locally) |
| **File watchers** | File saved/created | ✓ Yes (VS Code) |
| **AI post-action** | After AI modifies code | ✗ Doesn't exist |

**Key insight:** There's no way to hook into "every time AI modifies a file." You can only hook into git events or file system events.

### Case Study: The Training Folder Problem

**Before (sprawl):**
```
Training/
├── BC-LAR-ENGPRO001.xlsx      # Input data
├── BC-LAR-ENGPRO002.xlsx      # Input data
├── ... (8 more input files)
├── Training_Attendance_Tracker.xlsx  # Output
├── consolidate_training_data.py      # Main script
├── check_python_courses.py           # One-off troubleshooting
├── create_job_duty_filters.py        # One-off troubleshooting
├── create_training_tracker.py        # One-off troubleshooting
├── extract_course_names.py           # One-off troubleshooting
└── remove_by_employee.py             # One-off troubleshooting
```

**The problem isn't the flat structure—it's mixing production with experiments.**

**After (cleaned up, still flat):**
```
Training/
├── README.md
├── HANDOFF.md
├── _TODO.md
├── consolidate_training_data.py      # Main script (at root)
├── BC-LAR-ENGPRO001.xlsx             # Input files (at root—only 10)
├── BC-LAR-ENGPRO002.xlsx
├── ... (8 more input files)
├── _output/
│   └── Training_Attendance_Tracker.xlsx  # Generated output
└── _scratch/
    ├── check_python_courses.py       # One-off troubleshooting
    ├── create_job_duty_filters.py    # Experiments
    ├── create_training_tracker.py    # Old versions
    ├── extract_course_names.py
    └── remove_by_employee.py
```

**What changed:**
- Main script stays at root (it's production)
- Input files stay at root (only 10—not enough to need a folder)
- Generated output goes in `_output/`
- One-off/debug scripts go in `_scratch/`
- Added Core Three markdown files

**Per Section 3:** Only add `_input/` when you have many input files (20+). Stay flat until it hurts.

### Tool 1: Cleanup Check Script (Dry-Run First)

A Python script that scans your project and suggests what to move to `_scratch/` or `_output/`:

```
python cleanup_check.py

Output:
============================================================
CLEANUP CHECK (dry-run)
Scanning: C:\Users\...\Training
============================================================

⚠️  6 files could be organized:

  → _scratch/  (one-off scripts, experiments)
      check_python_courses.py
        (reason: matches 'check_' pattern)
      create_job_duty_filters.py
        (reason: troubleshooting script)
      create_training_tracker.py
        (reason: superseded by main script)
      extract_course_names.py
        (reason: one-off utility)
      remove_by_employee.py
        (reason: one-off utility)

  → _output/  (generated files)
      Training_Attendance_Tracker.xlsx
        (reason: matches output pattern 'Tracker')

✓  Files staying at root (correct):
      consolidate_training_data.py (main script)
      BC-LAR-ENGPRO*.xlsx (input files - only 10)

------------------------------------------------------------
Run with --fix to move files automatically
```

**Configuration in the script:**
```python
# Files that stay at root level
ROOT_ALLOWED = {
    'README.md', 'HANDOFF.md', '_TODO.md', 
    'requirements.txt', 'CLAUDE.md', '.gitignore'
}

# Your main scripts (stay at root, not _scratch/)
MAIN_SCRIPTS = {'consolidate_training_data.py'}

# Patterns that indicate one-off/debug work → _scratch/
SCRATCH_PATTERNS = ['check_', 'debug_', 'test_', '_v1', '_v2', 'old_', 'temp_']

# Patterns that indicate generated output → _output/
OUTPUT_PATTERNS = ['Tracker', 'Report', 'Output', 'Final', 'Generated']

# Note: Input files (.xlsx, .csv) stay at root unless you have 20+
# Only then consider creating _input/ folder
```

### Tool 2: Pre-Commit Hook (Git Integration)

Once you're comfortable with the cleanup check, integrate it into git:

**Installation:**
```bash
# Create hooks directory if needed
mkdir -p .git/hooks

# Create pre-commit hook
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
echo "Running cleanup check..."
python cleanup_check.py --warn-only

# Exit code 0 = allow commit (warn but don't block)
exit 0
EOF

# Make executable
chmod +x .git/hooks/pre-commit
```

**Important Notes:**
- **Hook location:** `.git/hooks/pre-commit` (inside the hidden `.git` folder)
- **Hidden folder:** The `.git` folder is hidden by default in Windows File Explorer
- **Not synced:** Git hooks are local only - they don't sync via push/pull for security reasons
- **Per-clone:** Each repository clone needs its own hook setup
- **Manual distribution:** To share hooks with team, document setup in README or use a script

**Behavior:**
```
$ git commit -m "Updated training tracker"

Running cleanup check...
⚠️  3 files could be organized:
  → _scratch/
      new_debug_script.py (reason: matches scratch pattern)
      
Proceeding with commit anyway...
[main 1234567] Updated training tracker
```

**Escalation path:**
1. Start with `exit 0` (warn but commit)
2. Later, change to `exit 1` if warnings found (block until fixed)
3. Eventually, use `--fix` to auto-organize before commit

### Tool 3: VS Code File Watcher (Optional)

For reducing noise in VS Code's file watcher:

**.vscode/settings.json:**
```json
{
  "files.watcherExclude": {
    "**/_scratch/**": true,
    "**/_output/**": true,
    "**/_archive/**": true
  }
}
```

This doesn't move files, but reduces noise from generated and temporary files.

**For actual auto-organization,** you'd need a VS Code extension or external file watcher—more complexity than it's worth for most workflows.

### Recommended Approach

| Phase | Action | Effort |
|-------|--------|--------|
| **Now** | Run `cleanup_check.py --fix` on existing projects | One-time |
| **Week 1** | Run `cleanup_check.py` manually before commits | Manual habit |
| **Week 2+** | Add pre-commit hook with warn-only | Automatic |
| **Later** | Tighten to block commits if needed | Optional |

### What About AI-Assisted Cleanup?

You asked about having AI decide what's dead code. Two options:

**Option A: Rule-based (free, instant)**
```python
# In cleanup_check.py
SCRATCH_PATTERNS = ['check_', 'debug_', 'test_', '_v1', '_v2']
# Matches patterns → suggest _scratch/
```

**Option B: AI-assisted (costs tokens)**
```
"Look at these 5 Python files and tell me which are 
one-off troubleshooting scripts vs. production code"
```

**Recommendation:** Start with rules. AI judgment is overkill for file organization—patterns catch 90% of cases.

### Adding Dead Code Detection

To catch unused imports (the other issue you mentioned), add this to the cleanup check:

```python
import ast

def find_unused_imports(filepath):
    """Basic unused import detection."""
    with open(filepath) as f:
        tree = ast.parse(f.read())
    
    imports = set()
    used_names = set()
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.asname or alias.name)
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                imports.add(alias.asname or alias.name)
        elif isinstance(node, ast.Name):
            used_names.add(node.id)
    
    return imports - used_names
```

**Output:**
```
⚠️  Potential unused imports:
    consolidate_training_data.py
      - os (line 3)
      - sys (line 4)
```

This is rule-based, instant, and free—no AI needed.

### Summary: Your Hook Strategy

| Trigger | What Runs | Behavior |
|---------|-----------|----------|
| Manual | `python cleanup_check.py` | Dry-run report |
| Manual | `python cleanup_check.py --fix` | Actually move files |
| Pre-commit | Hook runs cleanup_check | Warn but allow commit |
| Future | Hook with `exit 1` | Block commit until clean |

### When AI Actually Helps: One-Time Decisions

Rule-based tools handle ongoing organization. But for one-time cleanup decisions like "are these old scripts useful?", AI is the right tool.

**Real Example:**

Prompt sent to Claude CLI:
```
Look at these 5 Python scripts and tell me:
1. What does each one do?
2. Is the functionality now covered by consolidate_training_data.py?
3. Are any of them useful to keep as utilities?
```

**Result (30 seconds, ~500 tokens):**

| Script | AI Analysis | Action |
|--------|-------------|--------|
| `check_python_courses.py` | One-off diagnostic, trivially reproducible | Delete |
| `create_job_duty_filters.py` | **Not covered by main script, still useful** | Keep |
| `create_training_tracker.py` | v1 prototype, fully superseded | Delete |
| `extract_course_names.py` | Logic now embedded in main script | Delete |
| `remove_by_employee.py` | Cleans up sheet that no longer exists | Delete |

**Without AI:** 20+ minutes reading each script to understand it.
**With AI:** 30 seconds, clear actionable answer.

**The Pattern:**
- Use AI for **understanding** (one-time, high-value)
- Use rules for **ongoing automation** (free, consistent)
- Use time for **importance filtering** (if untouched for 30 days, probably safe to archive)

---

## 8. Markdown & Documentation Standards

**Goal:** Consistent, purposeful documentation that AI can use effectively—without over-engineering into "where did I put that?" territory.

### The Sprawl Problem

**How it happens:**
1. You start chatting with AI about an idea
2. The conversation grows; AI proposes creating files
3. AI names them based on the moment: `notes.md`, `handoff.md`, `project-notes.md`, `TODO.md`
4. Repeat across sessions and projects
5. Now you have `handoff.md`, `handdown.md`, `HANDOFF.md`, `session-notes.md`...

**The root cause:** AI generates file names ad-hoc based on conversation context, not a consistent system. You end up with whatever felt right at the time.

**The fix:** Give AI (and yourself) a simple framework so emergent files land predictably.

### The Core Three: Minimum Viable Documentation

Most projects need only three markdown files at root level:

| File | Purpose | Audience | Update Frequency |
|------|---------|----------|------------------|
| `README.md` | What this project is, how to use it | Humans (you, colleagues) | Project milestones |
| `HANDOFF.md` | Current state for continuing work | **AI** (fresh conversations) | End of each session |
| `_TODO.md` | Tasks, ideas, parking lot | You | Ongoing |

**Why these three?**
- **README** = the human onboarding doc (what and why)
- **HANDOFF** = the AI onboarding doc (where we are and what's next)
- **_TODO** = the junk drawer with a lid (prefixed with `_` so it sorts first, signals "internal")

**What about DECISIONS.md and CHANGELOG.md?**
Add them when you need them—not by default:
- `DECISIONS.md` → When you're making architectural choices you'll forget the rationale for
- `CHANGELOG.md` → When you're versioning releases for others to consume

For solo documentation work, these are often overkill.

### HANDOFF.md: Writing for AI, Not Humans

This is the key insight: **HANDOFF.md exists to restore context in a fresh AI conversation.**

You remember what you were doing. The AI doesn't. When a conversation gets slow, loopy, or forgetful, you start fresh—and HANDOFF.md is how the new conversation catches up.

**What AI needs to continue your work:**

```markdown
# HANDOFF — Training Tracker

> Last updated: 2025-01-29 3:30 PM

## Current State
- Main script `create_training_tracker.py` is functional
- Outputs to `_output/training_tracker.xlsx`
- Uses shared venv at `_Documentation/.venv`

## What's Working
- Employee data import from CSV
- Course filtering by job duty
- Excel formatting with frozen headers

## Current Problem
Duplicate entries appearing when employee has multiple job duties.
Attempted fix in lines 142-156 didn't resolve it.

## Next Step
Debug the deduplication logic. Start by printing the intermediate 
dataframe after the merge on line 145.

## Files to Know About
- `create_training_tracker.py` — Main script (the focus)
- `job_duties.csv` — Input mapping file
- `_scratch/debug_output.xlsx` — Test output from failed fix
```

**What makes this AI-effective:**
- **Context at the top** — Project name, last updated
- **State before problems** — What's working establishes baseline
- **Specific location of issue** — Line numbers, file names
- **Concrete next action** — Not "fix the bug" but "print dataframe after line 145"
- **File inventory** — AI can ask to see the right files

**Anti-patterns:**
- ❌ "See previous conversation" — There is no previous conversation for the AI
- ❌ "The usual approach" — Nothing is usual to a fresh context
- ❌ "Fix the issues we discussed" — What issues? Be explicit.

### Preventing Sprawl: The _scratch Pattern

**The problem:** Work-in-progress files accumulate at project root, mixed with "real" files.

**The solution:** One designated mess zone.

```
Training/
├── README.md                 ← Stays clean
├── HANDOFF.md                ← Always current
├── _TODO.md                  ← Tasks and ideas
├── create_training_tracker.py
├── job_duties.csv
│
└── _scratch/                 ← All work-in-progress goes here
    ├── debug_output.xlsx
    ├── test_merge.py
    ├── old_approach.py
    └── notes_from_meeting.md
```

**Rules for _scratch:**
1. Anything experimental or temporary goes here
2. When something graduates to "real," move it to root
3. Periodically empty it (weekly, or when it gets noisy)
4. It's okay for this folder to be messy—that's its job

**Tell the AI about _scratch:**
Add to your project instructions or HANDOFF.md:
```markdown
## Working Conventions
- In-progress files go in `_scratch/`
- When creating new files, put experiments in `_scratch/` and production files at root
```

### Naming Conventions: Taming AI-Generated Files

When AI proposes creating a file, it will use whatever name feels natural in the moment. You can steer this.

**Add to your copilot-instructions.md or HANDOFF.md:**

```markdown
## File Naming Conventions
When creating markdown files:
- Session handoff → `HANDOFF.md` (overwrite, don't create new)
- Tasks/ideas → append to `_TODO.md`
- Meeting notes → `_scratch/meeting_YYYY-MM-DD.md`
- Temporary analysis → `_scratch/analysis_[topic].md`

When creating scripts:
- Main/production scripts → root level, descriptive name
- Test/debug scripts → `_scratch/test_[what].py`
```

**The key principle:** Overwrite HANDOFF.md, append to _TODO.md, dump everything else in _scratch.

### Consolidation Triggers

**When to clean up:**
- More than 5 markdown files at project root → consolidate
- Files in `_scratch/` older than 2 weeks → archive or delete
- You can't find something → structure has failed, simplify

**Consolidation checklist:**
1. Is this file still relevant? → No: delete or archive
2. Does this duplicate another file? → Merge into one
3. Is this a "real" file or work-in-progress? → Move to appropriate location
4. Does the name follow conventions? → Rename

**Archive strategy:**
```
Training/
├── _archive/                 ← Completed/old stuff you might need
│   ├── 2024-Q4-approach/    ← Group by time or version
│   └── abandoned-ideas/
└── _scratch/                 ← Current work-in-progress
```

The difference: `_scratch` is active mess; `_archive` is inactive but preserved.

### Teaching Colleagues: The Minimum Transferable System

Since you're the test subject for Process Controls, here's what colleagues need to learn:

**The 60-second version:**
1. Every project has `README.md` (what it is), `HANDOFF.md` (where we are), `_TODO.md` (what's pending)
2. Temporary work goes in `_scratch/`
3. At end of session, update HANDOFF.md so a fresh AI conversation can continue
4. When it gets messy, clean up

**The one-pager for colleagues:**

```markdown
# Documentation Standards for AI-Assisted Work

## Required Files (every project)
- `README.md` — What this project does, how to run it
- `HANDOFF.md` — Current state, for continuing in fresh AI sessions
- `_TODO.md` — Tasks, ideas, parking lot

## Folder Conventions
- `_scratch/` — Work in progress, experiments, temporary files
- `_archive/` — Old stuff you might need someday (optional)

## The Key Habit
Before closing a session: update HANDOFF.md with current state and next steps.
This lets you (or anyone) start a fresh AI conversation and pick up where you left off.
```

### Questions Answered

| Question | Answer |
|----------|--------|
| Which standard files would you actually use? | Core three: README, HANDOFF, _TODO. Add DECISIONS/CHANGELOG only when needed. |
| Should HANDOFF.md be auto-generated or manually maintained? | AI-assisted at end of session. Say "update HANDOFF.md with our current state." |
| Archive strategy for old documentation? | `_archive/` folder for things you might need; delete things you won't. |

---

## 9. Workflow Patterns

**Goal:** Repeatable processes that keep projects clean from the start—without becoming a second job.

### The AI Conversation Lifecycle

Understanding this cycle is key to knowing *when* to do things:

```
┌─────────────────────────────────────────────────────────────┐
│  FRESH          PRODUCTIVE        DEGRADED        RESTART  │
│    │                │                 │              │      │
│    ▼                ▼                 ▼              ▼      │
│  Context         Working           Slow,          Start    │
│  is empty        well             loopy,          new      │
│                                   forgetful       chat     │
│    │                │                 │              │      │
│    └────────────────┴────────────────┴──────────────┘      │
│         ▲                                      │            │
│         │          HANDOFF.md                  │            │
│         └──────────────────────────────────────┘            │
└─────────────────────────────────────────────────────────────┘
```

**The pattern:**
1. Start fresh → AI knows nothing
2. Prime with context → AI becomes productive
3. Work until degradation → AI slows down, repeats itself, forgets details
4. Capture state → Write HANDOFF.md
5. Restart → New conversation, load HANDOFF.md, back to productive

**Your job:** Recognize the transition points and act on them.

### Starting a Session

**Scenario A: Continuing existing work**

1. Open project folder
2. Start new AI conversation
3. Prime with context:
   ```
   I'm continuing work on [project]. Here's the current state:
   [paste HANDOFF.md contents or attach file]
   
   I want to work on: [specific goal for this session]
   ```
4. Verify AI understands: Ask it to summarize the current state back to you

**Scenario B: Starting new work in existing project**

1. Open project folder
2. Start new AI conversation
3. Brief context + new goal:
   ```
   This is my [project name] project. [One sentence on what it does.]
   
   Today I want to: [new thing]
   ```
4. Let AI ask clarifying questions before diving in

**Scenario C: Starting a brand new project**

1. Create project folder
2. Create minimal structure:
   ```
   NewProject/
   ├── README.md      ← Even just a title and one-sentence purpose
   ├── HANDOFF.md     ← Can be empty or "Project just started"
   └── _scratch/      ← Create the folder now, use it immediately
   ```
3. Start AI conversation with intent:
   ```
   I'm starting a new project: [name]
   Purpose: [what it will do]
   
   Help me [first task: plan it out / create initial structure / etc.]
   ```

**The minimum viable start:** Open folder, open chat, state your goal. Don't over-ritualize.

### During a Session

**Where things go:**
- Experimental code → `_scratch/`
- Test outputs → `_scratch/`
- Notes from this session → `_scratch/` or append to `_TODO.md`
- "Real" code/files → project root (only when validated)

**Healthy session habits:**
- **One goal at a time** — Finish or park one thing before starting another
- **Name things immediately** — When AI creates a file, make sure it follows conventions
- **Move, don't copy** — When something graduates from `_scratch/`, move it (delete the original)
- **Note dead ends** — Quick note in `_TODO.md`: "Tried X, didn't work because Y"

**Signals the conversation is still healthy:**
- AI remembers details from earlier in the conversation
- Responses are quick
- AI builds on previous context without re-explaining
- Suggestions are relevant to your project

### Recognizing Degradation

**Signals it's time to start fresh:**

| Signal | What it looks like |
|--------|-------------------|
| **Looping** | AI suggests something you already tried, or repeats explanations |
| **Forgetting** | AI asks about something you already discussed, or contradicts earlier statements |
| **Slowing** | Noticeably longer response times |
| **Drifting** | Suggestions that don't fit your project context |
| **Bloating** | Scroll bar in chat window is tiny (lots of content) |

**The scroll bar test:** If the scroll bar is a tiny sliver, you've probably been chatting too long.

**Don't push through degradation.** It feels efficient to keep going, but you'll waste more time fighting a confused AI than starting fresh with good context.

### Ending a Session

**The 2-minute close-out:**

1. **Update HANDOFF.md** — Ask AI to help:
   ```
   Summarize our current state for HANDOFF.md. Include:
   - What's working now
   - What we were trying to do
   - Where we got stuck (if anywhere)
   - Suggested next step
   ```
   
2. **Review what AI wrote** — Make sure it's accurate; you know things AI doesn't

3. **Triage _scratch/** — Quick scan:
   - Keep: Still need it
   - Move: It's "real" now, promote to root
   - Delete: Junk from dead ends

4. **Optional: Update _TODO.md** — If new tasks emerged, capture them

**The minimum viable end:** Update HANDOFF.md. Everything else is nice-to-have.

### The "Abandon Ship" Decision

Sometimes you need to restart mid-task, not at a natural stopping point.

**When to abandon:**
- AI is confidently wrong and won't course-correct
- You've explained the same thing 3+ times
- AI is stuck in a loop suggesting the same failed approach
- Response time has become painful

**How to abandon gracefully:**
1. Don't try to salvage the conversation
2. Copy any useful code/text to a file (or `_scratch/`)
3. Quick HANDOFF.md update (even rough notes are better than nothing)
4. Start completely fresh
5. In new chat, prime with HANDOFF.md + explicit note about what didn't work:
   ```
   [HANDOFF.md contents]
   
   Note: Previous attempt to [X] failed because [Y]. 
   Let's try a different approach.
   ```

### Session Patterns by Duration

**Quick task (< 30 min):**
- Skip HANDOFF.md if task will complete this session
- Work directly, don't over-structure
- If you don't finish, *then* write HANDOFF.md

**Focused session (1-2 hours):**
- Start with HANDOFF.md review
- Single goal or related set of goals
- End with HANDOFF.md update
- Expect 1-2 conversation restarts if complex

**Deep work (half day):**
- Plan for 2-3 fresh conversations
- HANDOFF.md between each
- Use `_scratch/` heavily for iterations
- End-of-day consolidation: clean `_scratch/`, update README if scope changed

### Weekly Maintenance (15 minutes)

Pick a day. Do this once a week:

1. **Review active projects** — Is HANDOFF.md current in each?
2. **Clean _scratch/ folders** — Delete or archive anything > 2 weeks old
3. **Check for sprawl** — Any project root have > 5 markdown files? Consolidate.
4. **Update _TODO.md** — Remove completed items, add anything you've been carrying in your head

**Why weekly?** Daily is too much ceremony. Monthly lets things rot. Weekly catches drift before it compounds.

### Teaching Colleagues: The Workflow Cheat Sheet

For Process Controls team adoption:

```markdown
# AI Workflow Quick Reference

## Starting
1. Open project folder
2. New chat → paste HANDOFF.md or describe goal
3. Verify AI understands before diving in

## During
- Experiments go in `_scratch/`
- Working code stays at root
- One goal at a time

## Ending (THE KEY HABIT)
- Ask AI: "Update HANDOFF.md with our current state"
- Review for accuracy
- Quick _scratch/ triage

## When to Restart
- AI repeating itself or forgetting
- Responses getting slow
- Scroll bar is tiny (chat too long)
- You've explained something 3+ times

## Weekly (15 min)
- Clean _scratch/ folders
- Check HANDOFF.md is current
- Remove completed items from _TODO.md
```

### Questions Answered

| Question | Answer |
|----------|--------|
| How much ceremony is acceptable? | Minimal: state goal at start, update HANDOFF.md at end. Weekly maintenance pass. |
| Would a checklist or script help? | The cheat sheet above is your checklist. Scripts for file cleanup exist (see Section 7). Automating HANDOFF.md is overkill—just ask AI to write it. |

---

## 10. MCP & Tool Integration

**Goal:** Understand what those "7 MCP Connected" servers are actually doing and whether you need them.

### MCP in Plain English

**MCP = Model Context Protocol**

Think of it like USB ports for AI. Just as USB lets you plug different devices into your computer, MCP lets you plug different *capabilities* into Claude.

Without MCP: Claude can only work with what you paste into the chat.

With MCP: Claude can reach out and interact with external systems—read files, query databases, call APIs, run tools.

**The "7 MCP Connected" indicator** means Claude CLI has 7 different "plugins" available that extend what it can do.

### What Are MCP Servers?

Each MCP "server" is a small program that gives Claude a specific capability:

| Server Type | What It Does | Example Use |
|-------------|--------------|-------------|
| **Filesystem** | Read/write files on your computer | "Read the CSV in my Downloads folder" |
| **Git** | Interact with git repositories | "Show me the last 5 commits" |
| **GitHub** | Access GitHub APIs | "List open PRs in this repo" |
| **Database** | Query databases | "Show me customers added this week" |
| **Web/Fetch** | Retrieve web content | "Get the docs from this URL" |
| **Memory** | Persistent storage across sessions | "Remember that I prefer tabs over spaces" |
| **Custom** | Whatever you build | Run your own scripts as tools |

**The key insight:** MCP servers are *capabilities*, not content. They don't consume tokens sitting idle—they only cost tokens when Claude actually uses them.

### Your 7 Connected Servers

You're seeing "7 MCP Connected" but don't know what they are. Here's how to find out:

**In Claude CLI, run:**
```bash
claude mcp list
```

This will show all configured MCP servers and their status.

**Common default servers** (you likely have some of these):

| Server | Likely Included? | Purpose |
|--------|------------------|---------|
| `filesystem` | ✅ Probably | Read/write local files |
| `git` | ✅ Probably | Git operations |
| `fetch` | ✅ Probably | Retrieve web content |
| `memory` | Maybe | Persistent memory across sessions |
| `github` | Maybe | GitHub API access |
| `postgres`/`sqlite` | Unlikely | Database access (you'd know if you set this up) |
| `brave-search` | Maybe | Web search capability |

**To see details:**
```bash
claude mcp status
```

### Do You Need All 7?

**Probably not.** Most users only actively use 2-3 MCP servers.

**The ones you likely use without realizing:**
- **Filesystem** — This is how Claude CLI reads your project files
- **Git** — If you've asked Claude to check git status or commit

**The ones you might not need:**
- Database servers (if you're not querying databases)
- GitHub API (if you're not interacting with GitHub through Claude)
- Memory server (if you haven't explicitly used persistent memory)

**Should you disable unused servers?**

Unlike Copilot's instruction files (which consume tokens), idle MCP servers don't cost you tokens. They just sit ready.

However, there are reasons to clean up:
- **Clarity** — Knowing what's available helps you use it
- **Security** — Each server is a capability; fewer = smaller attack surface
- **Troubleshooting** — Fewer moving parts = easier debugging

### How MCP Actually Works

When you ask Claude something that requires an external tool:

```
You: "Read the HANDOFF.md file in this folder"

Claude thinks: "I need to read a file. I have a filesystem MCP server."

Claude → MCP Server: "Read /path/to/HANDOFF.md"

MCP Server → Claude: [file contents]

Claude: "Here's what HANDOFF.md says: ..."
```

**You don't have to explicitly invoke MCP.** Claude decides when to use tools based on your request. If you ask to read a file, it uses filesystem. If you ask about git history, it uses git.

### Common MCP Use Cases

**Filesystem (you're already using this):**
```
"Read all Python files in this folder and summarize what each does"
"Create a new file called utils.py with these functions"
"Find all files modified in the last week"
```

**Git (if you have it):**
```
"What changed in the last commit?"
"Show me the diff for this file"
"Create a commit with message 'Fix deduplication bug'"
```

**Fetch/Web (if you have it):**
```
"Get the pandas documentation for read_excel"
"Fetch the README from this GitHub repo URL"
```

**Memory (if you have it):**
```
"Remember that this project uses tabs, not spaces"
"What preferences have I told you about?"
```

### Configuring MCP Servers

MCP servers are configured in Claude CLI's settings. Location depends on your OS:

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

**Mac:**
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Linux:**
```
~/.config/Claude/claude_desktop_config.json
```

**Example configuration:**
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-filesystem", "/path/to/allowed/folder"]
    },
    "git": {
      "command": "npx", 
      "args": ["-y", "@anthropic/mcp-server-git"]
    }
  }
}
```

**To disable a server:** Remove or comment out its entry in the config file.

**To add a server:** Add a new entry with the appropriate command and arguments.

### MCP Security Considerations

Each MCP server is a capability you're granting to Claude. Think about what you're enabling:

| Server | What It Can Access | Risk Level |
|--------|-------------------|------------|
| Filesystem (scoped) | Only specified folders | Low |
| Filesystem (broad) | Large parts of your disk | Medium |
| Git | Your repository history | Low |
| GitHub (with token) | Your GitHub account | Medium |
| Database | Your database contents | High |
| Arbitrary command execution | Anything | Very High |

**Best practices:**
- **Scope filesystem access** — Don't give access to your entire home directory
- **Use read-only when possible** — Some servers have read-only modes
- **Audit periodically** — Check what's connected and why
- **Remove unused servers** — If you're not using it, disable it

### MCP vs. Copilot Context

Important distinction:

| Aspect | Copilot "13 references" | MCP "7 connected" |
|--------|------------------------|-------------------|
| What it is | Files loaded into context | Capabilities available |
| Token cost | Constant (loaded every time) | On-demand (only when used) |
| Main concern | Bloat, wasted tokens | Security, complexity |
| Fix for bloat | Move files out of auto-load | Not applicable |

**Your Copilot bloat problem (13 references) is NOT related to MCP.** They're different tools with different issues.

### When to Expand MCP Usage

You might want to add MCP capabilities when:

- **You're doing repetitive external lookups** — Web search server could help
- **You work with databases** — Database server for direct queries
- **You want Claude to remember things** — Memory server for preferences
- **You have custom workflows** — Build your own MCP server

**For now:** You don't need to change anything. Your 7 servers are likely working fine in the background. Just knowing they exist and what they do is enough.

### Homework: Audit Your MCP Setup

When you have time, run these commands to understand your setup:

```bash
# List all configured servers
claude mcp list

# Check status of each server
claude mcp status

# See what servers are available to install
claude mcp search
```

Then ask yourself:
- Do I recognize all 7 servers?
- Am I using capabilities I didn't know I had?
- Are any servers accessing things I'd rather they didn't?

### Questions Answered

| Question | Answer |
|----------|--------|
| What are the 7 MCP servers? | Run `claude mcp list` to see. Likely filesystem, git, fetch, and a few others. |
| Am I using them? | Filesystem almost certainly (how Claude reads your files). Others depend on your tasks. |
| Should I disable any? | Only if you want to reduce complexity or limit capabilities. They don't cost tokens when idle. |
| Is this related to my Copilot token problem? | No. MCP is Claude CLI; your token bloat is Copilot's instruction files. Different tools, different issues. |

---

## 10.5 Environment Management (Python)

**Goal:** Consistent, predictable Python environments without confusion or redundancy.

### The Multiple venv Problem

**Symptoms:**
- Every project has its own `.venv` folder
- You reinstall pandas, openpyxl, python-pptx in each project
- Multiple terminals open, unsure which venv is active
- AI generates `pip install` commands because it doesn't know what's installed

**The Cost:**
- Disk space (duplicate packages everywhere)
- Time (reinstalling same dependencies)
- Confusion (which terminal? which venv?)
- AI token waste (defensive pip install commands)

### Recommended Pattern: Shared Workspace venv

For documentation-heavy work with consistent tooling:

```
_Documentation/
├── .venv/                     ← ONE venv at workspace root
├── requirements.txt           ← All shared dependencies
│
├── Training/                  ← Inherits parent venv
│   └── (no .venv here)
├── Graphics/                  ← Inherits parent venv
└── SAP/                       ← Inherits parent venv
```

**Setup once:**
```bash
cd _Documentation
python -m venv .venv
.venv\Scripts\activate         # Windows
pip install pandas openpyxl python-pptx python-docx PyPDF2
pip freeze > requirements.txt
```

**VS Code configuration** (`.vscode/settings.json` at root):
```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/Scripts/python.exe"
}
```

### When to Use Separate venvs

| Scenario | Recommendation |
|----------|----------------|
| Same tools across all projects | Shared venv ✓ |
| One project needs different Python version | Separate venv for that project |
| Conflicting package versions | Separate venv |
| Deploying to production | Separate venv (mirror prod) |
| Learning/experimenting | Shared venv is fine |

### Telling the AI What's Installed

Add to your project instructions:
```markdown
## Python Environment
- Shared venv at workspace root: `_Documentation/.venv`
- Pre-installed: pandas, openpyxl, python-pptx, python-docx, PyPDF2
- Do NOT include pip install commands in scripts
```

This prevents the AI from adding defensive installation code.

### Terminal Management

**The problem:** Multiple terminals, multiple venvs, confusion.

**The fix:** 
1. Use VS Code's integrated terminal (auto-activates correct venv)
2. Close terminals you're not using
3. Name your terminals (right-click → Rename)
4. If confused, run: `which python` (Linux/Mac) or `where python` (Windows)

---

## 10.6 Agents & Autonomous Workflows

**Goal:** Understand when AI acts autonomously vs. interactively, and how to work effectively with agentic tools.

### What Makes Something "Agentic"?

**Chat (interactive):**
```
You: "How do I read an Excel file in Python?"
AI: "Use pandas: pd.read_excel('file.xlsx')"
You: "Now filter rows where status is 'Active'"
AI: "Use: df[df['status'] == 'Active']"
```
You drive each step. AI responds. You execute.

**Agent (autonomous):**
```
You: "Read the Excel file, filter active rows, and save to a new file"
AI: [reads file]
AI: [filters data]
AI: [writes output]
AI: "Done. Created filtered_output.xlsx with 47 rows."
```
AI plans and executes multiple steps. You review the result.

**The key difference:** Agents take *actions*, not just provide *answers*.

### The Agent Spectrum

Not all AI tools are equally agentic:

| Tool | Agentic Level | What It Can Do |
|------|---------------|----------------|
| Copilot autocomplete | None | Suggests code as you type |
| Copilot Chat | Low | Answers questions, generates code blocks |
| Claude.ai (web) | Low-Medium | Answers, can create artifacts/files |
| Claude CLI | **High** | Reads/writes files, runs commands, iterates |
| Claude Code | **High** | Full codebase access, executes code, git operations |
| Copilot Workspace | **High** | Plans and implements across multiple files |

**You're already using agents:** Claude CLI at home is agentic—it can read your files, write code, execute commands, and iterate on results.

### When to Use Agents vs. Chat

**Use chat (interactive) when:**
- Learning or exploring ("how does X work?")
- You want to understand before doing
- The task is ambiguous and needs discussion
- You don't trust the AI to execute correctly yet
- Security-sensitive operations (you want to review each step)

**Use agents (autonomous) when:**
- The task is well-defined with clear success criteria
- You'd just copy-paste the AI's suggestions anyway
- Multiple files or steps are involved
- The operation is reversible (or you have backups)
- Time matters more than understanding each step

**The trust gradient:**
```
Low trust                                         High trust
    │                                                 │
    ▼                                                 ▼
Chat about it → Generate code → Run with review → Let it run
```

As you build trust with a tool on a type of task, you can give it more autonomy.

### Working with Claude CLI (Your Home Setup)

Claude CLI is an agent. Here's how to use it effectively:

**Starting a task:**
```bash
claude "Read HANDOFF.md and continue where we left off"
```

Claude will:
1. Read your HANDOFF.md
2. Understand the current state
3. Propose next steps
4. Execute with your approval (or automatically, depending on settings)

**Scoping the work:**

Too broad (risky):
```bash
claude "Fix all the bugs in this project"
```

Well-scoped (better):
```bash
claude "In create_training_tracker.py, fix the duplicate row issue on line 145. 
The problem is employees with multiple job duties appear twice."
```

**The permission model:**

Claude CLI asks before taking significant actions:
- Creating/modifying files → Usually asks
- Running commands → Usually asks
- Reading files → Usually automatic

You can adjust this in settings, but the default "ask before writing" is good while building trust.

**Reviewing agent work:**

After Claude CLI completes a task:
1. **Check what changed:** `git diff` or review modified files
2. **Test the result:** Run the script, check the output
3. **Commit or revert:** If good, commit. If not, `git checkout .` to undo.

This is why git matters even for local work—it's your undo button for agent mistakes.

### Agent Guardrails

**Scope boundaries:**

Tell the agent what it should NOT touch:
```
"Fix the filtering logic in create_training_tracker.py. 
Don't modify the Excel formatting section—that's working fine."
```

**Checkpoint requests:**

For complex tasks, ask for pauses:
```
"Refactor this script in three phases:
1. Extract the data loading into a function — then pause for my review
2. Extract the filtering logic — then pause
3. Extract the output formatting — then pause"
```

**Dry-run mode:**

Ask the agent to explain before doing:
```
"What files would you modify to fix this bug? Don't make changes yet—just list them."
```

Then: "Okay, proceed with those changes."

**The reversibility principle:**

Before letting an agent run:
- Is this in git? (Can you revert?)
- Is this on real data or a copy?
- What's the blast radius if it goes wrong?

### Common Agent Patterns

**Pattern 1: The Informed Start**

Don't make the agent guess context:
```bash
# Bad - agent has to figure out what's going on
claude "continue working on this"

# Good - agent has full context
claude "Read HANDOFF.md. The current task is fixing deduplication. 
I tried the approach in _scratch/test_merge.py but it failed. 
Try a different approach using groupby instead."
```

**Pattern 2: The Iteration Loop**

Let the agent try, review, and refine:
```
You: "Write a script to process training data"
Agent: [creates script]
You: "Run it on the test file in _scratch/"
Agent: [runs, shows output]
You: "The date parsing is wrong—they're in MM/DD/YYYY format"
Agent: [fixes and re-runs]
You: "Good. Move the script to project root and update HANDOFF.md"
```

**Pattern 3: The Research Task**

Use agent capabilities for information gathering:
```
"Look at all Python files in this folder and tell me:
1. Which ones import pandas?
2. Which ones are likely one-off scripts vs. production code?
3. Any obvious code duplication between files?"
```

Agent can read and analyze faster than you can manually review.

**Pattern 4: The Cleanup Task**

Agents are good at tedious, well-defined operations:
```
"For each Python file in _scratch/:
1. Check if it's been modified in the last 30 days
2. If not, move it to _archive/
3. List what you moved"
```

### Agent Failure Modes

**Over-confidence:**
Agent makes changes without understanding your project's quirks.
*Fix:* Provide context. "The employee_id column has leading zeros that must be preserved as strings."

**Scope creep:**
Agent "helpfully" fixes things you didn't ask about.
*Fix:* Be explicit about boundaries. "ONLY modify the filter function. Nothing else."

**Infinite loops:**
Agent tries the same failing approach repeatedly.
*Fix:* Interrupt and redirect. "Stop. That approach isn't working. Let's try X instead."

**Hallucinated paths:**
Agent references files or functions that don't exist.
*Fix:* Ask it to verify. "List the actual files in this folder before modifying anything."

### HANDOFF.md for Agents

The HANDOFF.md format from Section 8 is especially important for agents:

```markdown
# HANDOFF — Training Tracker

## Current State
- Main script functional but has duplicate row bug
- Bug location: lines 142-156 in create_training_tracker.py

## What's Been Tried
- Simple drop_duplicates() — didn't work (loses job duty associations)
- See _scratch/test_merge.py for failed attempt

## Next Step
Try groupby approach: group by employee_id, aggregate job_duties into list

## Constraints
- Must preserve all job duty associations (no data loss)
- Output format must match existing Excel template
- Don't modify the Excel formatting section (lines 200-250)
```

An agent with this context can start working immediately without 10 rounds of clarifying questions.

### Teaching Colleagues: Agent Ground Rules

For the Process Controls team:

```markdown
# Working with AI Agents

## Before Letting an Agent Run:
- Is your work committed to git? (You need an undo button)
- Did you scope the task clearly?
- Did you specify what NOT to touch?

## The Trust Ladder:
1. Start with chat—understand what the AI would do
2. Move to "generate code, I'll run it"
3. Move to "run it, I'll review"
4. Only then: "run it autonomously"

## If Something Goes Wrong:
- git checkout . — Reverts all uncommitted changes
- git stash — Saves changes without committing (can restore later)
- Don't panic—agents rarely break things that can't be fixed

## Golden Rule:
The agent works for you. If it's going in the wrong direction, interrupt it.
```

### Questions Answered

| Question | Answer |
|----------|--------|
| What is an agent? | AI that takes actions (reads/writes files, runs commands) rather than just answering questions. Claude CLI is an agent. |
| When should I use agents vs. chat? | Chat for learning/exploring/sensitive ops. Agents for well-defined tasks, multi-step operations, tedious work. |
| How do I stay safe with agents? | Git everything, scope clearly, state boundaries, review before trusting, start with low autonomy. |

---

## 11. Security & Boundaries

**Goal:** Protect sensitive information while maximizing AI utility—especially when you're the test case for your team.

### The Two-Environment Reality

You operate in two distinct contexts:

| Aspect | Work | Home |
|--------|------|------|
| AI tool | GitHub Copilot | Claude CLI |
| Repository | Local only | GitHub (synced across 3 machines) |
| Data sensitivity | Higher (company data) | Lower (personal projects) |
| Policy constraints | Company IT policies | Your own judgment |
| Audience | Colleagues will inherit your patterns | Just you |

**The key insight:** Your work environment is inherently more contained (local only), but your home environment has more exposure (GitHub sync). Different risks, different mitigations.

### What Should Never Enter AI Context

**Absolute no-go (both environments):**

| Category | Examples | Why |
|----------|----------|-----|
| Credentials | Passwords, API keys, tokens | AI might echo them; they persist in logs |
| PII | SSNs, employee IDs, personal addresses | Privacy/compliance violations |
| Financial data | Account numbers, salary info, budgets | Confidential |
| Auth secrets | OAuth tokens, session cookies, private keys | Security breach waiting to happen |

**Work-specific no-go:**

| Category | Examples | Why |
|----------|----------|-----|
| Customer data | Client names, contracts, communications | Confidentiality agreements |
| Internal systems | Server names, IP addresses, architecture diagrams | Security exposure |
| Proprietary logic | Trade secrets, competitive advantages | Intellectual property |
| Pre-announcement info | Unreleased products, pending decisions | Business sensitivity |

**The test:** Before pasting something into AI chat, ask: *"Would I be comfortable if this appeared in a log file that got leaked?"* If no, don't paste it.

### Secrets Management

**The `.env` pattern:**

Keep secrets in environment variables, not in code or AI context.

```
project/
├── .env              ← Real secrets (NEVER committed, NEVER shown to AI)
├── .env.example      ← Template with dummy values (safe to commit)
├── .gitignore        ← Must include .env
└── script.py         ← References os.environ, not hardcoded values
```

**.env file:**
```
DB_PASSWORD=actual_secret_here
API_KEY=real_key_here
```

**.env.example file:**
```
DB_PASSWORD=your_password_here
API_KEY=your_api_key_here
```

**.gitignore must include:**
```
.env
*.pem
*.key
credentials.json
```

**When AI needs to work with code that uses secrets:**

✅ **Safe:**
```python
# Show AI this
password = os.environ.get('DB_PASSWORD')
```

❌ **Unsafe:**
```python
# Never show AI this
password = "actual_secret_123"
```

If AI generates code with placeholder secrets, replace them with environment variable references before committing.

### Work Environment: Local-Only Containment

Your work setup (local git, no GitHub sync) provides natural containment. But "local" doesn't mean "safe."

**What "local only" protects against:**
- Code/data leaking to public GitHub
- Sync across machines you don't control
- Exposure through GitHub's features (search, Copilot training, etc.)

**What "local only" does NOT protect against:**
- AI services receiving your prompts (Copilot sends code to GitHub/Azure)
- Screenshots or copy/paste out of the environment
- Local machine compromise
- Colleagues seeing your screen

**Work environment checklist:**

- [ ] Confirm: Is Copilot approved for use with company data? (Check IT policy)
- [ ] Understand: What data classification levels can you use with AI?
- [ ] Never: Paste customer data, credentials, or PII into Copilot
- [ ] Always: Use environment variables for any secrets
- [ ] Consider: Would your manager be comfortable with this in AI context?

**For your colleagues:** When you onboard them, make sure they understand that "local only" ≠ "private from AI services."

### Home Environment: GitHub Sync Awareness

Your home setup syncs to GitHub across 3 machines. This is convenient but requires more care.

**What syncs (and is visible to GitHub):**
- All committed code
- All committed config files (including `.github/copilot-instructions.md`)
- Commit messages and history
- Branch names

**What should NOT sync:**

```gitignore
# Secrets
.env
*.pem
*.key
credentials.json
secrets/

# Generated output (may contain processed data)
_output/

# Work in progress (may have debugging data)
_scratch/

# Large data files
*.csv
*.xlsx
data/

# Local-only config
.local/
```

**The `_scratch/` decision:**

You have a choice:
- **Sync `_scratch/`:** Experiments available on all machines, but anything sensitive you paste there goes to GitHub
- **Don't sync `_scratch/`:** Safer, but you lose work-in-progress when switching machines

**Recommendation:** Don't sync `_scratch/`. Use HANDOFF.md to capture state you need across machines.

### Data Handling Patterns

**Pattern 1: Sanitized examples**

When you need AI help with code that processes sensitive data:

```python
# Instead of real data:
# employees = pd.read_csv('real_employee_data.csv')

# Use synthetic example:
employees = pd.DataFrame({
    'id': ['E001', 'E002', 'E003'],
    'name': ['Alice Smith', 'Bob Jones', 'Carol White'],
    'department': ['Engineering', 'Sales', 'Engineering']
})
```

AI can help with the logic; you apply it to real data.

**Pattern 2: Structure, not content**

When discussing data problems:

✅ **Safe:** "I have a CSV with columns employee_id, department, training_date. How do I find duplicates?"

❌ **Unsafe:** "Here's my employee data: [pastes actual file contents]"

**Pattern 3: Redacted screenshots**

If you need to show AI an error or output:
1. Screenshot the relevant part
2. Redact any sensitive values (blur or black box)
3. Then share

**Pattern 4: Local-only data folders**

```
project/
├── data/              ← Gitignored, contains real data
├── data_sample/       ← Committed, contains synthetic examples
└── script.py          ← Works with either via config
```

### AI Tool-Specific Boundaries

**GitHub Copilot:**
- Sends code context to GitHub/Microsoft cloud for completions
- Your code *may* be used to improve Copilot (check your settings/organization policy)
- Copilot Chat has conversation history—don't paste secrets even in chat

**To check your Copilot data settings:**
VS Code → Settings → search "Copilot" → look for telemetry/data collection options

**Claude CLI:**
- Sends prompts to Anthropic's API
- Anthropic's data retention policies apply (check current policy)
- Files you reference are sent as context

**For both:**
- Assume anything you share could be logged
- Don't rely on "it probably won't leak" — assume it will

### Teaching Colleagues: The Security Briefing

When onboarding Process Controls team members, cover these points:

**The 5-minute security briefing:**

```markdown
# AI Security Basics

## Never put these in AI chat:
- Passwords, API keys, tokens
- Customer names or data
- Employee PII (SSNs, addresses)
- Internal server names/IPs

## Always do:
- Use .env files for secrets (never hardcode)
- Ask about structure, not content ("how do I process a CSV with these columns")
- Use synthetic/example data when showing AI your code

## Remember:
- "Local only" doesn't mean "private from AI" — your prompts go to the cloud
- When in doubt, ask: "Would I be comfortable if this leaked?"

## If you're unsure:
- Don't paste it — describe it instead
- Ask [your name] before using AI with sensitive data
```

### Incident Response: What If Something Slips?

If you accidentally paste sensitive data into AI:

1. **Don't panic** — but act quickly
2. **Stop the conversation** — don't continue; context may be cached
3. **Rotate credentials** — if you pasted passwords/keys, change them immediately
4. **Document it** — note what was exposed, when, which tool
5. **Report if required** — follow your company's incident process for work data
6. **Learn from it** — what led to the mistake? Can you add a safeguard?

**The reality:** Mistakes happen. A quick response limits damage. Pretending it didn't happen makes it worse.

### Boundary Checklist by Environment

**Work (Copilot, local only):**
- [ ] Confirmed AI usage is approved per company policy
- [ ] .env file exists and is gitignored
- [ ] No customer data in AI prompts
- [ ] No credentials hardcoded anywhere
- [ ] Colleagues briefed on security basics

**Home (Claude CLI, GitHub sync):**
- [ ] .gitignore excludes secrets, _scratch/, data files
- [ ] No work data in personal repos (keep them separate)
- [ ] Credentials use environment variables
- [ ] Sensitive experiments stay in _scratch/ (not synced)

### Questions Answered

| Question | Answer |
|----------|--------|
| Any specific security requirements at work? | Check with IT. At minimum: no customer data, no credentials, no PII in AI prompts. "Local only" doesn't mean private from AI services. |
| Strategy for separating sensitive work from AI-accessible content? | Use .env for secrets, describe structure instead of pasting content, use synthetic data for examples, keep real data in gitignored folders. |

---

## 12. Git & Multi-Machine Workflow

**Goal:** Stop the confusing git messages and sync smoothly across your home machines.

### Your Setup (It's Actually Fine)

Based on your screenshots, you have:

```
E:\Business\_Development\          ← Container folder (NOT a git repo)
├── .claude                        ← Claude CLI config
├── _Backups\
├── _Documentation\                ← Git repo → GitHub (home sync)
├── ControlsBMW\                   ← Git repo → GitHub
├── controls-docs\                 ← Git repo → GitHub
├── finances\                      ← Git repo → GitHub
└── healthassistant\               ← Git repo → GitHub
```

**This is 5 sibling repos, not nested.** That's correct. Your confusing messages are likely from multi-machine sync issues, not structural problems.

### Git Mental Model (Just Enough)

Think of git as three locations:

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Your Files     │     │  Local Git      │     │    GitHub       │
│  (working dir)  │ ──► │  (on your PC)   │ ──► │   (cloud)       │
│                 │     │                 │     │                 │
│ What you edit   │     │ Saved snapshots │     │ Shared between  │
│                 │     │                 │     │ your machines   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                       │                       │
        │      git add/commit   │      git push         │
        │─────────────────────►│──────────────────────►│
        │                       │                       │
        │                       │      git pull         │
        │◄──────────────────────────────────────────────│
```

**The key commands:**
- `git add .` → Stage your changes (prepare to save)
- `git commit -m "message"` → Save a snapshot locally
- `git push` → Upload to GitHub
- `git pull` → Download from GitHub

**The flow:**
1. Edit files
2. `git add .` + `git commit -m "what I did"`
3. `git push` (sends to GitHub)
4. On another machine: `git pull` (gets from GitHub)

### The Multi-Machine Workflow

**The #1 cause of confusion:** Forgetting to push or pull.

```
Machine A                          Machine B
─────────                          ─────────
Edit files                         
git commit                         
git push ───────► GitHub           
                                   git pull ◄─── GitHub
                                   Edit files
                                   git commit
                    GitHub ◄────── git push
git pull ◄───────                  
Edit files                         
...                                
```

**The rule:** Push before you leave, pull when you arrive.

**Before leaving a machine:**
```bash
git add .
git commit -m "WIP: describe what you were doing"
git push
```

**When arriving at a different machine:**
```bash
git pull
```
Then start working.

**If you forget:**
- Forgot to push? Your work is stuck on the other machine. Go back and push, or redo the work.
- Forgot to pull? You might create a conflict (see below).

### Common Confusing Messages (And What They Mean)

**"Your branch is ahead of 'origin/main' by X commits"**
```
Your branch is ahead of 'origin/main' by 3 commits.
  (use "git push" to publish your local commits)
```
**Translation:** You have commits that aren't on GitHub yet.
**Fix:** `git push`

---

**"Your branch is behind 'origin/main' by X commits"**
```
Your branch is behind 'origin/main' by 2 commits, and can be fast-forwarded.
  (use "git pull" to update your local branch)
```
**Translation:** GitHub has changes you don't have locally.
**Fix:** `git pull`

---

**"Your branch and 'origin/main' have diverged"**
```
Your branch and 'origin/main' have diverged,
and have 2 and 3 different commits each, respectively.
```
**Translation:** Both you AND GitHub have changes the other doesn't have. This happens when you forgot to pull before making changes.
**Fix:** 
```bash
git pull
# If there are conflicts, resolve them (see below)
git push
```

---

**"CONFLICT (content): Merge conflict in [file]"**
```
CONFLICT (content): Merge conflict in script.py
Automatic merge failed; fix conflicts and then commit the result.
```
**Translation:** You and another version (from your other machine) changed the same part of the same file.
**Fix:**
1. Open the file—look for `<<<<<<<`, `=======`, `>>>>>>>`
2. Edit to keep what you want, delete the markers
3. `git add [file]`
4. `git commit -m "Resolved merge conflict"`
5. `git push`

---

**"fatal: not a git repository"**
```
fatal: not a git repository (or any of the parent directories): .git
```
**Translation:** You're in a folder that isn't a git repo.
**Fix:** `cd` into the correct project folder. In your case, make sure you're in one of your 5 project folders, not in `_Development` itself.

---

**"Please commit your changes or stash them before you merge"**
```
error: Your local changes to the following files would be overwritten by merge:
        script.py
Please commit your changes or stash them before you merge.
```
**Translation:** You have uncommitted changes, and pulling would overwrite them.
**Fix:**
```bash
# Option A: Commit first
git add .
git commit -m "WIP"
git pull

# Option B: Stash temporarily
git stash
git pull
git stash pop   # brings your changes back
```

---

**"Updates were rejected because the remote contains work..."**
```
! [rejected]        main -> main (fetch first)
error: failed to push some refs to 'github.com:...'
hint: Updates were rejected because the remote contains work that you do
hint: not have locally.
```
**Translation:** GitHub has commits you don't have. You need to pull before you can push.
**Fix:**
```bash
git pull
# Resolve any conflicts if needed
git push
```

### The Daily Workflow Cheat Sheet

**Starting work on a machine:**
```bash
cd E:\Business\_Development\[project]
git pull
# Now work
```

**Ending work (before leaving machine):**
```bash
git add .
git commit -m "Describe what you did"
git push
```

**Quick status check:**
```bash
git status
```
This tells you:
- What files changed
- Whether you're ahead/behind GitHub
- What needs to be committed

### VS Code Git Integration

You don't have to use the command line. VS Code has built-in git:

**Bottom left corner:** Shows current branch

**Source Control panel (Ctrl+Shift+G):**
- See changed files
- Stage files (+ button)
- Commit (checkmark button)
- Push/Pull (... menu or sync button)

**The sync button (↑↓):** Does pull then push in one click.

**My recommendation:** Use the VS Code UI for daily stuff, but know the commands for when things go wrong.

### Your .claude at the Parent Level

You have `.claude` in `_Development`, not in individual projects:

```
_Development\
├── .claude          ← Claude CLI config HERE
├── _Documentation\
├── ControlsBMW\
└── ...
```

**Is this a problem?**

For git: No. Git doesn't care about `.claude`.

For Claude CLI: It might treat all 5 projects as one workspace. This could be:
- **Good:** Shared settings, Claude sees your whole development environment
- **Bad:** Claude might get confused about which project you're working in

**If you want per-project Claude config:**
```
_Development\
├── .claude                     ← Global/shared config
├── _Documentation\
│   └── CLAUDE.md              ← Project-specific instructions
├── ControlsBMW\
│   └── CLAUDE.md              ← Project-specific instructions
└── ...
```

Each project can have its own `CLAUDE.md` that adds project-specific context.

### Recovering from Common Messes

**"I made changes on Machine B but forgot I had unpushed changes on Machine A"**

This creates diverged branches. On whichever machine you're on:
```bash
git pull
# Resolve any conflicts
git add .
git commit -m "Merged changes from both machines"
git push
```

Then on the other machine: `git pull`

---

**"I want to undo my last commit"**

If you haven't pushed yet:
```bash
git reset --soft HEAD~1   # Undo commit, keep changes staged
```

If you already pushed—don't try to undo. Make a new commit that fixes it.

---

**"I accidentally committed a secret/password"**

If you haven't pushed: 
```bash
git reset --soft HEAD~1   # Undo commit
# Remove the secret from your files
git add .
git commit -m "Fixed"
```

If you already pushed: **Assume the secret is compromised.** Rotate the password/key immediately. Then you can clean up the git history (complicated) or just move forward (easier).

---

**"Everything is messed up and I just want to start fresh"**

Nuclear option (loses uncommitted work):
```bash
git fetch origin
git reset --hard origin/main
```

This makes your local copy exactly match GitHub. Use with caution.

### Workflow Summary

| Situation | Command |
|-----------|---------|
| Starting work | `git pull` |
| Saving work | `git add .` → `git commit -m "message"` |
| Sending to GitHub | `git push` |
| Check status | `git status` |
| See recent history | `git log --oneline -5` |
| Undo uncommitted changes | `git checkout -- [file]` |
| Resolve "diverged" | `git pull` → fix conflicts → `git push` |

**The golden rule:** Commit often, push before leaving, pull when arriving.

---

## Appendix: Open Questions & Research

### Configuration Mechanics
- [x] ~~Exactly how does Copilot's "X items" indicator work?~~ → Section 1: Files in `.github/instructions/` auto-load
- [x] ~~What's the hierarchy: user settings → workspace → repo → folder?~~ → Section 1: Additive, not override
- [ ] How do .github and .claude folders interact (if at all)? → They don't; separate tools

### Skills & Instructions
- [x] ~~Difference between a skill and an instruction file?~~ → Section 1: Skills are folders with multiple files; instructions are single .md files
- [x] ~~How to activate/deactivate skills per project?~~ → Section 1: Move out of `.github/instructions/` to deactivate
- [ ] Can you see token cost of loaded context? → No direct visibility; estimate by line count × ~8

### Token & Cost
- [ ] Where to see Copilot token usage breakdown? → Not available in consumer interface
- [x] ~~Can you set model defaults and override per-task?~~ → Section 5: Yes, manually via dropdown
- [x] ~~Best practices for staying within budget?~~ → Section 6: Reduce token tax, restart strategically

### Hooks
- [x] ~~Best hook framework for VS Code?~~ → Section 7: Git hooks for commits; no AI post-action hooks exist
- [ ] Can hooks call AI without burning main token budget? → Unknown; likely no
- [ ] Latency tolerance for AI-assisted hooks? → Not tested

### Research Sources
- [ ] GitHub Copilot documentation — For official config details
- [ ] Claude CLI documentation — For CLAUDE.md specifics
- [x] ~~Awesome Copilot repo~~ → Source of downloaded skills; caused the bloat problem

---

## Next Steps

**✅ Guide Writing Complete!**

All 13 sections are now written. Time to execute:

1. ~~**Audit current state**~~ ✅ — 13 references identified, Dataverse files confirmed as culprit
2. ~~**Establish folder template**~~ ✅ — Section 3 complete
3. ~~**Define model strategy**~~ ✅ — Section 5 complete
4. ~~**Implement one hook**~~ ✅ — Section 7, cleanup_check.py created
5. ~~**Add agents section**~~ ✅ — Section 10.6 complete
6. ~~**Explain MCP**~~ ✅ — Section 10 complete

**Action items to execute:**
- [ ] Move Dataverse files from `.github/instructions/` to `_reference/dataverse/`
- [ ] Slim `copilot-instructions.md` to <50 lines
- [ ] Run `claude mcp list` to see your 7 connected servers
- [ ] Verify "Used X references" decreases after file moves
- [ ] Test workflow with colleagues

---

*Last updated: January 29, 2025*
*Status: ✅ COMPLETE — All 14 sections written*
*Next: Execute cleanup actions (move Dataverse files, slim instructions, audit MCP)*
