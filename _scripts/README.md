# Reusable Scripts

Root-level scripts for common tasks across all projects in this workspace.

## Available Scripts

### create_distribution_package.ps1

Creates timestamped distribution packages (ZIP) for USB/manual transfer in air-gapped environments.

**Features:**
- Auto-detects project files to include
- Size-aware: can exclude/warn about large files
- Supports project-specific config via `.distribution-config.json`
- Dry-run mode to preview before creating
- Smart exclusions (`.venv`, `.git`, `__pycache__`, etc.)

**Basic Usage:**

```powershell
# From any project folder, run:
..\_scripts\create_distribution_package.ps1

# Preview without creating ZIP:
..\_scripts\create_distribution_package.ps1 -DryRun

# Exclude files larger than 25MB:
..\_scripts\create_distribution_package.ps1 -ExcludeLargeFiles -MaxFileSize 25

# Custom package name:
..\_scripts\create_distribution_package.ps1 -PackageName "MyProject_v2.0"
```

**Project-Specific Configuration:**

Copy `.distribution-config.json.template` to your project root as `.distribution-config.json` and customize:

```json
{
  "LargeFileThresholdMB": 50,
  "MaxPackageSizeMB": 500,
  "AdditionalExcludes": ["_scratch", "*.bak"],
  "CustomReadme": "Your custom README content"
}
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| OutputPath | string | `.\Distribution` | Where to create the package |
| PackageName | string | auto-detect | Base name for ZIP file |
| ItemsToInclude | string[] | auto-detect | Specific items to include |
| ExcludeLargeFiles | switch | false | Skip files > MaxFileSize |
| MaxFileSize | int | 50 | Max file size in MB |
| MaxPackageSize | int | 500 | Warning threshold for package |
| DryRun | switch | false | Preview without creating |
| UseConfig | switch | true | Load .distribution-config.json |
| ReadmeContent | string | auto-generate | Custom README content |

**Examples:**

```powershell
# SpendTracker distribution
cd C:\Users\GF99\Documentation\SpendTracker
..\_scripts\create_distribution_package.ps1

# Skill Matrix with large file exclusion
cd "C:\Users\GF99\Documentation\Skill Matrix"
..\_scripts\create_distribution_package.ps1 -ExcludeLargeFiles

# PC Value Tracker with custom settings
cd C:\Users\GF99\Documentation\PC_Value_Tracker
..\_scripts\create_distribution_package.ps1 -MaxFileSize 25 -PackageName "PC_Value_Tracker_v3.0"
```

**What Gets Excluded (Always):**

- `.venv` (virtual environments)
- `.git` (git repositories)
- `__pycache__` (Python cache)
- `node_modules` (npm packages)
- `.env` files (secrets)
- `Distribution` folder (output location)
- Log files, temp files, system files

**Output:**

Creates `Distribution/{PackageName}_{timestamp}.zip` containing:
- All project files (except exclusions)
- Auto-generated `DISTRIBUTION_README.txt`
- Original project structure preserved

---

## Adding New Scripts

When adding scripts here:
1. Make them reusable across projects
2. Include comprehensive help comments
3. Use parameters for customization
4. Test in multiple projects
5. Document in this README
