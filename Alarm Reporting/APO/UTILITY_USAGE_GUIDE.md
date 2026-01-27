# APO Project Utilities - Usage Guide

## Overview

The project now uses **two separate utilities** for different tasks:

1. **`organize_files.ps1`** - Organizes files into logical folder structure (project-specific)
2. **`create_distribution_package.ps1`** - Creates timestamped ZIP packages (reusable/generic)

## Separation Benefits

- **Reusability**: Distribution script can be copied to any project folder
- **Flexibility**: Organize files once, create packages multiple times
- **Maintainability**: Each utility has a single, clear responsibility
- **Portability**: Distribution script works with any folder structure

---

## 1. File Organization (`organize_files.ps1`)

### Purpose
Organizes APO project files into a structured folder hierarchy for better project management.

### When to Use
- When starting fresh with unorganized files
- After receiving new documents that need proper placement
- One-time setup to establish project structure

### Usage

```powershell
# Run file organization
.\organize_files.ps1
```

### What It Does
Creates folder structure and moves files to appropriate locations:

```
APO/
├── 1_Deliverables/
│   ├── Conference_Submission/
│   ├── Whitepaper/
│   └── Checklist/
├── 2_Source_Documents/
│   ├── Working_Versions/
│   └── Barbara_Feedback/
├── 3_Reference_Materials/
│   ├── Honeywell_Documentation/
│   ├── Industry_Standards/
│   └── Case_Studies/
├── 4_Scripts_Tools/
└── 5_Archive/
    └── Extracted_Text/
```

### Customization
Edit the `$FileMapping` hashtable in the script to add/modify file placements.

---

## 2. Distribution Package Creator (`create_distribution_package.ps1`)

### Purpose
Generic utility to create timestamped ZIP packages from any folder. **Can be reused in other projects.**

### When to Use
- Creating release packages for distribution
- Archiving project snapshots
- Sharing project contents with stakeholders
- **Any project that needs ZIP distribution packages**

### Usage

#### Basic Usage (Auto-detect everything)
```powershell
# Create package from current folder
.\create_distribution_package.ps1

# Creates: APO_20260127_143022.zip (using folder name + timestamp)
```

#### Custom Package Name
```powershell
# Specify custom package name
.\create_distribution_package.ps1 -PackageName "ACM_to_APO_Migration"

# Creates: ACM_to_APO_Migration_20260127_143022.zip
```

#### Specific Items Only
```powershell
# Include only specific folders/files
.\create_distribution_package.ps1 -ItemsToInclude @(
    "1_Deliverables",
    "4_Scripts_Tools",
    "PROJECT_HANDOFF_SUMMARY.md",
    "README.md"
)
```

#### Custom Output Location
```powershell
# Output to different directory
.\create_distribution_package.ps1 -OutputPath "C:\Releases"
```

#### Custom README Content
```powershell
# Provide custom README for the package
$readme = @"
# My Custom Project Package
This package contains...
"@

.\create_distribution_package.ps1 -ReadmeContent $readme
```

### What It Does

1. **Auto-detects** items to include (excludes `.venv`, `.git`, `Distribution`, etc.)
2. **Stages** files to temporary directory
3. **Creates** README.txt (default or custom)
4. **Compresses** to timestamped ZIP
5. **Cleans up** staging directory

### Auto-Excluded Items

The script automatically excludes:
- `Distribution/` (output folder)
- `.venv/` (Python virtual environment)
- `.git/` (version control)
- `.github/` (GitHub config)
- `__pycache__/` (Python cache)
- `*.pyc` (compiled Python)
- `.env` (environment variables)
- `.vs/` (Visual Studio)
- `node_modules/` (Node.js)
- `staging_temp/` (temporary staging)

---

## Typical Workflow

### Initial Setup
```powershell
# 1. Organize files into structure (one-time)
.\organize_files.ps1

# 2. Verify folder structure looks correct
```

### Create Distribution Package
```powershell
# 3. Create distribution package
.\create_distribution_package.ps1

# Output: Distribution/APO_20260127_143022.zip
```

### Update and Re-package
```powershell
# 4. Make changes to files...

# 5. Create new package (no re-organization needed)
.\create_distribution_package.ps1

# Output: Distribution/APO_20260127_151545.zip (new timestamp)
```

