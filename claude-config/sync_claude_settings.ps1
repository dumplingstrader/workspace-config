# sync_claude_settings.ps1
#
# Copies this repo's canonical Claude Code user settings into place on the
# current workstation. Run after `git pull` on any machine to pick up
# changes made elsewhere. Backs up the existing file first (never deletes
# it outright).
#
# Usage:
#   powershell -File sync_claude_settings.ps1

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$source = Join-Path $repoRoot "settings.user.json"
$targetDir = Join-Path $env:USERPROFILE ".claude"
$target = Join-Path $targetDir "settings.json"

if (-not (Test-Path $source)) {
    Write-Output "[!] Source file not found: $source"
    exit 1
}

if (-not (Test-Path $targetDir)) {
    New-Item -ItemType Directory -Force -Path $targetDir | Out-Null
}

if (Test-Path $target) {
    $backup = Join-Path $targetDir "settings.json.bak"
    Copy-Item -Path $target -Destination $backup -Force
    Write-Output "[OK] Backed up existing settings to $backup"
}

Copy-Item -Path $source -Destination $target -Force
Write-Output "[OK] Synced $source -> $target"
Write-Output "Permission rules reload live -- no restart needed for a running session."
