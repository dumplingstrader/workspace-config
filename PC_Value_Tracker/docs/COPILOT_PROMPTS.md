# Copilot Prompts for Process Controls Value Tracking

**Purpose:** Extract specific, detailed issue data from Outlook emails for workload documentation and value demonstration.

**Author:** Tony Chiu  
**Created:** January 2026

---

## How to Use These Prompts

1. Open Microsoft Copilot in Outlook or Teams
2. Copy the appropriate prompt below
3. Adjust the date range as needed
4. Review and refine results
5. Export to your tracking system

---

## Prompt 1: Weekly Issue Extraction (Recommended - Run Weekly)

Use this prompt every Friday to capture the week's work:

```
Search my sent emails from the past 7 days. For each email that involves troubleshooting, problem resolution, or technical support, extract the following information in a table format:

| Date | Subject | Requester | System/Equipment | Issue Summary | Resolution | Time Indicator | Request Source |

For each field:
- Date: When the email was sent
- Subject: Email subject line
- Requester: Who asked for help or reported the issue (person or group)
- System/Equipment: What system was involved (e.g., Experion, PLC-5, Triconex, DynAMo, graphics, alarms)
- Issue Summary: Brief description of the problem (1-2 sentences)
- Resolution: How it was resolved OR current status (fixed, handed off, pending, escalated)
- Time Indicator: Any mention of time spent or urgency (e.g., "spent 2 hours", "emergency", "quick fix")
- Request Source: Where the request came from (PLC_SIS email group, direct request, Operations, Projects, AMP, etc.)

Focus on emails where I provided technical assistance, troubleshooting, problem solving, or coordination. Skip routine administrative emails, meeting invites, and FYI-only messages.

Format as a table I can copy to Excel.
```

### FOLLOW-UP: Fill in Time Indicators

If many entries have incomplete "Time Indicator" data, use this follow-up:

```
For entries in the previous table where Time Indicator is incomplete or unclear, please infer the time/effort based on:

1. Email thread length (number of back-and-forth messages)
2. Time span between first message and resolution
3. Keywords indicating effort ("investigating", "urgent", "troubleshooting", "spent", "working on")
4. Complexity of the issue described

Estimate as: Quick fix (<1hr), Moderate (1-4hr), Significant (4-8hr), Major effort (8+hr), or Ongoing/Multi-day

Update the table with these estimates.
```

---

## General Tips for Running All Prompts

### Running for Multiple Time Periods
- Be specific with date ranges: "January 1, 2024 to December 31, 2024"
- For historical data, run separately by year or quarter
- Label each export with the date range (e.g., "2024_Weekly.xlsx")

### Handling Incomplete Data
If Copilot returns incomplete fields, use this follow-up:
```
For entries with missing or unclear [FIELD_NAME], please infer the most likely value based on email content and context.
```

### If Results Are Too Large
If Copilot indicates too many results:
- Break into smaller date ranges (weekly or monthly)
- Add more specific keywords to narrow focus
- Ask for "top 50 most significant" first

### Exporting Results
Always specify format at the end of your prompt:
- "Format as a table I can copy to Excel"
- "Export as CSV format"

---

## Prompt 2: Monthly Summary by Category

Run at end of month to see patterns:

```
Search my sent emails from the past 30 days. Categorize all technical support and troubleshooting emails into these categories:

1. **Alarm Management** - DynAMo, ACM, alarm configuration, nuisance alarms, alarm rationalization
2. **PLC/SIS Issues** - ControlLogix, PLC-5, Triconex, safety systems, interlocks
3. **DCS/Experion** - Experion, TDC, C300, controllers, servers
4. **HMI/Graphics** - Console displays, graphics issues, operator stations, screen performance
5. **Network/Infrastructure** - OPC, communication, servers, connectivity
6. **Vendor Coordination** - Honeywell, Schneider, GE support cases, TAC escalations
7. **Project Support** - AMP, capital projects, MOC, commissioning
8. **Training/Documentation** - Knowledge transfer, procedures, how-to questions

For each category, provide:
- Count of emails
- Brief summary of main issues
- Any recurring problems
- Notable time-intensive items

Also flag any emails that mention:
- "AMP" or "console upgrade" or "modernization"
- Legacy equipment (PLC-5, SLC-500, TDC)
- Urgent/emergency situations
- Issues that were NOT Process Controls responsibility (handed off to Electrical, Mechanical, etc.)
```

---

## Prompt 3: AMP-Related Issue Extraction

Use to specifically capture AMP project burden:

```
Search my sent emails from the past 90 days for any emails related to:
- AMP (Automation Modernization Program)
- Console upgrades
- TDC to Experion migration
- C300 cutover
- Graphics migration
- ASM (Abnormal Situation Management)
- New HMI issues
- Post-project problems
- Contractor deliverables
- FAT/SAT issues

For each email found, extract:

| Date | Issue | Root Cause | Was This Preventable? | Time Spent | Status |

Where:
- Root Cause: What caused the issue (contractor quality, rushed timeline, ignored feedback, design flaw, etc.)
- Was This Preventable: Yes/No - Could this have been caught during project delivery?
- Time Spent: Any indication of effort required
- Status: Resolved, ongoing, escalated, or accepted as-is
```

