<#
.SYNOPSIS
    Organizes Promotion folder files into logical structure
.DESCRIPTION
    Creates organized folder structure and moves files to appropriate locations
    for better project management: Scripts, Presentations, Source Documents, etc.
.NOTES
    Created: January 28, 2026
    Project: Site Lead Process Controls Engineer Promotion Materials
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
Write-Info "Promotion Materials File Organization"
Write-Info "Current directory: $ScriptPath"
Write-Host ""

# Define folder structure
$FolderStructure = @{
    "Scripts" = @()
    "Presentations" = @()
    "Source_Documents" = @()
    "Supporting_Documents" = @()
    "Templates" = @()
    "Archive" = @()
}

# File mapping (source -> destination)
$FileMapping = @{
    # Python Scripts (active)
    "add_content.py" = "Scripts"
    "standardize_formatting.py" = "Scripts"
    
    # Presentations
    "Site_Lead_PCS_Engineer_Presentation_01_30_26.pptx" = "Presentations"
    "working.pptx" = "Presentations"
    "titles-only.pptx" = "Presentations"
    
    # Source Documents
    "presentation_deck_01_30_26.md" = "Source_Documents"
    "SiteLeadEngineer_TonyChiu.docx" = "Source_Documents"
    "docx_content.txt" = "Source_Documents"
    
    # Supporting Documents
    "executive_summary_one_page_01_30_26.md" = "Supporting_Documents"
    "executive_summary_one_page_01_30_26.pdf" = "Supporting_Documents"
    "talking_points_updated_01_30_26.md" = "Supporting_Documents"
    "gap_responses_preparation_01_30_26.md" = "Supporting_Documents"
    "gap_responses_preparation_01_30_26.pdf" = "Supporting_Documents"
    
    # Templates and Configuration
    "MPC NEW PowerPoint Template (07-06-2020) (545456x9C980).pptx" = "Templates"
    "replacement-text.json" = "Templates"
    "text-inventory.json" = "Templates"
    
    # Archive (old/unused scripts)
    "build_mpc_presentation.ps1" = "Archive"
    "build_mpc_presentation_fixed.ps1" = "Archive"
    "generate_presentation.js" = "Archive"
    "generate_presentation_powershell.ps1" = "Archive"
    "current-content.md" = "Archive"
    "template-content.md" = "Archive"
    "presentation-verification.md" = "Archive"
    "gap_analysis_prep.md" = "Archive"
    "meeting_invite_email.md" = "Archive"
    "meeting_talking_points.md" = "Archive"
}

