# Reference Instructions (On-Demand)

Specialized instruction files and rarely-used skills for occasional use. These are **not auto-loaded** by GitHub Copilot to reduce token usage. Reference them explicitly when needed.

## Skills (Document Processing)

These skills were moved from `.github/skills/` to reduce token consumption. They are loaded only when explicitly requested.

- **docx-skill/** - Word document creation, editing, tracked changes, and comments
- **pdf-skill/** - PDF manipulation, form filling, text/table extraction  
- **pptx-skill/** - PowerPoint presentation creation and editing

**Usage:** Explicitly reference when needed:
```
"Use the pptx skill from _reference/pptx-skill/ to create a presentation"
"Load the docx skill from _reference/docx-skill/ and help me edit this document"
```

**Note:** The XLSX skill remains in `.github/skills/xlsx/` and auto-loads due to frequent use across multiple projects.

## AI & Copilot Framework
- `agent-skills.instructions.md` - Guidelines for creating GitHub Copilot skills
- `agents.instructions.md` - Custom agent file creation guidelines
- `ai-prompt-engineering-safety-best-practices.instructions.md` - Prompt engineering and responsible AI
- `prompt.instructions.md` - Creating high-quality prompt files
- `tasksync.instructions.md` - TaskSync V4 terminal-based task management protocol

## Python - Dataverse SDK
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

## Other Languages
- `java.instructions.md` - Java application development guidelines

## Workflow & Documentation
- `task-implementation.instructions.md` - Task plans with progressive tracking
- `update-code-from-shorthand.instructions.md` - Shorthand code expansion
- `update-docs-on-code-change.instructions.md` - Auto-update documentation

## Usage

To use these instructions, explicitly reference them in your request:
```
"Use the instructions from _reference/dataverse-python.instructions.md to..."
```

Or ask Copilot to read them:
```
"Read _reference/agent-skills.instructions.md and help me create a new skill"
```
