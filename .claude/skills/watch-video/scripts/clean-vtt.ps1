[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$InputPath,

    [Parameter(Mandatory = $true)]
    [string]$OutputPath
)

$resolvedInput = (Resolve-Path -LiteralPath $InputPath -ErrorAction Stop).Path
$outputParent = Split-Path -Parent $OutputPath
if ($outputParent) {
    New-Item -ItemType Directory -Path $outputParent -Force | Out-Null
}

$seen = [System.Collections.Generic.HashSet[string]]::new(
    [System.StringComparer]::Ordinal
)
$lines = [System.Collections.Generic.List[string]]::new()
$inCue = $false

foreach ($rawLine in [System.IO.File]::ReadLines($resolvedInput)) {
    $line = $rawLine.Trim()
    if (-not $line -or $line -eq 'WEBVTT' -or
        $line.StartsWith('Kind:') -or $line.StartsWith('Language:') -or
        $line.StartsWith('NOTE')) {
        continue
    }
    if ($line -match '-->') {
        $inCue = $true
        continue
    }
    if (-not $inCue -or $line -match '^\d+$') {
        continue
    }

    $text = [System.Net.WebUtility]::HtmlDecode(
        ($line -replace '<[^>]+>', '' -replace '\s+', ' ').Trim()
    )
    if ($text -and $seen.Add($text)) {
        $lines.Add($text)
    }
}

[System.IO.File]::WriteAllLines(
    [System.IO.Path]::GetFullPath($OutputPath),
    $lines,
    [System.Text.UTF8Encoding]::new($false)
)

Write-Output ([System.IO.Path]::GetFullPath($OutputPath))
