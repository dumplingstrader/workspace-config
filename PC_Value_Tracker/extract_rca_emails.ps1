# Export difficult-investigation emails from Sent Items (last 3 years)
# Requires Outlook for Windows (desktop). Leave Outlook open or closed; script will launch COM.

$ErrorActionPreference = "Stop"
Add-Type -AssemblyName Microsoft.Office.Interop.Outlook | Out-Null

$phrases = @(
  "root cause", "the problem was", "it turned out",
  "after investigation", "permanently fixed",
  "process improvement", "lessons learned"
)

$outPath = Join-Path $env:USERPROFILE "Downloads\RCA_Export.csv"
if (Test-Path $outPath) { Remove-Item $outPath -Force }

$excelHeader = "Date,To,Subject,BodyPreview"
[System.IO.File]::WriteAllText($outPath, $excelHeader + "`r`n")

$ol = New-Object -ComObject Outlook.Application
$ns = $ol.GetNamespace("MAPI")
$sent = $ns.GetDefaultFolder([Microsoft.Office.Interop.Outlook.OlDefaultFolders]::olFolderSentMail)

# Date filter: last 36 months
$cutoff = (Get-Date).AddMonths(-36)

# Pull items (Outlook COM doesn't support full-text filter reliably; we post-filter)
$items = $sent.Items
$items.Sort("SentOn", $false)  # newest first

# Iterate and match phrases
$count = 0
foreach ($item in $items) {
    try {
        if ($null -eq $item -or -not ($item -is [Microsoft.Office.Interop.Outlook.MailItem])) { continue }
        if ($item.SentOn -lt $cutoff) { break }  # items sorted desc; safe to break

        $text = (($item.Subject) + " " + ($item.Body)) -as [string]
        if ([string]::IsNullOrWhiteSpace($text)) { continue }

        $hit = $false
        foreach ($p in $phrases) {
            if ($text.IndexOf($p, [System.StringComparison]::OrdinalIgnoreCase) -ge 0) { $hit = $true; break }
        }
        if (-not $hit) { continue }

        $date = $item.SentOn.ToString("yyyy-MM-dd HH:mm")
        $to = ($item.To -replace "`r|`n", " " -replace ",", ";")
        $subj = ($item.Subject -replace "`r|`n", " " -replace ",", ";")
        # Take first 800 characters of body as preview (helps downstream extraction)
        $body = ($item.Body -replace "`r|`n", " ")
        if ($body.Length -gt 800) { $body = $body.Substring(0,800) }
        $body = ($body -replace ",", ";")

        $line = "$date,$to,$subj,$body"
        Add-Content -Path $outPath -Value $line
        $count++
    } catch {
        # continue on individual item errors
        continue
    }
}

Write-Host "Exported $count messages to $outPath"
