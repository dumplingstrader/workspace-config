<#
.SYNOPSIS
    Creates a timestamped distribution package (ZIP) for USB/manual distribution
.DESCRIPTION
    Reusable utility to create distribution packages from any project folder.
    Designed for air-gapped environments requiring USB transfer.
    
    Features:
    - Auto-detects project files to include
    - Size-aware: can exclude/warn about large files
    - Supports project-specific config via .distribution-config.json
    - Dry-run mode to preview before creating
    - Creates organized staging area before zipping
    
.PARAMETER OutputPath
    Where to create the distribution package (default: .\Distribution)
    
.PARAMETER PackageName
    Base name for the ZIP file (default: auto-detected from folder name)
    
.PARAMETER ItemsToInclude
    Array of folder/file names to include (default: auto-detect all except exclusions)
    
.PARAMETER ExcludeLargeFiles
    Skip files larger than MaxFileSize threshold
    
.PARAMETER MaxFileSize
    Maximum individual file size in MB (default: 50MB). Files larger are skipped if ExcludeLargeFiles is set.
    
.PARAMETER MaxPackageSize
    Maximum total package size in MB (default: 500MB). Warning only, does not block creation.
    
.PARAMETER DryRun
    Preview what would be included without creating the ZIP
    
.PARAMETER UseConfig
    Load settings from .distribution-config.json in project folder (default: true)
    
.PARAMETER ReadmeContent
    Optional custom README.txt content to include in package
    
.EXAMPLE
    .\create_distribution_package.ps1
    Creates package with auto-detected settings
    
.EXAMPLE
    .\create_distribution_package.ps1 -ExcludeLargeFiles -MaxFileSize 25
    Creates package, excluding files larger than 25MB
    
.EXAMPLE
    .\create_distribution_package.ps1 -DryRun
    Preview what would be packaged without creating ZIP
    
.EXAMPLE
    .\create_distribution_package.ps1 -PackageName "MyProject_v2" -ItemsToInclude @("scripts", "data", "README.md")
    Creates package with specific name and items
    
.NOTES
    Created: January 30, 2026
    Purpose: Reusable distribution package creator for air-gapped environments
    Location: _scripts/create_distribution_package.ps1 (root level, reusable across projects)
#>

[CmdletBinding()]
param(
    [Parameter()]
    [string]$OutputPath = ".\Distribution",
    
    [Parameter()]
    [string]$PackageName = "",
    
    [Parameter()]
    [string[]]$ItemsToInclude = @(),
    
    [Parameter()]
    [switch]$ExcludeLargeFiles,
    
    [Parameter()]
    [int]$MaxFileSize = 50,
    
    [Parameter()]
    [int]$MaxPackageSize = 500,
    
    [Parameter()]
    [switch]$DryRun,
    
    [Parameter()]
    [switch]$UseConfig = $true,
    
    [Parameter()]
    [string]$ReadmeContent = ""
)

# Color output functions
function Write-Success { param($Message) Write-Host "✓ $Message" -ForegroundColor Green }
function Write-Info { param($Message) Write-Host "ℹ $Message" -ForegroundColor Cyan }
function Write-Warning { param($Message) Write-Host "⚠ $Message" -ForegroundColor Yellow }
function Write-Error { param($Message) Write-Host "✗ $Message" -ForegroundColor Red }
function Write-FileSize { param($Message, $Size) Write-Host "  $Message" -NoNewline; Write-Host " ($([math]::Round($Size, 2)) MB)" -ForegroundColor Gray }

# Get script location and set working directory to caller's location
$ScriptPath = Get-Location
Write-Info "Distribution Package Creator v2.0"
Write-Info "Working directory: $ScriptPath"
Write-Host ""

# Load project-specific config if exists
$Config = @{
    ExcludePatterns = @()
    LargeFileThresholdMB = $MaxFileSize
    CustomReadme = ""
    AdditionalExcludes = @()
}

if ($UseConfig -and (Test-Path ".distribution-config.json")) {
    try {
        $ConfigFile = Get-Content ".distribution-config.json" -Raw | ConvertFrom-Json
        Write-Success "Loaded configuration from .distribution-config.json"
        
        if ($ConfigFile.ExcludePatterns) { $Config.ExcludePatterns = $ConfigFile.ExcludePatterns }
        if ($ConfigFile.LargeFileThresholdMB) { $Config.LargeFileThresholdMB = $ConfigFile.LargeFileThresholdMB; $MaxFileSize = $ConfigFile.LargeFileThresholdMB }
        if ($ConfigFile.CustomReadme) { $Config.CustomReadme = $ConfigFile.CustomReadme }
        if ($ConfigFile.AdditionalExcludes) { $Config.AdditionalExcludes = $ConfigFile.AdditionalExcludes }
        Write-Host ""
    }
    catch {
        Write-Warning "Failed to load .distribution-config.json: $_"
        Write-Host ""
    }
}

