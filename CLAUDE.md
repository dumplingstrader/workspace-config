# E:\_Development — AI Workspace

## Workspace Index

| Repo | Purpose |
|------|---------|
| `ControlsBMW/` | Controls engineering social media persona and content system |
| `controls-docs/` | Controls engineering documentation and knowledge base |
| `finances/` | Coin portfolio CLI tool (Python + SQLite + Click) |
| `healthassistant/` | Personal health tracking app (React + FastAPI) |
| `Documentation/` | Work-related documentation and project templates (exported from work laptop) |

## Shared Workspace Resources

| Path | Purpose |
|------|---------|
| `.claude/skills/` | 16 Claude skills (shared across all projects) |
| `.claude/template/` | Skill template for creating new skills |
| `resource-tools/` | AI resource indexer — 288 resources (skills, agents, prompts) with 94.9% token savings |
| `_reference/` | Reference material: awesome-copilot collection, archived skills, Copilot docs |
| `_scripts/` | Workspace-level utility scripts |
| `_templates/` | Project templates |
| `bootstrap_core_three.ps1` | Automated Core Three file creation for new projects |
| `cleanup_check.py` | File organization + unused imports detection |

## Shared Conventions

### Directory Conventions
- `_scratch/` — Work-in-progress, temporary files, experiments
- `_output/` — Generated files (reports, exports, builds)
- `_archive/` — Old/superseded files kept for reference
- `_reference/` — Reference material, third-party docs, archived resources

### Core Three Files (Required in Every Project)
Every project root must have:
1. **README.md** — What the project is, how to run it, folder structure
2. **HANDOFF.md** — AI context restoration document (current state, blockers, next steps). For AI session continuity, not human notes. Keep under 200 lines.
3. **_TODO.md** — Task tracking with sections: Tasks, Ideas, Parking Lot

### CLAUDE.md (Per-Project)
Each repo also has a `CLAUDE.md` with project-specific context for Claude: tech stack, key commands, folder layout, and conventions unique to that project.

## File Naming Conventions
- Python scripts: `verb_noun.py` (e.g., `build_index.py`, `check_ingredients.py`)
- Folders: `lowercase-hyphens` (e.g., `resource-tools`, `knowledge-bases`)
- Documentation: `UPPER_CASE.md` for root-level docs, `lowercase-hyphens.md` for nested docs

## Session Habit
Before closing any session, update the project's `HANDOFF.md` with:
- What was accomplished
- Current blockers or open questions
- What to do next
