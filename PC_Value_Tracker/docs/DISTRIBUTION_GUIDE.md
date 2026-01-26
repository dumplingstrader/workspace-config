# PC Value Tracker V2.0 - Distribution Guide

**For package maintainers: How to create and distribute the portable zip package.**

**Version:** 2.0
**Updated:** January 2026

---

## Overview

This package is distributed as a portable zip file. Users extract it, run `setup_environment.ps1`, and they're ready to go. There is no remote Git repository.

**Distribution model:**
- Maintainer creates zip from master copy
- Zip is placed on shared network location
- Users download, extract, and run setup
- Local instances are disposable (users reimport fresh copies as needed)

---

## Creating the Distribution Zip

### What to INCLUDE

```
PC_Value_Tracker/
├── setup_environment.ps1       <- Required - sets up environment
├── README.md                   <- Required - user documentation
├── requirements.txt            <- Required - Python dependencies
|
├── scripts/                    <- Required - all Python scripts
│   ├── collect/
│   │   └── aggregate_weekly.py
│   ├── report/
│   │   ├── generate_monthly_summary.py
│   │   └── generate_stream_scorecard.py
│   └── util/
│       ├── create_quick_log_template.py
│       └── migrate_v1_to_v2.py
|
├── config/                     <- Required - configuration files
│   ├── streams.json            <- Stream definitions and keywords
│   └── settings.json
|
├── docs/                       <- Required - documentation
│   ├── METHODOLOGY.md
│   ├── QUICK_START.md
│   ├── STREAM_DEFINITIONS.md
│   ├── COPILOT_PROMPT.md
│   ├── COPILOT_PROMPT_AFTER_HOURS.md  <- For supervisors
│   ├── SUPERVISOR_BRIEFING.md
│   ├── DATA_MANAGEMENT.md
│   └── DISTRIBUTION_GUIDE.md
|
├── data/                       <- Include empty structure
│   └── raw/                    <- For weekly Copilot exports
|
├── output/                     <- Include empty structure
│   ├── monthly/
│   ├── quarterly/
│   └── scorecards/
|
├── templates/                  <- Include template files
│   ├── quick_log.xlsx
│   └── PC_Value_Template.xlsx
|
└── archive/                    <- Optional - V1.0 reference
    └── v1.0/
```

### What to EXCLUDE

| Item | Reason |
|------|--------|
| `.venv\` | Created by setup script - machine-specific |
| `.git\` | No remote repo - not needed |
| `__pycache__\` | Python cache - regenerated |
| `*.pyc` | Compiled Python - regenerated |
| `.claude\` | Claude Code settings - user-specific |

### Pilot Data INCLUDED (Examples for Recipients)

The distribution **includes pilot data** to serve as real-world examples:

| Item | Purpose |
|------|---------|
| `data\master.json` | 63 pilot records showing actual tracked issues |
| `data\raw\*.xlsx` | Example Copilot exports |
| `data\archive\` | Archived raw files demonstrating file management |
| `output\monthly\*.xlsx` | Example monthly reports |
| `output\quarterly\*.xlsx` | Example quarterly reports |

Recipients can review the pilot data to understand the system, then start their own tracking by adding new exports to `data\raw\`.

---

## PowerShell Script to Create Distribution Zip

Save this as `create_distribution.ps1` and run from the master project folder:

```powershell
# PC Value Tracker V2.0 - Create Distribution Zip
# Run from the master project folder

$timestamp = Get-Date -Format "yyyyMMdd"
$zipName = "PC_Value_Tracker_v2.0_$timestamp.zip"
$tempFolder = ".\dist_temp"

Write-Host "Creating distribution package: $zipName" -ForegroundColor Cyan

# Clean up temp folder if exists
if (Test-Path $tempFolder) {
    Remove-Item -Recurse -Force $tempFolder
}

# Create temp folder structure
New-Item -ItemType Directory -Path $tempFolder | Out-Null
New-Item -ItemType Directory -Path "$tempFolder\scripts\collect" | Out-Null
New-Item -ItemType Directory -Path "$tempFolder\scripts\report" | Out-Null
New-Item -ItemType Directory -Path "$tempFolder\scripts\util" | Out-Null
New-Item -ItemType Directory -Path "$tempFolder\config" | Out-Null
New-Item -ItemType Directory -Path "$tempFolder\docs" | Out-Null
New-Item -ItemType Directory -Path "$tempFolder\data\raw" | Out-Null
New-Item -ItemType Directory -Path "$tempFolder\output\monthly" | Out-Null
New-Item -ItemType Directory -Path "$tempFolder\output\quarterly" | Out-Null
New-Item -ItemType Directory -Path "$tempFolder\output\scorecards" | Out-Null
New-Item -ItemType Directory -Path "$tempFolder\templates" | Out-Null

# Copy root files
Copy-Item "setup_environment.ps1" $tempFolder
Copy-Item "README.md" $tempFolder
Copy-Item "requirements.txt" $tempFolder

