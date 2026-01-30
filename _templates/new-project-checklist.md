# New Project Checklist

Quick setup guide for starting a new project in this workspace.

## 1. Create Project Folder

```powershell
cd C:\Users\GF99\Documentation
mkdir NewProjectName
cd NewProjectName
```

## 2. Copy Core Templates

```powershell
# From _templates/ folder:
cp ..\_templates\project-readme.md README.md
cp ..\_templates\project-handoff.md HANDOFF.md
cp ..\_templates\_TODO.md _TODO.md
```

## 3. Customize Core Files

- [ ] Edit `README.md` - Replace placeholders with project details
- [ ] Edit `HANDOFF.md` - Add initial project context
- [ ] Edit `_TODO.md` - Add first tasks

## 4. Create Standard Folders

```powershell
mkdir _scratch
# Optional (only if needed):
# mkdir _output
# mkdir _archive
```

## 5. Add Project-Specific Config (Optional)

Only if project needs custom Copilot rules:

```powershell
mkdir .github
cp ..\_templates\project-copilot-instructions.md .github\copilot-instructions.md
# Customize .github/copilot-instructions.md with project-specific context
```

## 6. Set Up Python Environment (If Needed)

If project requires different dependencies than workspace root:

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install [packages]
pip freeze > requirements.txt
```

**Note**: Most projects should use the workspace root `.venv`. Only create project-specific environment if dependencies conflict.

## 7. Update Workspace Documentation

- [ ] Add project to workspace README or main documentation
- [ ] Update `.gitignore` if project has special files to exclude

## 8. Initial Commit

```powershell
git add .
git commit -m "Initial project setup: [ProjectName]"
```

## Folder Structure Result

```
NewProjectName/
├── README.md              ← What this is (for humans)
├── HANDOFF.md             ← Current state (for AI)
├── _TODO.md               ← Tasks and ideas
├── .github/               ← Optional project-specific config
│   └── copilot-instructions.md
├── _scratch/              ← Experiments and WIP
├── _output/               ← Generated files (optional)
└── _archive/              ← Old versions (optional)
```

## Next Steps

1. Start coding your main script
2. Update `HANDOFF.md` as you make progress
3. Use `_scratch/` for experiments
4. Update `_TODO.md` as tasks evolve
5. Move production-ready files to project root