# Determine package name
if ([string]::IsNullOrWhiteSpace($PackageName)) {
    $PackageName = Split-Path $ScriptPath -Leaf
    Write-Info "Auto-detected package name: $PackageName"
}
else {
    Write-Info "Using package name: $PackageName"
}

# Standard exclude patterns (always excluded)
$StandardExcludes = @(
    "Distribution",
    ".venv",
    ".git",
    ".github",
    ".vs",
    ".vscode",
    "__pycache__",
    "*.pyc",
    "*.pyo",
    ".env",
    ".env.local",
    "node_modules",
    "staging_temp",
    "*.log",
    ".DS_Store",
    "Thumbs.db",
    "desktop.ini"
)

# Combine with config excludes
$AllExcludes = $StandardExcludes + $Config.AdditionalExcludes + $Config.ExcludePatterns | Select-Object -Unique

# Auto-detect items to include if not specified
if ($ItemsToInclude.Count -eq 0) {
    Write-Info "Auto-detecting items to include..."
    
    $AllItems = Get-ChildItem -Path $ScriptPath | Where-Object {
        $item = $_
        $shouldExclude = $false
        
        foreach ($pattern in $AllExcludes) {
            if ($item.Name -like $pattern) {
                $shouldExclude = $true
                break
            }
        }
        
        -not $shouldExclude
    } | Select-Object -ExpandProperty Name
    
    $ItemsToInclude = $AllItems
    Write-Success "Found $($ItemsToInclude.Count) items to include"
}

Write-Host ""
Write-Info "Scanning files and calculating sizes..."
Write-Host ""

# Scan files and calculate sizes
$FileScanResults = @{
    TotalFiles = 0
    TotalSize = 0
    LargeFiles = @()
    IncludedFiles = @()
    SkippedFiles = @()
}

foreach ($Item in $ItemsToInclude) {
    $ItemPath = Join-Path $ScriptPath $Item
    if (Test-Path $ItemPath) {
        if ((Get-Item $ItemPath).PSIsContainer) {
            # Directory - scan recursively
            $Files = Get-ChildItem -Path $ItemPath -Recurse -File
            foreach ($File in $Files) {
                $FileSizeMB = $File.Length / 1MB
                $FileScanResults.TotalFiles++
                $FileScanResults.TotalSize += $FileSizeMB
                
                if ($FileSizeMB -gt $MaxFileSize) {
                    $FileScanResults.LargeFiles += @{
                        Path = $File.FullName.Replace($ScriptPath, ".")
                        Size = $FileSizeMB
                    }
                    
                    if ($ExcludeLargeFiles) {
                        $FileScanResults.SkippedFiles += $File.FullName.Replace($ScriptPath, ".")
                    }
                    else {
                        $FileScanResults.IncludedFiles += $File.FullName.Replace($ScriptPath, ".")
                    }
                }
                elseif ($FileSizeMB -gt 10) {
                    # Warn about files >10MB even if not excluding
                    $FileScanResults.IncludedFiles += $File.FullName.Replace($ScriptPath, ".")
                }
                else {
                    $FileScanResults.IncludedFiles += $File.FullName.Replace($ScriptPath, ".")
                }
            }
        }
        else {
            # Single file
            $File = Get-Item $ItemPath
            $FileSizeMB = $File.Length / 1MB
            $FileScanResults.TotalFiles++
            $FileScanResults.TotalSize += $FileSizeMB
            
            if ($FileSizeMB -gt $MaxFileSize) {
                $FileScanResults.LargeFiles += @{
                    Path = $File.FullName.Replace($ScriptPath, ".")
                    Size = $FileSizeMB
                }
                
                if ($ExcludeLargeFiles) {
                    $FileScanResults.SkippedFiles += $File.FullName.Replace($ScriptPath, ".")
                }
                else {
                    $FileScanResults.IncludedFiles += $File.FullName.Replace($ScriptPath, ".")
                }
            }
            else {
                $FileScanResults.IncludedFiles += $File.FullName.Replace($ScriptPath, ".")
            }
        }
    }
}

