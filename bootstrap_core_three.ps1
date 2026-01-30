# Bootstrap Core Three Documentation
# Adds README.md, HANDOFF.md, and _TODO.md to projects missing them

param(
    [switch]$DryRun,
    [string[]]$Projects = @()
)

$templateDir = "_templates"
$allProjects = @(
    'Experion_License_Aggregator',
    'Graphics',
    'Integrity',
    'PC_Value_Tracker',
    'SAP',
    'Skill Matrix',
    'SpendTracker',
    'Training'
)

# Use specified projects or all
$targetProjects = if ($Projects.Count -gt 0) { $Projects } else { $allProjects }

Write-Host "=== BOOTSTRAPPING CORE THREE DOCUMENTATION ===" -ForegroundColor Cyan
if ($DryRun) {
    Write-Host "(DRY RUN - no files will be created)" -ForegroundColor Yellow
}
Write-Host ""

$stats = @{
    Created = 0
    Skipped = 0
    Errors = 0
}

foreach ($proj in $targetProjects) {
    if (-not (Test-Path $proj)) {
        Write-Host "⚠️  $proj - project folder not found" -ForegroundColor Red
        $stats.Errors++
        continue
    }
    
    Write-Host "$proj" -ForegroundColor White
    
    # README.md
    $readmePath = Join-Path $proj "README.md"
    if (Test-Path $readmePath) {
        Write-Host "  [SKIP] README.md already exists" -ForegroundColor Gray
        $stats.Skipped++
    } else {
        if (-not $DryRun) {
            Copy-Item "$templateDir/project-readme.md" $readmePath
        }
        Write-Host "  [CREATE] README.md" -ForegroundColor Green
        $stats.Created++
    }
    
    # HANDOFF.md
    $handoffPath = Join-Path $proj "HANDOFF.md"
    if (Test-Path $handoffPath) {
        Write-Host "  [SKIP] HANDOFF.md already exists" -ForegroundColor Gray
        $stats.Skipped++
    } else {
        if (-not $DryRun) {
            Copy-Item "$templateDir/project-handoff.md" $handoffPath
        }
        Write-Host "  [CREATE] HANDOFF.md" -ForegroundColor Green
        $stats.Created++
    }
    
    # _TODO.md
    $todoPath = Join-Path $proj "_TODO.md"
    if (Test-Path $todoPath) {
        Write-Host "  [SKIP] _TODO.md already exists" -ForegroundColor Gray
        $stats.Skipped++
    } else {
        if (-not $DryRun) {
            Copy-Item "$templateDir/_TODO.md" $todoPath
        }
        Write-Host "  [CREATE] _TODO.md" -ForegroundColor Green
        $stats.Created++
    }
    
    Write-Host ""
}

Write-Host "=== SUMMARY ===" -ForegroundColor Cyan
Write-Host "Created: $($stats.Created) files" -ForegroundColor Green
Write-Host "Skipped: $($stats.Skipped) files (already exist)" -ForegroundColor Gray
if ($stats.Errors -gt 0) {
    Write-Host "Errors:  $($stats.Errors) projects" -ForegroundColor Red
}

if ($DryRun) {
    Write-Host ""
    Write-Host "Run without -DryRun to create files" -ForegroundColor Yellow
}
