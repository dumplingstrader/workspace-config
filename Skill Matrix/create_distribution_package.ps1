<#
.SYNOPSIS
    Creates a timestamped distribution package (ZIP) from Skill Matrix folder
.DESCRIPTION
    Generic utility to create distribution packages from any folder structure.
    Copies specified items to a staging area and creates a timestamped ZIP archive.
    Reusable across different projects.
.PARAMETER OutputPath
    Where to create the distribution package (default: .\Distribution)
.PARAMETER PackageName
    Base name for the ZIP file (default: uses parent folder name)
.PARAMETER ItemsToInclude
    Array of folder/file names to include (default: all items except Distribution, .venv, .git, etc.)
.PARAMETER ReadmeContent
    Optional custom README.txt content to include in package
.EXAMPLE
    .\create_distribution_package.ps1
    Creates package with auto-detected name and all content
.EXAMPLE
    .\create_distribution_package.ps1 -PackageName "SkillMatrix" -ItemsToInclude @("Promotion", "Step_Up_Cards", "README.md")
    Creates package with specific name and items
.NOTES
    Created: January 28, 2026
    Purpose: Reusable distribution package creator for Skill Matrix project
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
    [string]$ReadmeContent = ""
)

# Color output functions
function Write-Success { param($Message) Write-Host "[SUCCESS] $Message" -ForegroundColor Green }
function Write-Info { param($Message) Write-Host "[INFO] $Message" -ForegroundColor Cyan }
function Write-Warning { param($Message) Write-Host "[WARNING] $Message" -ForegroundColor Yellow }
function Write-Error { param($Message) Write-Host "[ERROR] $Message" -ForegroundColor Red }

# Get script location
$ScriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptPath

# Determine package name
if ([string]::IsNullOrWhiteSpace($PackageName)) {
    $PackageName = "SkillMatrix_Promotion"
    Write-Info "Using package name: $PackageName"
}

Write-Info "Distribution Package Creator"
Write-Info "Current directory: $ScriptPath"
Write-Info "Package name: $PackageName"
Write-Host ""

# Auto-detect items to include if not specified
if ($ItemsToInclude.Count -eq 0) {
    Write-Info "Auto-detecting items to include..."
    
    # Exclude common non-distributable items
    $ExcludePatterns = @(
        "Distribution",
        ".venv",
        ".git",
        ".github",
        "__pycache__",
        "*.pyc",
        ".env",
        ".vs",
        "node_modules",
        "staging_temp",
        "organize_files.ps1",
        "create_distribution_package.ps1"
    )
    
    $AllItems = Get-ChildItem -Path $ScriptPath | Where-Object {
        $item = $_
        $shouldExclude = $false
        
        foreach ($pattern in $ExcludePatterns) {
            if ($item.Name -like $pattern) {
                $shouldExclude = $true
                break
            }
        }
        
        -not $shouldExclude
    } | Select-Object -ExpandProperty Name
    
    $ItemsToInclude = $AllItems
    Write-Info "Found $($ItemsToInclude.Count) items to include"
}

Write-Host ""
Write-Info "Items to include in package:"
foreach ($item in $ItemsToInclude) {
    Write-Host "  • $item" -ForegroundColor Gray
}
Write-Host ""

# Function to create distribution package
function New-DistributionPackage {
    param(
        [string]$OutputPath,
        [string]$PackageName,
        [string[]]$ItemsToInclude,
        [string]$ReadmeContent
    )
    
    Write-Info "Creating distribution package..."
    
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
    
    foreach ($Item in $ItemsToInclude) {
        $SourcePath = Join-Path $ScriptPath $Item
        if (Test-Path $SourcePath) {
            try {
                $DestPath = Join-Path $StagingPath $Item
                Copy-Item -Path $SourcePath -Destination $DestPath -Recurse -Force -ErrorAction Stop
                Write-Success "Copied: $Item"
                $CopiedCount++
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
    
    # Create README if content provided
    if (-not [string]::IsNullOrWhiteSpace($ReadmeContent)) {
        $ReadmeContent | Out-File -FilePath (Join-Path $StagingPath "README.txt") -Encoding UTF8
        Write-Success "Created: README.txt"
    }
    else {
        # Create basic README
        $DefaultReadme = @"
# Skill Matrix & Promotion Package
**Generated**: $(Get-Date -Format "MMMM dd, yyyy HH:mm:ss")

This package contains:

## Promotion Materials (Promotion/)
- Presentation deck for 1/30/26 meeting
- Executive summary (one-page)
- Updated talking points
- Gap response preparation
- Meeting materials and documentation

## Proficiency Step-Up Cards (Step_Up_Cards/)
- AB PLC Proficiency Step-Up Card
- Experion DCS Proficiency Step-Up Card
- Triconex SIS Proficiency Step-Up Card

## Python Scripts (Scripts/)
- Skill matrix enhancement utilities
- Assessment value management
- Role requirement population tools

## Documentation (Root)
- Process controls skill matrix handoff summary
- Project overview and context

For more information, refer to the documentation within each folder.
"@
        $DefaultReadme | Out-File -FilePath (Join-Path $StagingPath "README.txt") -Encoding UTF8
        Write-Success "Created: README.txt (default)"
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
        Write-Info "Package size: $([math]::Round($ZipSize, 2)) MB"
        Write-Info "Location: $ZipPath"
    }
    catch {
        Write-Error "Failed to create ZIP archive: $_"
        return $false
    }
    finally {
        # Cleanup staging
        if (Test-Path $StagingPath) {
            Remove-Item -Path $StagingPath -Recurse -Force
        }
    }
    
    Write-Host ""
    Write-Success "Distribution package created successfully!"
    return $true
}

# Main execution
try {
    $success = New-DistributionPackage -OutputPath $OutputPath -PackageName $PackageName -ItemsToInclude $ItemsToInclude -ReadmeContent $ReadmeContent
    
    if ($success) {
        Write-Host ""
        Write-Success "Process completed!"
        Write-Info "Next steps:"
        Write-Host "  1. Review distribution package in: $OutputPath" -ForegroundColor Cyan
        Write-Host "  2. Test ZIP contents before external distribution" -ForegroundColor Cyan
        Write-Host "  3. Share the package or upload as needed" -ForegroundColor Cyan
    }
}
catch {
    Write-Error "Script failed: $_"
    exit 1
}
