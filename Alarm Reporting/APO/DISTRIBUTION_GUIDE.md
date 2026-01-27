# Distribution Package Guide

**Created**: January 27, 2026  
**Updated**: January 27, 2026 (Separated utilities)  
**Scripts**: `organize_files.ps1` (file organization), `create_distribution_package.ps1` (packaging)

---

## Overview

The project uses **two separate utilities** for better reusability:

1. **`organize_files.ps1`** - Organizes APO files into logical structure (project-specific)
2. **`create_distribution_package.ps1`** - Creates timestamped ZIP packages (generic/reusable)

See [UTILITY_USAGE_GUIDE.md](UTILITY_USAGE_GUIDE.md) for complete usage documentation.

---

## Quick Start

### First-Time Setup: Organize Files
```powershell
# Run once to create folder structure and organize files
.\organize_files.ps1
```

### Create Distribution Package
```powershell
# Create ZIP package (auto-detects all content)
.\create_distribution_package.ps1

# Custom package name
.\create_distribution_package.ps1 -PackageName "ACM_to_APO_Migration"

# Include only specific items
.\create_distribution_package.ps1 -ItemsToInclude @("1_Deliverables", "PROJECT_HANDOFF_SUMMARY.md")
```

### Re-package After Updates
```powershell
# No need to re-organize - just create new package
.\create_distribution_package.ps1
```

---

## Organized Folder Structure

### 1_Deliverables/
**Ready-to-distribute final outputs**

#### Conference_Submission/
- `Executive_Summary_Conference_Submission.txt` - Conference website submission (1097 chars)
- `Presentation_Outline_Conference.md` - 20 slides, 50-minute presentation
- `Presentation_Outline_Conference.docx` - Word version
- `DynAMo Standard Sync and Alternative Active Sync v3.2.pptx` - Technical presentation

#### Whitepaper/
- `ACM_to_APO_Migration_Whitepaper_Outline.md` - **PRIMARY MASTER FILE**
- `ACM_to_APO_Migration_Whitepaper_Outline.docx` - Word version for distribution

#### Checklist/
- `ACM_to_APO_Migration_Comprehensive_Checklist.xlsx` - 250+ tasks, 11 sheets
- `CHECKLIST_CREATION_SUMMARY.md` - How it was created
- `CHECKLIST_CREATION_SUMMARY.pdf` - PDF version

### 2_Source_Documents/
**Working versions and feedback**

#### Working_Versions/
- `APO_Deployment_Workflow_Checklist.xlsx` - Barbara's original workflow

#### Barbara_Feedback/
- `ACM_to_APO_Migration_Whitepaper_Outline_BKS edits.docx` - 40+ changes tracked
- `Potential additions to the Standard HAM delivery (Barbara Schubert).docx` - Enhancement proposals

### 3_Reference_Materials/
**Supporting documentation**

#### Honeywell_Documentation/
- `Alarm Performance Optimizer Configuration Guide.pdf`
- `Alarm Performance Optimizer Installation Guide.pdf`
- `GuardianNewsletterQ32025.pdf`

#### Industry_Standards/
- `honeywell-alarm-management-standards-whitepaper.pdf` - ISA 18.2, EEMUA 191

#### Case_Studies/
- `MPC APO Deployment Cookbook.docx` - Marathon internal best practices
- `O-791428_ APO training.docx` - Training materials
- `SuccessStory_IrvingOil_AlarmManagement1.pdf` - Success story

### 4_Scripts_Tools/
**Python automation**

- `create_comprehensive_checklist_v2.py` - **PRIMARY GENERATOR** (current version)
- `create_comprehensive_checklist.py` - Original version (v1)
- `read_checklist.py` - Excel validation utility

**Usage**:
```powershell
python create_comprehensive_checklist_v2.py
```

### 5_Archive/
**Historical content**

#### Extracted_Text/
- `BKS_edits_extracted.txt` - Text from Barbara's tracked changes
- `PPTX_extracted.txt` - Extracted PowerPoint content

---

## Distribution Package Contents

When you run the script, it creates a ZIP file with this structure:

```
ACM_to_APO_Migration_Package_YYYYMMDD_HHMMSS.zip
├── README.txt (auto-generated package guide)
├── PROJECT_HANDOFF_SUMMARY.md
├── APO_Documentation_Analysis_Summary.md
├── image/ (folder with screenshots/diagrams)
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

---

## Use Cases

### 1. Conference Submission Package
**For**: Honeywell Users Conference 2026 website upload

**Steps**:
1. Run script to organize files
2. Navigate to `1_Deliverables/Conference_Submission/`
3. Submit `Executive_Summary_Conference_Submission.txt` via conference website
4. Keep presentation files for later slide development

**Key files**:
- Executive summary (ready for copy/paste)
- Presentation outline (20 slides with speaker notes)
- DynAMo presentation (Alternative Active Sync technical deep-dive)

### 2. Client Delivery Package
**For**: Sending migration guidance to Marathon sites or external clients

**Steps**:
1. Run full script (organize + ZIP)
2. Locate ZIP in `Distribution/` folder
3. Send via secure file transfer or Teams/SharePoint

**What client gets**:
- Complete checklist (250+ tasks)
- Migration whitepaper outline
- Reference documentation
- Python tools for customization

### 3. Internal Team Handoff
**For**: Transferring project to another team member

**Steps**:
1. Run full script
2. Include ZIP + `PROJECT_HANDOFF_SUMMARY.md` in handoff email
3. Point to key documents in README.txt

**What they need to know**:
- Primary master file location
- Python scripts for regeneration
- Barbara's feedback integration history

### 4. Archive/Milestone Snapshot
**For**: Version control or project milestone documentation

**Steps**:
1. Run script before major changes
2. Store ZIP with version tag (e.g., `_v1.0_ConferenceReady`)
3. Keep in archive folder or SharePoint

**When to snapshot**:
- Before conference submission
- After major whitepaper edits
- Before client delivery
- End of project phase

---

## Regenerating Checklist After Changes

If whitepaper outline is updated and checklist needs regeneration:

```powershell
# 1. Navigate to APO folder
cd "C:\Users\GF99\Documentation\Alarm Reporting\APO"

# 2. Activate Python environment (if needed)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3. Install dependencies (first time only)
pip install pandas openpyxl

# 4. Run generator
python 4_Scripts_Tools\create_comprehensive_checklist_v2.py

# 5. Checklist updates in place
# Location: 1_Deliverables\Checklist\ACM_to_APO_Migration_Comprehensive_Checklist.xlsx
```

---

## Customization

### Adding Files to Package

Edit `$FileMapping` hashtable in `create_distribution_package.ps1`:

```powershell
$FileMapping = @{
    # Add new file
    "NewDocument.pdf" = "1_Deliverables\Conference_Submission"
    # File will be moved during organization
}
```

### Changing Folder Names

Edit `$FolderStructure` hashtable:

```powershell
$FolderStructure = @{
    "1_Deliverables" = @(
        "Conference_Submission",
        "Whitepaper",
        "Checklist",
        "NewSubfolder"  # Add subfolder
    )
}
```

### Excluding Files from ZIP

Edit `$ItemsToZip` array:

```powershell
$ItemsToZip = @(
    "1_Deliverables",
    "2_Source_Documents",
    # Comment out to exclude:
    # "5_Archive",
)
```

---

## Troubleshooting

### "File in use" errors
**Solution**: Close Excel/Word before running script. Script will skip locked files.

### ZIP not created
**Solution**: Check `Distribution/` folder exists and you have write permissions.

### Files not moving
**Solution**: Ensure file names match exactly (check for typos in `$FileMapping`).

### Python scripts fail
**Solution**: Ensure Python 3.x installed and dependencies (`pandas`, `openpyxl`) are available.

---

## Best Practices

1. **Before external distribution**: Review ZIP contents to ensure no sensitive internal data
2. **Version control**: Include date/version in filename when manually distributing
3. **Test extraction**: Unzip package in temp location to verify structure
4. **Document changes**: Update `PROJECT_HANDOFF_SUMMARY.md` when making major changes
5. **Backup originals**: Keep unorganized backup before first run (one-time safety)

---

## Script Options Reference

| Parameter | Description | Example |
|-----------|-------------|---------|
| None | Full process (organize + ZIP) | `.\create_distribution_package.ps1` |
| `-OrganizeOnly` | Only organize files, no ZIP | `.\create_distribution_package.ps1 -OrganizeOnly` |
| `-ZipOnly` | Only create ZIP (assumes organized) | `.\create_distribution_package.ps1 -ZipOnly` |
| `-OutputPath` | Custom output location | `.\create_distribution_package.ps1 -OutputPath "C:\Distributions"` |

---

## Next Steps After Organization

1. ✅ Files organized into logical structure
2. ✅ Distribution package created with README
3. 📝 Update PROJECT_HANDOFF_SUMMARY.md with new structure
4. 🎯 Use `1_Deliverables/Conference_Submission/` for conference upload
5. 📦 Share ZIP package with stakeholders
6. 🔄 Re-run script anytime to create fresh package

---

**Questions?** See `PROJECT_HANDOFF_SUMMARY.md` for full project context and contact information.