---

## Prompt 4: "Not Our Problem" Tracking

Use to capture diagnostic work that gets handed off:

```
Search my sent emails from the past 30 days where I:
- Determined an issue was NOT a Process Controls problem
- Handed off an issue to another group (Electrical, Mechanical, Maintenance, IT, Projects)
- Helped diagnose a problem even though it wasn't our responsibility
- Provided guidance but the fix was someone else's job

For each, extract:

| Date | Original Request | My Diagnosis | Actual Root Cause | Handed Off To | Time Spent Diagnosing |

This captures the "invisible work" of troubleshooting issues that turn out to be someone else's responsibility.
```

---

## Prompt 5: Recurring Issues Identification

Use monthly to spot patterns:

```
Search my sent emails from the past 90 days. Identify any issues that appear multiple times - same system, same problem, or same requester asking about similar things.

Group recurring issues by:
1. System/Equipment - What keeps breaking?
2. Root Cause - What's the underlying problem?
3. Frequency - How often does this come up?
4. Permanent Fix Possible? - Is there a way to eliminate this recurring issue?

Flag any issues that:
- Have occurred 3+ times
- Involve obsolete equipment (PLC-5, SLC, TDC)
- Were identified during AMP but not fixed
- Require a capital project to permanently resolve
```

---

## Alternative: PowerShell Direct Extraction for RCA Emails

If Copilot has difficulty extracting root cause analysis emails, use this PowerShell script:

**Save as `extract_rca_emails.ps1` and run:** `.\extract_rca_emails.ps1`

```powershell
# Export emails with root cause analysis keywords
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

$cutoff = (Get-Date).AddMonths(-36)  # Last 3 years
$items = $sent.Items
$items.Sort("SentOn", $false)

$count = 0
foreach ($item in $items) {
    try {
        if ($null -eq $item -or -not ($item -is [Microsoft.Office.Interop.Outlook.MailItem])) { continue }
        if ($item.SentOn -lt $cutoff) { break }

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
        $body = ($item.Body -replace "`r|`n", " ")
        if ($body.Length -gt 800) { $body = $body.Substring(0,800) }
        $body = ($body -replace ",", ";")

        $line = "$date,$to,$subj,$body"
        Add-Content -Path $outPath -Value $line
        $count++
    } catch {
        continue
    }
}

Write-Host "Exported $count messages to $outPath"
```

**Results:** CSV file saved to Downloads folder with Date, To, Subject, and Body Preview

---

## Prompt 6: Time Estimation for Past Work

Use to estimate effort on historical issues:

```
For the following list of issues I've worked on, estimate the time spent based on email thread length, complexity, and number of follow-ups:

[Paste your issue list here]

Categorize each as:
- Quick (< 1 hour): Simple answer, one email, routine fix
- Moderate (1-4 hours): Some investigation, multiple emails, coordination needed
- Significant (4-8 hours): Deep troubleshooting, multiple days, vendor involvement
- Major (8+ hours): Extended investigation, site visits, major coordination

Provide reasoning for each estimate.
```

---

## Prompt 7: PLC_SIS Email Group Analysis

Since you monitor the PLC_SIS email group:

```
Search the PLC_SIS email group messages from the past 30 days. For each thread:

| Date | Topic | Who Responded | Response Time | Resolution | Was I Involved? |

Summarize:
- Total threads received
- How many I personally responded to
- How many went unanswered or had delayed responses
- Common themes or recurring questions
- Knowledge gaps indicated (questions that suggest training needs)
```

---

## Tips for Better Results

### Be Specific About Date Ranges
- "past 7 days" for weekly tracking
- "from January 1 to January 31, 2026" for specific periods
- "past 90 days" for pattern analysis

### Refine with Follow-ups
After initial results, ask:
- "Show me more details on item #3"
- "Which of these involved AMP?"
- "Estimate time spent on the top 5 items"

### Export Format
Ask Copilot to format for export:
- "Put this in a table I can paste into Excel"
- "Format as CSV"
- "Create a bullet list summary"

### Combine with Manual Notes
Copilot captures what's in email. Add your own notes for:
- Phone calls and hallway conversations
- Time spent that wasn't documented
- Context that wasn't in the email thread

---

## Data Fields for Value Tracking

When building your tracker, capture these fields:

| Field | Source | Notes |
|-------|--------|-------|
| Date | Email timestamp | When it happened |
| Issue Summary | Email subject/body | What was the problem |
| System | Email body | Experion, PLC, SIS, HMI, etc. |
| Requester | Email from/to | Who asked for help |
| Request Source | Email group or direct | PLC_SIS group, Operations, Projects, etc. |
| Root Cause Category | Your assessment | PC Issue, AMP, Vendor, Mechanical, etc. |
| AMP Related | Keyword flag | Yes/No |
| Obsolete Equipment | Keyword flag | Yes/No |
| Time Spent | Estimate | Hours |
| Resolution | Email body | Fixed, handed off, escalated, pending |
| Was PC Responsible | Your judgment | Yes, No, Partial |
| Business Impact | Your assessment | Production, Safety, Compliance, Efficiency |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Jan 2026 | Initial prompts for value tracking |