# Display scan results
Write-Info "Scan Results:"
Write-Host "  Total items to package: " -NoNewline; Write-Host $ItemsToInclude.Count -ForegroundColor White
Write-Host "  Total files: " -NoNewline; Write-Host $FileScanResults.TotalFiles -ForegroundColor White
Write-Host "  Estimated uncompressed size: " -NoNewline; Write-Host "$([math]::Round($FileScanResults.TotalSize, 2)) MB" -ForegroundColor White
Write-Host "  Estimated compressed size: " -NoNewline; Write-Host "$([math]::Round($FileScanResults.TotalSize * 0.3, 2)) MB (approx)" -ForegroundColor Gray
Write-Host ""

# Warn about large files
if ($FileScanResults.LargeFiles.Count -gt 0) {
    Write-Warning "Found $($FileScanResults.LargeFiles.Count) large file(s) (>$MaxFileSize MB):"
    foreach ($LargeFile in $FileScanResults.LargeFiles) {
        if ($ExcludeLargeFiles) {
            Write-Host "  [SKIPPED] " -NoNewline -ForegroundColor Yellow
        }
        else {
            Write-Host "  [INCLUDED] " -NoNewline -ForegroundColor Cyan
        }
        Write-FileSize $LargeFile.Path $LargeFile.Size
    }
    Write-Host ""
    
    if (-not $ExcludeLargeFiles) {
        Write-Warning "Use -ExcludeLargeFiles to skip files larger than $MaxFileSize MB"
        Write-Host ""
    }
}

# Check total package size
if ($FileScanResults.TotalSize -gt $MaxPackageSize) {
    Write-Warning "Package size ($([math]::Round($FileScanResults.TotalSize, 2)) MB) exceeds recommended limit ($MaxPackageSize MB)"
    Write-Warning "Consider using -ExcludeLargeFiles or reducing content"
    Write-Host ""
}

# Display items to include
Write-Info "Items to include in package:"
foreach ($item in $ItemsToInclude) {
    Write-Host "  • $item" -ForegroundColor Gray
}
Write-Host ""

# Dry run exit
if ($DryRun) {
    Write-Info "DRY RUN - No files were packaged"
    Write-Success "Preview complete. Remove -DryRun to create the ZIP package."
    exit 0
}

# Create distribution package
Write-Info "Creating distribution package..."
Write-Host ""

# Create output directory if needed
if (-not (Test-Path $OutputPath)) {
    New-Item -ItemType Directory -Path $OutputPath -Force | Out-Null
}

# Generate timestamp
$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$ZipFileName = "${PackageName}_$Timestamp.zip"
$ZipPath = Join-Path $OutputPath $ZipFileName

# Create temp staging directory
$StagingPath = Join-Path $OutputPath "staging_temp"
if (Test-Path $StagingPath) {
    Remove-Item -Path $StagingPath -Recurse -Force
}
New-Item -ItemType Directory -Path $StagingPath -Force | Out-Null

# Copy items to staging
Write-Info "Copying files to staging area..."
$CopiedCount = 0
$SkippedCount = 0
$CopiedSize = 0

foreach ($Item in $ItemsToInclude) {
    $SourcePath = Join-Path $ScriptPath $Item
    if (Test-Path $SourcePath) {
        try {
            $DestPath = Join-Path $StagingPath $Item
            
            # If excluding large files, need to filter during copy
            if ($ExcludeLargeFiles -and (Get-Item $SourcePath).PSIsContainer) {
                # Create directory structure
                New-Item -ItemType Directory -Path $DestPath -Force | Out-Null
                
                # Copy files selectively
                $Files = Get-ChildItem -Path $SourcePath -Recurse -File
                foreach ($File in $Files) {
                    $FileSizeMB = $File.Length / 1MB
                    if ($FileSizeMB -le $MaxFileSize) {
                        $RelPath = $File.FullName.Replace($SourcePath, "")
                        $DestFile = Join-Path $DestPath $RelPath
                        $DestDir = Split-Path $DestFile -Parent
                        
                        if (-not (Test-Path $DestDir)) {
                            New-Item -ItemType Directory -Path $DestDir -Force | Out-Null
                        }
                        
                        Copy-Item -Path $File.FullName -Destination $DestFile -Force
                        $CopiedCount++
                        $CopiedSize += $FileSizeMB
                    }
                    else {
                        $SkippedCount++
                    }
                }
                Write-Success "Copied: $Item (filtered large files)"
            }
            else {
                # Copy entire item
                Copy-Item -Path $SourcePath -Destination $DestPath -Recurse -Force -ErrorAction Stop
                
                # Count files
                if ((Get-Item $SourcePath).PSIsContainer) {
                    $FileCount = (Get-ChildItem -Path $SourcePath -Recurse -File).Count
                    $CopiedCount += $FileCount
                }
                else {
                    $CopiedCount++
                }
                
                Write-Success "Copied: $Item"
            }
        }
        catch {
            Write-Warning "Failed to copy: $Item ($_)"
            $SkippedCount++
        }
    }
    else {
        Write-Warning "Not found: $Item"
        $SkippedCount++
    }
}

