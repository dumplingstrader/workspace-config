# LA Refinery Spend Tracker v2.0 - Setup
# Run this once to install Python dependencies

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "LA Refinery Spend Tracker - Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Python:" -ForegroundColor Yellow
    Write-Host "  1. Go to https://www.python.org/downloads/" -ForegroundColor White
    Write-Host "  2. Download Python 3.11 or later" -ForegroundColor White
    Write-Host "  3. Run the installer" -ForegroundColor White
    Write-Host "  4. IMPORTANT: Check 'Add Python to PATH'" -ForegroundColor White
    Write-Host "  5. Click 'Install Now'" -ForegroundColor White
    Write-Host ""
    pause
    exit 1
}

Write-Host ""
Write-Host "Installing Python dependencies..." -ForegroundColor Cyan
pip install pandas openpyxl --break-system-packages

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "Setup complete!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "  1. Place ME2K exports in data\me2k\ folder" -ForegroundColor White
    Write-Host "     (filename must start with 'EXPORT_')" -ForegroundColor Gray
    Write-Host "  2. Place TS Actuals in data\ts_actuals\ folder" -ForegroundColor White
    Write-Host "     (filename must contain 'ts_actual')" -ForegroundColor Gray
    Write-Host "  3. Run: .\run_tracker.ps1" -ForegroundColor White
    Write-Host "  4. Check output in output\ folder" -ForegroundColor White
} else {
    Write-Host ""
    Write-Host "ERROR: Setup failed" -ForegroundColor Red
    Write-Host "Try running manually: pip install pandas openpyxl" -ForegroundColor Yellow
}

Write-Host ""
pause
