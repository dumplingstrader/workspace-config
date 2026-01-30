<#
.SYNOPSIS
    Organizes Skill Matrix/Promotion project files into logical folder structure
.DESCRIPTION
    Creates organized folder structure and moves files to appropriate locations
    for better project management and easier distribution preparation.
.NOTES
    Created: January 28, 2026
    Project: Site Lead Process Controls Engineer Promotion Package
#>

[CmdletBinding()]
param()

# Color output functions
function Write-Success { param($Message) Write-Host "✓ $Message" -ForegroundColor Green }
function Write-Info { param($Message) Write-Host "ℹ $Message" -ForegroundColor Cyan }
function Write-Warning { param($Message) Write-Host "⚠ $Message" -ForegroundColor Yellow }

# Get script location
$ScriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptPath

Write-Host ""
Write-Info "Skill Matrix Project File Organization"
Write-Info "Current directory: $ScriptPath"
Write-Host ""

# Define folder structure
$FolderStructure = @{
    "Promotion" = @()  # Already exists with promotion materials
    "Step_Up_Cards" = @()  # For proficiency cards
    "Scripts" = @()  # Python scripts
    "Archive" = @()  # Old versions
}

# File mapping (source -> destination)
$FileMapping = @{
    # Proficiency Step-Up Cards
    "AB_PLC_Proficiency_Step-Up_Card.md" = "Step_Up_Cards"
    "Experion_DCS_Proficiency_Step-Up_Card.md" = "Step_Up_Cards"
    "Triconex_SIS_Proficiency_Step-Up_Card.md" = "Step_Up_Cards"
    
    # Python Scripts
    "clear_assessment_values.py" = "Scripts"
    "enhance_skill_matrix.py" = "Scripts"
    "populate_role_requirements.py" = "Scripts"
}

# Files to keep in root (documentation and summary)
$RootFiles = @(
    "process_controls_skill_matrix_handoff_summary.md",
    "organize_files.ps1",
    "create_distribution_package.ps1"
)

Write-Info "Step 1: Creating folder structure..."
Write-Host ""

foreach ($TopFolder in $FolderStructure.Keys) {
    $TopPath = Join-Path $ScriptPath $TopFolder
    if (-not (Test-Path $TopPath)) {
        New-Item -ItemType Directory -Path $TopPath -Force | Out-Null
        Write-Success "Created: $TopFolder\"
    }
    else {
        Write-Info "Exists: $TopFolder\"
    }
    
    foreach ($SubFolder in $FolderStructure[$TopFolder]) {
        $SubPath = Join-Path $TopPath $SubFolder
        if (-not (Test-Path $SubPath)) {
            New-Item -ItemType Directory -Path $SubPath -Force | Out-Null
            Write-Success "Created: $TopFolder\$SubFolder\"
        }
    }
}

Write-Host ""
Write-Info "Step 2: Moving files to organized structure..."
Write-Host ""

$MoveCount = 0
$SkipCount = 0
$NotFoundCount = 0

foreach ($SourceFile in $FileMapping.Keys) {
    $SourcePath = Join-Path $ScriptPath $SourceFile
    $DestFolder = $FileMapping[$SourceFile]
    $DestPath = Join-Path $ScriptPath $DestFolder
    $DestFilePath = Join-Path $DestPath (Split-Path $SourceFile -Leaf)
    
    if (Test-Path $SourcePath) {
        # Only move if not already in correct location
        if ($SourcePath -ne $DestFilePath) {
            try {
                Move-Item -Path $SourcePath -Destination $DestPath -Force -ErrorAction Stop
                Write-Success "Moved: $SourceFile → $DestFolder\"
                $MoveCount++
            }
            catch {
                Write-Warning "Skipped: $SourceFile (file may be open in another program)"
                $SkipCount++
            }
        }
        else {
            Write-Info "Already in place: $SourceFile"
        }
    }
    else {
        Write-Warning "Not found: $SourceFile"
        $NotFoundCount++
    }
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Success "Organization complete!"
Write-Host ""
Write-Info "Summary:"
Write-Host "  • Files moved: $MoveCount" -ForegroundColor Green
if ($SkipCount -gt 0) {
    Write-Host "  • Files skipped: $SkipCount (close open files and re-run)" -ForegroundColor Yellow
}
if ($NotFoundCount -gt 0) {
    Write-Host "  • Files not found: $NotFoundCount" -ForegroundColor Yellow
}
Write-Host ""

Write-Info "Organized structure:"
Write-Host ""
Write-Host "  Promotion/                    (Promotion materials)" -ForegroundColor Cyan
Write-Host "    - Presentation deck, executive summary, talking points" -ForegroundColor Gray
Write-Host ""
Write-Host "  Step_Up_Cards/                (Proficiency cards)" -ForegroundColor Cyan
Write-Host "    - AB PLC, Experion DCS, Triconex SIS" -ForegroundColor Gray
Write-Host ""
Write-Host "  Scripts/                      (Python utilities)" -ForegroundColor Cyan
Write-Host "    - Skill matrix enhancement and assessment scripts" -ForegroundColor Gray
Write-Host ""
Write-Host "  Root/                         (Documentation)" -ForegroundColor Cyan
Write-Host "    - Handoff summary and organization scripts" -ForegroundColor Gray
Write-Host ""

Write-Info "Next steps:"
Write-Host "  1. Review organized structure" -ForegroundColor Cyan
Write-Host "  2. Run .\create_distribution_package.ps1 to create ZIP package" -ForegroundColor Cyan
Write-Host ""