# Directories to move
$DirectoryMapping = @{
    "template-unpacked" = "Templates"
    "slides" = "Archive"
}

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
        if ($SourcePath -ne $DestFilePath) {
            try {
                Move-Item -Path $SourcePath -Destination $DestPath -Force -ErrorAction Stop
                Write-Success "Moved: $SourceFile -> $DestFolder\"
                $MoveCount++
            }
            catch {
                Write-Warning "Skipped: $SourceFile (file may be open)"
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
Write-Info "Step 3: Moving directories..."
Write-Host ""

foreach ($SourceDir in $DirectoryMapping.Keys) {
    $SourcePath = Join-Path $ScriptPath $SourceDir
    $DestFolder = $DirectoryMapping[$SourceDir]
    $DestPath = Join-Path $ScriptPath $DestFolder
    $DestDirPath = Join-Path $DestPath $SourceDir
    
    if (Test-Path $SourcePath) {
        if ($SourcePath -ne $DestDirPath) {
            try {
                Move-Item -Path $SourcePath -Destination $DestPath -Force -ErrorAction Stop
                Write-Success "Moved: $SourceDir\ -> $DestFolder\"
                $MoveCount++
            }
            catch {
                Write-Warning "Skipped: $SourceDir\ (directory may be in use)"
                $SkipCount++
            }
        }
        else {
            Write-Info "Already in place: $SourceDir\"
        }
    }
    else {
        Write-Warning "Not found: $SourceDir\"
        $NotFoundCount++
    }
}

Write-Host ""
Write-Host "=======================================================" -ForegroundColor Cyan
Write-Host ""
Write-Success "Organization complete!"
Write-Host ""
Write-Info "Summary:"
Write-Host "  * Items moved: $MoveCount" -ForegroundColor Green
if ($SkipCount -gt 0) {
    Write-Host "  * Items skipped: $SkipCount (close open files and re-run)" -ForegroundColor Yellow
}
if ($NotFoundCount -gt 0) {
    Write-Host "  * Items not found: $NotFoundCount" -ForegroundColor Yellow
}
Write-Host ""

Write-Info "Organized structure:"
Write-Host ""
Write-Host "  Presentations/                (Final and working presentations)" -ForegroundColor Cyan
Write-Host "    - Site_Lead_PCS_Engineer_Presentation_01_30_26.pptx (FINAL)" -ForegroundColor Green
Write-Host "    - working.pptx, titles-only.pptx (intermediate files)" -ForegroundColor Gray
Write-Host ""
Write-Host "  Scripts/                      (Python generation scripts)" -ForegroundColor Cyan
Write-Host "    - add_content.py (content generation)" -ForegroundColor Gray
Write-Host "    - standardize_formatting.py (formatting application)" -ForegroundColor Gray
Write-Host ""
Write-Host "  Source_Documents/             (Original content)" -ForegroundColor Cyan
Write-Host "    - presentation_deck_01_30_26.md" -ForegroundColor Gray
Write-Host "    - SiteLeadEngineer_TonyChiu.docx" -ForegroundColor Gray
Write-Host ""
Write-Host "  Supporting_Documents/         (Meeting preparation materials)" -ForegroundColor Cyan
Write-Host "    - Executive summary (MD + PDF)" -ForegroundColor Gray
Write-Host "    - Talking points, Gap responses" -ForegroundColor Gray
Write-Host ""
Write-Host "  Templates/                    (MPC template and configs)" -ForegroundColor Cyan
Write-Host "    - MPC PowerPoint template" -ForegroundColor Gray
Write-Host "    - JSON mappings and unpacked template" -ForegroundColor Gray
Write-Host ""
Write-Host "  Archive/                      (Old/unused files)" -ForegroundColor Cyan
Write-Host "    - Abandoned PowerShell/Node.js approaches" -ForegroundColor Gray
Write-Host "    - Draft markdown files" -ForegroundColor Gray
Write-Host ""
Write-Host "  Root/                         (Documentation)" -ForegroundColor Cyan
Write-Host "    - PROJECT_HANDOFF.md (comprehensive documentation)" -ForegroundColor Green
Write-Host "    - organize_promotion_files.ps1 (this script)" -ForegroundColor Gray
Write-Host ""

Write-Info "Key Files After Organization:"
Write-Host ""
Write-Host "  [FINAL PRESENTATION]" -ForegroundColor Green
Write-Host "     Presentations/Site_Lead_PCS_Engineer_Presentation_01_30_26.pptx" -ForegroundColor White
Write-Host ""
Write-Host "  [SUPPORTING DOCS]" -ForegroundColor Green
Write-Host "     Supporting_Documents/executive_summary_one_page_01_30_26.pdf" -ForegroundColor White
Write-Host "     Supporting_Documents/talking_points_updated_01_30_26.md" -ForegroundColor White
Write-Host ""
Write-Host "  [DOCUMENTATION]" -ForegroundColor Green
Write-Host "     PROJECT_HANDOFF.md" -ForegroundColor White
Write-Host ""

Write-Info "To Modify Presentation in Future:"
Write-Host "  1. Close PowerPoint if presentation is open" -ForegroundColor Cyan
Write-Host "  2. Edit Scripts/add_content.py" -ForegroundColor Cyan
Write-Host "  3. Run: python Scripts/add_content.py" -ForegroundColor Cyan
Write-Host "  4. Run: python Scripts/standardize_formatting.py" -ForegroundColor Cyan
Write-Host "  5. Presentation updated in Presentations folder" -ForegroundColor Cyan
Write-Host ""