Write-Host ""
Write-Info "Files copied: $CopiedCount succeeded, $SkippedCount skipped"
Write-Host ""

# Create README
if (-not [string]::IsNullOrWhiteSpace($ReadmeContent)) {
    $ReadmeContent | Out-File -FilePath (Join-Path $StagingPath "DISTRIBUTION_README.txt") -Encoding UTF8
    Write-Success "Created: DISTRIBUTION_README.txt (custom)"
}
elseif (-not [string]::IsNullOrWhiteSpace($Config.CustomReadme)) {
    $Config.CustomReadme | Out-File -FilePath (Join-Path $StagingPath "DISTRIBUTION_README.txt") -Encoding UTF8
    Write-Success "Created: DISTRIBUTION_README.txt (from config)"
}
else {
    # Create basic README
    $DefaultReadme = @"
# $PackageName Distribution Package
**Generated**: $(Get-Date -Format "MMMM dd, yyyy HH:mm:ss")

This is a portable distribution package for air-gapped/manual transfer.

## Contents

This package contains all necessary files to run the application.
See the main README.md or documentation for setup and usage instructions.

## Setup Instructions

1. Extract this ZIP to your desired location
2. Follow the instructions in README.md or QUICK_START.txt (if present)
3. Run any setup scripts (e.g., setup.ps1, setup_environment.ps1)

## Package Information

- Package Name: $PackageName
- Files Included: $CopiedCount
- Created: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
"@

    if ($ExcludeLargeFiles) {
        $DefaultReadme += @"

## Notes

- Large files (>$MaxFileSize MB) were excluded from this package
- Total excluded files: $SkippedCount
"@
    }

    $DefaultReadme | Out-File -FilePath (Join-Path $StagingPath "DISTRIBUTION_README.txt") -Encoding UTF8
    Write-Success "Created: DISTRIBUTION_README.txt (default)"
}

Write-Host ""
Write-Info "Creating ZIP archive..."

# Remove old zip if exists
if (Test-Path $ZipPath) {
    Remove-Item -Path $ZipPath -Force
    Write-Info "Removed existing: $ZipFileName"
}

# Create zip archive
try {
    Compress-Archive -Path "$StagingPath\*" -DestinationPath $ZipPath -CompressionLevel Optimal -Force
    Write-Success "Created: $ZipFileName"
    
    # Get zip file size
    $ZipSize = (Get-Item $ZipPath).Length / 1MB
    Write-Host ""
    Write-Info "Package Information:"
    Write-Host "  Name: " -NoNewline; Write-Host $ZipFileName -ForegroundColor White
    Write-Host "  Size: " -NoNewline; Write-Host "$([math]::Round($ZipSize, 2)) MB" -ForegroundColor White
    Write-Host "  Location: " -NoNewline; Write-Host $ZipPath -ForegroundColor White
    Write-Host "  Files: " -NoNewline; Write-Host $CopiedCount -ForegroundColor White
    
    if ($ZipSize -gt $MaxPackageSize) {
        Write-Host ""
        Write-Warning "Package size exceeds recommended $MaxPackageSize MB for USB transfer"
    }
}
catch {
    Write-Error "Failed to create ZIP archive: $_"
    exit 1
}
finally {
    # Cleanup staging
    if (Test-Path $StagingPath) {
        Remove-Item -Path $StagingPath -Recurse -Force
    }
}

Write-Host ""
Write-Success "Distribution package created successfully!"
Write-Host ""
Write-Info "Next steps:"
Write-Host "  1. Test the ZIP by extracting and running" -ForegroundColor Cyan
Write-Host "  2. Copy to USB drive or network location" -ForegroundColor Cyan
Write-Host "  3. Distribute to recipients" -ForegroundColor Cyan
Write-Host ""
