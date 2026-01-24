# Manual Setup Guide (Non-Docker)

This guide is for setting up the PC Value Tracker on a new machine **without Docker**. Perfect for when Docker won't install or you prefer a traditional Python setup.

---

## Prerequisites

- **Windows 10/11** (or macOS/Linux with minor path adjustments)
- **Python 3.10+** - [Download from python.org](https://www.python.org/downloads/)
  - ⚠️ During installation: **Check "Add Python to PATH"**
- **Git** (optional, for version control) - [Download from git-scm.com](https://git-scm.com/)

---

## Quick Setup (Automated)

### Windows PowerShell

1. **Extract project** to your desired location (e.g., `C:\Projects\PC_Value_Tracker\`)

2. **Open PowerShell** in project directory:
   ```powershell
   cd C:\Projects\PC_Value_Tracker
   ```

3. **Run setup script**:
   ```powershell
   .\setup_environment.ps1
   ```

   This will:
   - ✅ Check Python version (needs 3.10+)
   - ✅ Create virtual environment (`.venv`)
   - ✅ Install all dependencies from `requirements.txt`
   - ✅ Verify packages installed correctly
   - ✅ Create output directories

4. **Place your data**:
   - Copy `master_combined.json` to `data/` directory

5. **Test scripts**:
   ```powershell
   .\.venv\Scripts\python.exe scripts\generate_monthly_report.py --help
   ```

---

## Manual Setup (Step-by-Step)

If the automated script fails or you prefer manual control:

### 1. Verify Python Installation

```powershell
python --version
```

Should show: `Python 3.10.x` or higher. If not:
- Download from [python.org](https://www.python.org/downloads/)
- **Important**: Check "Add Python to PATH" during installation
- Restart PowerShell after installation

### 2. Create Virtual Environment

```powershell
# Navigate to project directory
cd C:\Projects\PC_Value_Tracker

# Create virtual environment
python -m venv .venv

# Activate it
.\.venv\Scripts\activate
```

You should see `(.venv)` appear in your prompt.

### 3. Install Dependencies

```powershell
# Upgrade pip first
python -m pip install --upgrade pip

# Install required packages
pip install -r requirements.txt
```

**What gets installed:**
- `pandas>=1.5.0` - Data manipulation
- `openpyxl>=3.0.0` - Excel file generation
- `python-pptx>=0.6.21` - PowerPoint generation
- `matplotlib>=3.5.0` - Charts (optional)
- `seaborn>=0.12.0` - Visualization (optional)

### 4. Verify Installation

```powershell
python -c "import pandas; print('pandas:', pandas.__version__)"
python -c "import openpyxl; print('openpyxl:', openpyxl.__version__)"
python -c "import pptx; print('python-pptx:', pptx.__version__)"
```

All should print version numbers without errors.

### 5. Create Output Directories

```powershell
New-Item -ItemType Directory -Force -Path data
New-Item -ItemType Directory -Force -Path output
New-Item -ItemType Directory -Force -Path templates
New-Item -ItemType Directory -Force -Path submissions
```

### 6. Place Your Data

Copy `master_combined.json` from your old machine to `data/` directory.

---

## Running Scripts

### Activate Environment (Required Each Session)

Every time you open a new PowerShell window:

```powershell
cd C:\Projects\PC_Value_Tracker
.\.venv\Scripts\activate
```

### Generate Monthly Report

```powershell
# Using virtual environment Python
.\.venv\Scripts\python.exe scripts\generate_monthly_report.py --month 2026-01

# Or if environment activated:
python scripts\generate_monthly_report.py --month 2026-01
```

Output: `output/Monthly_Report_2026-01.xlsx`

### Generate Quarterly Report

```powershell
.\.venv\Scripts\python.exe scripts\generate_quarterly_report.py --quarter 2025-Q4
```

Output: `output/Quarterly_Report_2025-Q4.xlsx`

### Create Leadership Presentation (Blank Template)

```powershell
.\.venv\Scripts\python.exe scripts\create_leadership_presentation_template.py
```

Output: `templates/Leadership_Presentation_Template.pptx`

### Create Auto-Filled Presentation

```powershell
.\.venv\Scripts\python.exe scripts\create_leadership_presentation_template.py `
  --quarter 2025-Q4 `
  --input data\master_combined.json `
  --output output\Q4_2025_Presentation.pptx
```

Output: `output/Q4_2025_Presentation.pptx` with Q4 2025 data

---

## Transferring from Another Machine

### Option 1: Zip File Transfer (Simplest)

**On old machine:**
1. **DO NOT** include `.venv/` (it's machine-specific)
2. Create archive:
   ```powershell
   # Exclude virtual environment
   Compress-Archive -Path * -DestinationPath PC_Value_Tracker_Transfer.zip -Exclude .venv
   ```
3. Transfer `PC_Value_Tracker_Transfer.zip` to new machine (USB, cloud, network share)

**On new machine:**
1. Extract archive
2. Run `.\setup_environment.ps1` to rebuild environment
3. Place `master_combined.json` in `data/`

### Option 2: Git Repository (Best for Version Control)

**On old machine (if not already using git):**
```powershell
git init
git add .
git commit -m "Initial commit - PC Value Tracker"
git remote add origin <your-git-url>
git push -u origin main
```

**On new machine:**
```powershell
git clone <your-git-url>
cd PC_Value_Tracker
.\setup_environment.ps1
```

Place `master_combined.json` in `data/` (don't commit data files with sensitive info)

### Option 3: Direct File Copy

Copy entire project folder to USB drive or network share:
- **Include:** All `.py`, `.md`, `.txt`, `.json`, `config/`, `scripts/`, `docs/`
- **Exclude:** `.venv/` (rebuild on new machine), `output/` (temporary), `.git/` (unless using git)

On new machine, run `.\setup_environment.ps1` to rebuild environment.

---

## Troubleshooting

### Python Not Found

**Symptom:** `python: command not found` or `python is not recognized`

**Solution:**
1. Install Python from [python.org](https://www.python.org/downloads/)
2. During installation, **check "Add Python to PATH"**
3. Restart PowerShell
4. Verify: `python --version`

### pip Not Found

**Symptom:** `pip: command not found`

**Solution:**
```powershell
python -m ensurepip --upgrade
```

### Package Installation Fails

**Symptom:** `ERROR: Could not install packages` or `Failed building wheel`

**Solution:**
1. Upgrade pip: `python -m pip install --upgrade pip`
2. Try individual packages:
   ```powershell
   pip install pandas
   pip install openpyxl
   pip install python-pptx
   ```
3. Check internet connection (pip needs to download packages)

### Scripts Generate Empty Output

**Symptom:** Excel/PowerPoint files created but no data

**Solution:**
1. Verify `master_combined.json` is in `data/` directory
2. Check JSON format:
   ```powershell
   python -c "import json; json.load(open('data/master_combined.json'))"
   ```
3. Run with debugging:
   ```powershell
   python scripts\generate_monthly_report.py --month 2026-01 --debug
   ```

### Virtual Environment Activation Fails

**Symptom:** `.\.venv\Scripts\activate` does nothing or shows error

**Solution:**
1. **PowerShell execution policy issue:**
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
2. Then retry: `.\.venv\Scripts\activate`

### Wrong Python Version

**Symptom:** Script fails with syntax errors or import errors

**Solution:**
1. Check version in virtual environment:
   ```powershell
   .\.venv\Scripts\python.exe --version
   ```
2. If wrong, delete `.venv` and recreate:
   ```powershell
   Remove-Item -Recurse -Force .venv
   python -m venv .venv
   .\.venv\Scripts\activate
   pip install -r requirements.txt
   ```

---

## Differences from Docker Setup

| Aspect | Docker | Manual Setup |
|--------|--------|--------------|
| **Setup Time** | 5-10 min (if Docker works) | 3-5 min (always works) |
| **Consistency** | 100% identical everywhere | Varies by Python version |
| **Isolation** | Fully isolated container | Shares system Python |
| **Transfer** | Export/import images | Copy files + rebuild venv |
| **Debugging** | Harder (inside container) | Easier (native environment) |
| **Requirements** | Docker Desktop (200MB+) | Just Python (50MB) |

**When to use Manual Setup:**
- ✅ Docker won't install (corporate restrictions, hardware issues)
- ✅ Simpler debugging needed
- ✅ Minimal disk space available
- ✅ Quick setup on single machine

**When Docker is better:**
- ✅ Deploying to multiple machines
- ✅ Need guaranteed environment consistency
- ✅ CI/CD pipelines
- ✅ Team collaboration with different OS versions

---

## Quick Reference Card

### First Time Setup
```powershell
cd C:\Projects\PC_Value_Tracker
.\setup_environment.ps1
```

### Daily Usage
```powershell
# Activate environment
.\.venv\Scripts\activate

# Generate monthly report
python scripts\generate_monthly_report.py --month 2026-01

# Generate quarterly report
python scripts\generate_quarterly_report.py --quarter 2025-Q4

# Create blank presentation template
python scripts\create_leadership_presentation_template.py

# Create auto-filled presentation
python scripts\create_leadership_presentation_template.py --quarter 2025-Q4 --input data\master_combined.json
```

### File Locations
- **Data:** `data/master_combined.json`
- **Output:** `output/*.xlsx`, `output/*.pptx`
- **Templates:** `templates/*.pptx`
- **Scripts:** `scripts/*.py`
- **Documentation:** `docs/*.md`

---

## Next Steps After Setup

1. **Verify Environment:**
   ```powershell
   .\.venv\Scripts\python.exe scripts\generate_monthly_report.py --help
   ```

2. **Generate Test Report:**
   ```powershell
   .\.venv\Scripts\python.exe scripts\generate_monthly_report.py --month 2026-01
   ```

3. **Check Output:**
   - Open `output/Monthly_Report_2026-01.xlsx`
   - Verify data populated correctly

4. **Read Documentation:**
   - `README.md` - Project overview
   - `docs/REPORTING_BUILD_SUMMARY.md` - Complete system documentation
   - `docs/METHODOLOGY.md` - Leadership-facing methodology

5. **Continue Development:**
   - Modify scripts in `scripts/` directory
   - Test changes: `python scripts\<script_name>.py`
   - Commit changes: `git add .; git commit -m "Description"`

---

## Getting Help

If you encounter issues:

1. **Check error message carefully** - Most errors indicate missing files or wrong paths
2. **Verify virtual environment activated** - Should see `(.venv)` in prompt
3. **Check file paths** - Use absolute paths if relative paths fail
4. **Review documentation:**
   - `REPORTING_BUILD_SUMMARY.md` - System overview
   - `CONSOLIDATION_SUMMARY.md` - Recent changes
   - `DOCUMENTATION_UPDATE_SUMMARY.md` - Latest updates

5. **Check Python environment:**
   ```powershell
   .\.venv\Scripts\python.exe -c "import sys; print(sys.executable)"
   pip list
   ```

---

**Setup Complete?** Try generating a monthly report to verify everything works!
