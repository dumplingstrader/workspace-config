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

# Copy templates if they exist
if (Test-Path "templates") {
    Copy-Item "templates\*.xlsx" "$tempFolder\templates\" -ErrorAction SilentlyContinue
}

# Copy pilot data (master.json and raw files as examples)
if (Test-Path "data\master.json") {
    Copy-Item "data\master.json" "$tempFolder\data\"
}
if (Test-Path "data\raw\*.xlsx") {
    Get-ChildItem "data\raw\*.xlsx" | Copy-Item -Destination "$tempFolder\data\raw\"
}

# Copy archived data if exists
if (Test-Path "data\archive") {
    Copy-Item -Recurse "data\archive" "$tempFolder\data\" -ErrorAction SilentlyContinue
}

# Copy example outputs (generated reports)
if (Test-Path "output\monthly\*.xlsx") {
    Get-ChildItem "output\monthly\*.xlsx" | Copy-Item -Destination "$tempFolder\output\monthly\"
}
if (Test-Path "output\quarterly\*.xlsx") {
    Get-ChildItem "output\quarterly\*.xlsx" | Copy-Item -Destination "$tempFolder\output\quarterly\"
}

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
Write-Host "  - scripts\collect\ (aggregate_raw_data.py)"
Write-Host "  - scripts\report\ (generate_monthly_report.py, generate_quarterly_report.py)"
Write-Host "  - scripts\util\ (show_summary.py, archive_raw_files.py, fix_blank_resolutions.py)"
Write-Host "  - config\ (streams.json)"
Write-Host "  - docs\ (all documentation)"
Write-Host "  - data\master.json (107 records)"
Write-Host "  - data\archive\ (archived files)"
Write-Host "  - output\ (example reports)"
Write-Host ""
Write-Host "Included pilot data as examples for recipients." -ForegroundColor Cyan
Write-Host "Upload to shared network location for distribution." -ForegroundColor Magenta
