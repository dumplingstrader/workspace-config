<#
.SYNOPSIS
    Organizes APO project files into logical folder structure
.DESCRIPTION
    Creates organized folder structure and moves files to appropriate locations
    for better project management and easier distribution preparation.
.NOTES
    Created: January 27, 2026
    Project: ACM to APO Migration Whitepaper & Conference Submission
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
Write-Info "APO Project File Organization"
Write-Info "Current directory: $ScriptPath"
Write-Host ""

# Define folder structure
$FolderStructure = @{
    "1_Deliverables" = @(
        "Conference_Submission",
        "Whitepaper",
        "Checklist"
    )
    "2_Source_Documents" = @(
        "Working_Versions",
        "Barbara_Feedback"
    )
    "3_Reference_Materials" = @(
        "Honeywell_Documentation",
        "Industry_Standards",
        "Case_Studies"
    )
    "4_Scripts_Tools" = @()
    "5_Archive" = @(
        "Extracted_Text"
    )
}

# File mapping (source -> destination)
$FileMapping = @{
    # 1_Deliverables/Conference_Submission
    "Executive_Summary_Conference_Submission.txt" = "1_Deliverables\Conference_Submission"
    "Presentation_Outline_Conference.md" = "1_Deliverables\Conference_Submission"
    "Presentation_Outline_Conference.docx" = "1_Deliverables\Conference_Submission"
    "DynAMo Standard Sync and Alternative Active Sync v3.2.pptx" = "1_Deliverables\Conference_Submission"
    
    # 1_Deliverables/Whitepaper
    "ACM_to_APO_Migration_Whitepaper_Outline.md" = "1_Deliverables\Whitepaper"
    "ACM_to_APO_Migration_Whitepaper_Outline.docx" = "1_Deliverables\Whitepaper"
    
    # 1_Deliverables/Checklist
    "ACM_to_APO_Migration_Comprehensive_Checklist.xlsx" = "1_Deliverables\Checklist"
    "CHECKLIST_CREATION_SUMMARY.md" = "1_Deliverables\Checklist"
    "CHECKLIST_CREATION_SUMMARY.pdf" = "1_Deliverables\Checklist"
    
    # 2_Source_Documents/Working_Versions
    "APO_Deployment_Workflow_Checklist.xlsx" = "2_Source_Documents\Working_Versions"
    
    # 2_Source_Documents/Barbara_Feedback
    "ACM_to_APO_Migration_Whitepaper_Outline_BKS edits.docx" = "2_Source_Documents\Barbara_Feedback"
    "Potential additions to the Standard HAM delivery (Barbara Schubert).docx" = "2_Source_Documents\Barbara_Feedback"
    
    # 3_Reference_Materials/Honeywell_Documentation
    "Alarm Performance Optimizer Configuration Guide.pdf" = "3_Reference_Materials\Honeywell_Documentation"
    "Alarm Performance Optimizer Installation Guide.pdf" = "3_Reference_Materials\Honeywell_Documentation"
    "GuardianNewsletterQ32025.pdf" = "3_Reference_Materials\Honeywell_Documentation"
    
    # 3_Reference_Materials/Industry_Standards
    "honeywell-alarm-management-standards-whitepaper.pdf" = "3_Reference_Materials\Industry_Standards"
    
    # 3_Reference_Materials/Case_Studies
    "MPC APO Deployment Cookbook.docx" = "3_Reference_Materials\Case_Studies"
    "O-791428_ APO training.docx" = "3_Reference_Materials\Case_Studies"
    "SuccessStory_IrvingOil_AlarmManagement1.pdf" = "3_Reference_Materials\Case_Studies"
    
    # 4_Scripts_Tools
    "create_comprehensive_checklist.py" = "4_Scripts_Tools"
    "create_comprehensive_checklist_v2.py" = "4_Scripts_Tools"
    "read_checklist.py" = "4_Scripts_Tools"
    
    # 5_Archive/Extracted_Text
    "BKS_edits_extracted.txt" = "5_Archive\Extracted_Text"
    "PPTX_extracted.txt" = "5_Archive\Extracted_Text"
}

# Files to keep in root (documentation)
$RootFiles = @(
    "PROJECT_HANDOFF_SUMMARY.md",
    "APO_Documentation_Analysis_Summary.md",
    "DISTRIBUTION_GUIDE.md",
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
        else {
            Write-Info "Exists: $TopFolder\$SubFolder\"
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
Write-Host "  1_Deliverables/" -ForegroundColor Cyan
Write-Host "    - Conference_Submission/  (4 files)" -ForegroundColor Gray
Write-Host "    - Whitepaper/             (2 files)" -ForegroundColor Gray
Write-Host "    - Checklist/              (3 files)" -ForegroundColor Gray
Write-Host ""
Write-Host "  2_Source_Documents/" -ForegroundColor Cyan
Write-Host "    - Working_Versions/       (1 file)" -ForegroundColor Gray
Write-Host "    - Barbara_Feedback/       (2 files)" -ForegroundColor Gray
Write-Host ""
Write-Host "  3_Reference_Materials/" -ForegroundColor Cyan
Write-Host "    - Honeywell_Documentation/ (3 files)" -ForegroundColor Gray
Write-Host "    - Industry_Standards/      (1 file)" -ForegroundColor Gray
Write-Host "    - Case_Studies/            (3 files)" -ForegroundColor Gray
Write-Host ""
Write-Host "  4_Scripts_Tools/              (3 files)" -ForegroundColor Cyan
Write-Host ""
Write-Host "  5_Archive/" -ForegroundColor Cyan
Write-Host "    - Extracted_Text/          (2 files)" -ForegroundColor Gray
Write-Host ""
Write-Host "  Root documentation:" -ForegroundColor Cyan
foreach ($RootFile in $RootFiles) {
    if (Test-Path (Join-Path $ScriptPath $RootFile)) {
        Write-Host "    • $RootFile" -ForegroundColor Gray
    }
}
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

Write-Info "Next steps:"
Write-Host "  1. Review organized folder structure" -ForegroundColor White
Write-Host "  2. Run .\create_distribution_package.ps1 -ZipOnly to create ZIP" -ForegroundColor White
Write-Host "  3. See DISTRIBUTION_GUIDE.md for full usage information" -ForegroundColor White
Write-Host ""
