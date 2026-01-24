# PC Value Tracker - Automated Environment Setup Script
# Run this on new machine to set up Python environment
# Usage: .\setup_environment.ps1

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "PC Value Tracker - Environment Setup" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Check if Python is installed
Write-Host "Checking for Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Found: $pythonVersion" -ForegroundColor Green
    
    # Check version (need 3.10+)
    if ($pythonVersion -match "Python (\d+)\.(\d+)") {
        $major = [int]$Matches[1]
        $minor = [int]$Matches[2]
        
        if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 10)) {
            Write-Host "⚠ Warning: Python 3.10+ recommended (you have $major.$minor)" -ForegroundColor Yellow
            Write-Host "  Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
        }
    }
} catch {
    Write-Host "✗ Python not found!" -ForegroundColor Red
    Write-Host "  Please install Python 3.10+ from: https://www.python.org/downloads/" -ForegroundColor Red
    Write-Host "  Make sure to check 'Add Python to PATH' during installation" -ForegroundColor Red
    exit 1
}

# Check if pip is available
Write-Host "`nChecking for pip..." -ForegroundColor Yellow
try {
    $pipVersion = pip --version 2>&1
    Write-Host "✓ Found: $pipVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ pip not found!" -ForegroundColor Red
    Write-Host "  Run: python -m ensurepip --upgrade" -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host "`nCreating virtual environment..." -ForegroundColor Yellow
if (Test-Path ".venv") {
    Write-Host "⚠ Virtual environment already exists (.venv)" -ForegroundColor Yellow
    $response = Read-Host "Delete and recreate? (y/N)"
    if ($response -eq "y" -or $response -eq "Y") {
        Remove-Item -Recurse -Force .venv
        Write-Host "Deleted existing .venv" -ForegroundColor Gray
    } else {
        Write-Host "Using existing .venv" -ForegroundColor Gray
        .\.venv\Scripts\activate
        Write-Host "✓ Activated existing virtual environment" -ForegroundColor Green
        $skipInstall = $true
    }
}

if (-not $skipInstall) {
    python -m venv .venv
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Created .venv" -ForegroundColor Green
    } else {
        Write-Host "✗ Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
    
    # Activate virtual environment
    Write-Host "`nActivating virtual environment..." -ForegroundColor Yellow
    .\.venv\Scripts\activate
    Write-Host "✓ Activated" -ForegroundColor Green
}

# Install dependencies
Write-Host "`nInstalling Python packages from requirements.txt..." -ForegroundColor Yellow
Write-Host "(This may take 1-2 minutes...)" -ForegroundColor Gray

pip install --upgrade pip | Out-Null
pip install -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ All packages installed successfully" -ForegroundColor Green
} else {
    Write-Host "✗ Package installation failed" -ForegroundColor Red
    Write-Host "  Try manually: pip install pandas openpyxl python-pptx" -ForegroundColor Red
    exit 1
}

# Verify installations
Write-Host "`nVerifying installations..." -ForegroundColor Yellow
$packages = @("pandas", "openpyxl", "pptx")
$allGood = $true

foreach ($pkg in $packages) {
    try {
        $result = python -c "import $pkg; print($pkg.__version__)" 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  ✓ $pkg ($result)" -ForegroundColor Green
        } else {
            Write-Host "  ✗ $pkg failed to import" -ForegroundColor Red
            $allGood = $false
        }
    } catch {
        Write-Host "  ✗ $pkg not found" -ForegroundColor Red
        $allGood = $false
    }
}

# Create directories if missing
Write-Host "`nCreating output directories..." -ForegroundColor Yellow
$dirs = @("data", "output", "templates", "submissions")
foreach ($dir in $dirs) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir | Out-Null
        Write-Host "  ✓ Created $dir/" -ForegroundColor Green
    } else {
        Write-Host "  → $dir/ exists" -ForegroundColor Gray
    }
}

# Final status
Write-Host "`n========================================" -ForegroundColor Cyan
if ($allGood) {
    Write-Host "✓ SETUP COMPLETE!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "`nNext steps:" -ForegroundColor Yellow
    Write-Host "  1. Place master_combined.json in data/ directory"
    Write-Host "  2. Run scripts using:" -ForegroundColor Yellow
    Write-Host "     .\.venv\Scripts\python.exe scripts\generate_monthly_report.py --help" -ForegroundColor Cyan
    Write-Host "     .\.venv\Scripts\python.exe scripts\create_leadership_presentation_template.py --help" -ForegroundColor Cyan
    Write-Host "`n  3. To activate environment in future sessions:" -ForegroundColor Yellow
    Write-Host "     .\.venv\Scripts\activate" -ForegroundColor Cyan
} else {
    Write-Host "⚠ SETUP INCOMPLETE" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "`nSome packages failed to install. Try manually:" -ForegroundColor Yellow
    Write-Host "  pip install pandas openpyxl python-pptx" -ForegroundColor Cyan
}

Write-Host ""