# Copy scripts
Get-ChildItem "scripts\collect\*.py" -ErrorAction SilentlyContinue | Copy-Item -Destination "$tempFolder\scripts\collect\"
Get-ChildItem "scripts\report\*.py" -ErrorAction SilentlyContinue | Copy-Item -Destination "$tempFolder\scripts\report\"
Get-ChildItem "scripts\util\*.py" -ErrorAction SilentlyContinue | Copy-Item -Destination "$tempFolder\scripts\util\"

# Copy config
Copy-Item "config\*.json" "$tempFolder\config\"

# Copy docs
Get-ChildItem "docs\*.md" | Copy-Item -Destination "$tempFolder\docs\"

# Copy templates
Copy-Item "templates\*.xlsx" "$tempFolder\templates\" -ErrorAction SilentlyContinue

# Create zip
if (Test-Path $zipName) {
    Remove-Item $zipName
}

Compress-Archive -Path "$tempFolder\*" -DestinationPath $zipName

# Clean up
Remove-Item -Recurse -Force $tempFolder

Write-Host ""
Write-Host "Distribution package created: $zipName" -ForegroundColor Green
Write-Host ""
Write-Host "Contents:" -ForegroundColor Yellow
Write-Host "  - setup_environment.ps1 (run first)"
Write-Host "  - README.md (user guide)"
Write-Host "  - scripts\ (collect, report, util)"
Write-Host "  - config\ (streams.json)"
Write-Host "  - docs\ (all documentation)"
Write-Host "  - data\master.json (pilot data - 63 records)"
Write-Host "  - data\raw\ (pilot raw files)"
Write-Host "  - data\archive\ (archived files)"
Write-Host "  - output\ (example reports)"
Write-Host ""
Write-Host "Included pilot data as examples for recipients." -ForegroundColor Cyan
Write-Host "Upload to shared network location for distribution." -ForegroundColor Magenta
```

---

## Manual Zip Creation (Alternative)

If you prefer to create the zip manually:

### Step 1: Clean the project folder
```powershell
# Remove items that shouldn't be distributed
Remove-Item -Recurse -Force .venv -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force .git -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force .claude -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force __pycache__ -ErrorAction SilentlyContinue
Get-ChildItem -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force

# Note: Pilot data (master.json, raw files, outputs) stays in the zip as examples
```

### Step 2: Create zip
```powershell
Compress-Archive -Path * -DestinationPath PC_Value_Tracker_v2.0.zip
```

### Step 3: Restore your master copy
If you cleaned the master copy, restore from backup or Git.

---

## Version Management

Since there's no remote Git repository, version management is manual:

### Version Numbering
- Use semantic versioning: `v2.0`, `v2.1`, `v3.0`
- Include date in zip filename: `PC_Value_Tracker_v2.0_20260124.zip`

### Changelog
Maintain a simple changelog in the README:

```markdown
## Version History

### V2.0 (January 2026)
- Complete redesign: 5-stream model
- Simplified schema (6 core fields)
- Unified Copilot prompt
- Stream-specific scorecards

### V1.0 (January 2026)
- Initial implementation
- Archived in archive/v1.0/
```

### Announcing Updates
When distributing a new version:
1. Place new zip on shared network
2. Email/message team with version number and changes
3. Include reminder to backup `data/` folder before updating

---

## Shared Network Location

Recommended folder structure on shared drive:

```
\\server\shared\PC_Value_Tracker\
├── LATEST\
│   └── PC_Value_Tracker_v2.0_20260124.zip    <- Current version
├── ARCHIVE\
│   └── PC_Value_Tracker_v1.0_20260115.zip
└── README.txt                                 <- Brief instructions
```

**README.txt content:**
```
PC Value Tracker V2.0 - Portable Distribution
=============================================

1. Download the zip from LATEST\ folder
2. Extract to your Documents folder
3. Open folder in VSCode or PowerShell
4. Run: .\setup_environment.ps1
5. See README.md for usage instructions

Questions? Contact Tony Chiu
```

---

## Troubleshooting Distribution Issues

### Users report "Python not found"
They need to install Python with "Add to PATH" checked. Include this in communications.

### Users report "Execution policy" errors
They need to run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Zip is too large
Check that you excluded:
- `.venv\` (can be 200MB+)
- `.git\` (can be large with history)
- `data\master.json` (user's data)

Expected zip size: **~100KB - 500KB** (scripts and docs only)

### Users lose data after update
Remind users to backup `data/` folder before deleting old version.

---

## Quick Reference

### Create distribution zip:
```powershell
.\create_distribution.ps1
```

### Test zip before distribution:
1. Extract to a test folder
2. Run `.\setup_environment.ps1`
3. Verify scripts work: `python scripts/report/generate_monthly_summary.py --help`

### What users need to know:
1. Extract zip
2. Run `.\setup_environment.ps1`
3. Backup `data/` folder before updating

---

*V2.0 - Less tracking, more changing.*
