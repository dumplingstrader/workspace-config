# Copy PC Value Tracker to shared folder (excludes private files)
# Usage: .\copy_to_shared_folder.ps1 -Destination "\\server\share\PC_Value_Tracker"

param(
    [Parameter(Mandatory=$true)]
    [string]$Destination
)

$source = $PSScriptRoot

# Create destination if it doesn't exist
if (-not (Test-Path $Destination)) {
    New-Item -ItemType Directory -Path $Destination -Force | Out-Null
}

# Files and folders to include
$itemsToShare = @(
    "README.md",
    "SETUP.md",
    "requirements.txt",
    "config\",
    "scripts\",
    "templates\",
    "submissions\README.md",
    "docs\METHODOLOGY.md",
    "docs\COPILOT_PROMPTS.md",
    "docs\COPILOT_PROMPTS_LEAD_ENGINEER.md",
    "docs\DATA_COLLECTION_PROCEDURE.md",
    "docs\SUPERVISOR_BRIEFING.md",
    "extract_rca_emails.ps1"
)

# Files to EXCLUDE (will NOT be copied)
Write-Host "Copying shareable files to: $Destination" -ForegroundColor Green
Write-Host ""
Write-Host "EXCLUDED (private files):" -ForegroundColor Yellow
Write-Host "  - docs\HANDOFF_INTERNAL.md"
Write-Host "  - data\ folder (your personal work history)"
Write-Host "  - output\ folder (your generated reports)"
Write-Host ""

foreach ($item in $itemsToShare) {
    $sourcePath = Join-Path $source $item
    $destPath = Join-Path $Destination $item
    
    if (Test-Path $sourcePath) {
        if (Test-Path $sourcePath -PathType Container) {
            # Copy directory
            Copy-Item -Path $sourcePath -Destination $destPath -Recurse -Force
            Write-Host "Copied: $item" -ForegroundColor Cyan
        } else {
            # Copy file
            $destDir = Split-Path $destPath -Parent
            if (-not (Test-Path $destDir)) {
                New-Item -ItemType Directory -Path $destDir -Force | Out-Null
            }
            Copy-Item -Path $sourcePath -Destination $destPath -Force
            Write-Host "Copied: $item" -ForegroundColor Cyan
        }
    }
}

# Create empty data and output folders (with README placeholders)
$dataFolder = Join-Path $Destination "data"
$outputFolder = Join-Path $Destination "output"

if (-not (Test-Path $dataFolder)) {
    New-Item -ItemType Directory -Path $dataFolder -Force | Out-Null
    Set-Content -Path (Join-Path $dataFolder "README.md") -Value "# Data Folder`n`nPlace your extracted work history files here.`n`nFiles in this folder are kept private."
}

if (-not (Test-Path $outputFolder)) {
    New-Item -ItemType Directory -Path $outputFolder -Force | Out-Null
    Set-Content -Path (Join-Path $outputFolder "README.md") -Value "# Output Folder`n`nGenerated reports will be saved here.`n`nFiles in this folder are kept private."
}

Write-Host ""
Write-Host "Copy complete! Shared folder ready at: $Destination" -ForegroundColor Green
Write-Host ""
Write-Host "Your private files remain only on your local machine." -ForegroundColor Yellow
