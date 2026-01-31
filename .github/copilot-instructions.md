# GitHub Copilot Workspace Configuration

## Overview
Technical documentation workspace for industrial control systems with a focus on training management and process control documentation.

## Resources

**Skills** (`.github/skills/`): XLSX - Excel automation (auto-loaded)  
**Prompts** (`.github/prompts/`): Reusable templates for code review, optimization, documentation  
**Instructions** (`.github/instructions/`): Coding standards, best practices (auto-loaded by Copilot)  
**Reference** (`_reference/`): Specialized instructions and rarely-used skills (not auto-loaded)  
  - See [`_reference/README.md`](_reference/README.md) for full catalog

## Project-Specific Configuration

For workspace-specific rules, workflows, architecture details, and preferences, see [`.github/project-config.md`](.github/project-config.md).

**Key sections:**
- File naming conventions → [project-config.md#file-naming-conventions](.github/project-config.md#file-naming-conventions)
- Training system workflows
- Python environment setup

## Model Selection

Skills and prompts specify optimal models via frontmatter. Free models (GPT-4.1, GPT-5 mini) handle 80% of tasks. Premium models (Claude Sonnet 4.5) reserved for complex code. See [MODEL_COST_OPTIMIZATION.md](.github/MODEL_COST_OPTIMIZATION.md) for details.