---

## Using Distribution Script in Other Projects

### Copy to New Project

```powershell
# 1. Copy script to your project folder
Copy-Item ".\create_distribution_package.ps1" "C:\MyOtherProject\"

# 2. Navigate to project
cd "C:\MyOtherProject"

# 3. Create package (uses folder name automatically)
.\create_distribution_package.ps1

# Creates: MyOtherProject_20260127_160000.zip
```

### Example: Training Folder

```powershell
cd "C:\Users\GF99\Documentation\Training"

# Create distribution package with custom name
.\create_distribution_package.ps1 -PackageName "Training_Tracker_Release"

# Output: Distribution/Training_Tracker_Release_20260127_160000.zip
```

### Example: SpendTracker

```powershell
cd "C:\Users\GF99\Documentation\SpendTracker"

# Include only specific items
.\create_distribution_package.ps1 `
    -PackageName "SpendTracker_v1.0" `
    -ItemsToInclude @("scripts", "templates", "docs", "QUICK_START.txt", "requirements.txt")

# Output: Distribution/SpendTracker_v1.0_20260127_160000.zip
```

---

## Parameters Reference

### `create_distribution_package.ps1`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `-OutputPath` | string | `.\Distribution` | Where to create ZIP files |
| `-PackageName` | string | (folder name) | Base name for ZIP file |
| `-ItemsToInclude` | string[] | (auto-detect) | Specific items to include |
| `-ReadmeContent` | string | (auto-generated) | Custom README text |

---

## Output Structure

### Distribution Folder
```
Distribution/
├── APO_20260127_143022.zip
├── APO_20260127_151545.zip
└── APO_20260127_160000.zip
```

### Inside Each ZIP
```
APO_20260127_143022.zip
├── 1_Deliverables/
├── 2_Source_Documents/
├── 3_Reference_Materials/
├── 4_Scripts_Tools/
├── 5_Archive/
├── README.txt (auto-generated)
└── (all other files/folders)
```

---

## Troubleshooting

### "File in use" errors
Close Excel/Word files before running organization script.

### Large package size
Use `-ItemsToInclude` to exclude large reference materials:
```powershell
.\create_distribution_package.ps1 -ItemsToInclude @(
    "1_Deliverables",
    "4_Scripts_Tools",
    "PROJECT_HANDOFF_SUMMARY.md"
)
```

### Custom README not appearing
Ensure `-ReadmeContent` is a valid string (use here-strings for multi-line):
```powershell
$readme = @"
Line 1
Line 2
"@
```

---

## Best Practices

1. **Organize once** - Run `organize_files.ps1` only when setting up structure
2. **Package often** - Create new distribution packages as needed without re-organizing
3. **Version control** - Keep Distribution/ folder in `.gitignore`
4. **Test packages** - Extract and verify ZIP contents before external distribution
5. **Custom names** - Use meaningful package names for releases (`-PackageName`)
6. **Selective packaging** - Use `-ItemsToInclude` for client-specific distributions

---

## Examples

### Full APO Package
```powershell
.\create_distribution_package.ps1 -PackageName "ACM_to_APO_Migration_Complete"
```

### Deliverables Only
```powershell
.\create_distribution_package.ps1 `
    -PackageName "ACM_to_APO_Deliverables" `
    -ItemsToInclude @("1_Deliverables", "PROJECT_HANDOFF_SUMMARY.md")
```

### Scripts and Tools
```powershell
.\create_distribution_package.ps1 `
    -PackageName "APO_Automation_Tools" `
    -ItemsToInclude @("4_Scripts_Tools", "DISTRIBUTION_GUIDE.md")
```

---

## Migration from Old Script

**Old approach** (combined script):
```powershell
.\create_distribution_package.ps1 -ZipOnly  # Skip organization
```

**New approach** (separated utilities):
```powershell
# Organize once
.\organize_files.ps1

# Package as needed (organization step removed)
.\create_distribution_package.ps1
```

**Benefits of separation**:
- Distribution script is now reusable across projects
- Clearer separation of concerns
- More flexible parameterization
- Easier to maintain and extend

---

**Last Updated**: January 27, 2026  
**Script Versions**: organize_files.ps1 (v1.0), create_distribution_package.ps1 (v2.0)
