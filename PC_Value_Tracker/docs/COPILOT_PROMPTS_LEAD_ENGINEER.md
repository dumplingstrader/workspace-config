# Copilot Prompts — Lead Engineer Value Demonstration

**Purpose:** Extract comprehensive issue data that demonstrates Lead Engineer-level impact over multiple years.

**Author:** Tony Chiu  
**Date:** January 2026

---

## Strategy: Prove Lead Engineer Impact

You need data showing:
1. **Volume** — You handle significant workload
2. **Scope** — Multi-system, multi-area, multi-site expertise
3. **Complexity** — Not just break-fix, but root cause analysis, vendor coordination, cross-functional leadership
4. **Duration** — You've been doing this consistently for years
5. **Impact** — Business outcomes, not just technical fixes

---

## Time Ranges to Cover

| Period | Purpose | Prompt Focus |
|--------|---------|--------------|
| **2023** | Historical depth | Major issues, cross-site work |
| **2024** | AMP year | Project support burden, quality issues |
| **2025** | Recent excellence | Current state, ongoing leadership |
| **2026 YTD** | Fresh evidence | What you're doing right now |

Run each prompt for each year, or use "past 3 years" for combined extraction.

---

## PROMPT 1: Comprehensive Issue Extraction (Full History)

Use this to get the broadest picture:

```
Search my sent emails from [START DATE] to [END DATE]. For each email where I provided technical assistance, troubleshooting, problem resolution, root cause analysis, vendor coordination, training, or cross-functional support, extract:

| Date | Subject | Requester | Requester_Dept | System | Area_Unit | Issue_Summary | My_Role | Resolution | Complexity |

Where:
- Date: Email sent date
- Subject: Email subject line
- Requester: Who needed help (person, group, or department)
- Requester_Dept: Operations, Projects, Maintenance, Engineering, Corporate, Other Site
- System: Experion, TDC, PLC, SIS, HMI, Alarms, DynAMo, Integrity, Network, APC, Server, Other
- Area_Unit: FCC, Coker, Alkylation, Utilities, FCCU, Sulfur, Offsites, Plantwide, Multi-site, Corporate
- Issue_Summary: Brief description (1-2 sentences)
- My_Role: Led, Assisted, Consulted, Trained, Escalated, Coordinated
- Resolution: Fixed, Resolved, Handed off, Escalated to vendor, Documented, Training provided, Process improved
- Complexity: Quick (<1hr), Moderate (1-4hr), Significant (4-8hr), Major (8+hr), Ongoing/Multi-day

Focus on emails showing technical leadership, not routine administrative messages.

Format as a table I can copy to Excel.
```

**Run this for:**
- January 2023 - December 2023
- January 2024 - December 2024
- January 2025 - December 2025
- January 2026 - Present

### FOLLOW-UP: Fill in Complexity TBD Values

After Copilot returns the initial table, use this follow-up prompt to estimate complexity:

```
For the entries in the previous table where Complexity is marked as TBD, please infer the complexity level based on:

1. Email thread length (number of back-and-forth messages)
2. Time span between first message and resolution
3. Keywords indicating effort or urgency ("investigating", "working on", "urgent", "troubleshooting", "multiple attempts", "escalated")
4. Number of people involved in the thread
5. Mention of site visits, vendor calls, or extended coordination

Use these criteria:
- Quick (<1hr): Single email or quick reply, routine fix, no follow-up needed
- Moderate (1-4hr): 2-4 email exchanges, same-day resolution, some investigation
- Significant (4-8hr): 5+ emails or multi-day thread, vendor involvement, or cross-functional coordination
- Major (8+hr): Extended investigation, multiple days/weeks, site visits, complex RCA
- Ongoing/Multi-day: Explicitly spans multiple days or mentions "ongoing", "continuing to monitor", "long-term"

Update the previous table with estimated Complexity values replacing all TBD entries.
```

---

## General Tips for Running All Prompts

### Running for Multiple Years
When running any prompt for different time periods:
- Be specific with date ranges: "January 1, 2024 to December 31, 2024"
- Run separately for each year to manage result volume
- Label each export with the year (e.g., "2024_Issues.xlsx", "2023_Issues.xlsx")

### Handling TBD or Missing Data
If Copilot returns TBD or incomplete data in any field, use this follow-up:
```
For entries with TBD or missing values in [FIELD_NAME], please infer the most likely value based on email content, context, and patterns in similar emails.
```

### If Results Are Too Large
If Copilot says the result set is too large:
- Break into smaller date ranges (quarterly or monthly)
- Add more specific keywords to narrow focus
- Ask for "top 100 most significant" first, then drill down

### Exporting Results
Always end your prompt with:
- "Format as a table I can copy to Excel"
- OR "Export as CSV format"
- OR "Create a downloadable table"

---

## PROMPT 2: Cross-Site and Corporate Work

This captures your multi-site impact (key for Lead Engineer):

```
Search my sent emails from the past 3 years for any emails involving:
- Other refinery sites (Wilmington, Salt Lake City, Detroit, Anacortes, Galveston Bay, Garyville)
- Corporate teams or corporate SMEs
- Multi-site coordination
- Standards that apply to multiple sites
- Tiger Team or governance work
- Alarm Management across sites
- DynAMo or Integrity systems at multiple locations

For each, extract:
| Date | Sites_Involved | Topic | My_Role | Outcome |

This shows cross-site technical leadership beyond single-site support.
```

---

## PROMPT 3: Vendor and Escalation Coordination

This shows you operate at a level that interfaces with vendors:

```
Search my sent emails from the past 3 years involving:
- Honeywell (TAC cases, support, escalations, product issues)
- Schneider / Triconex support
- Hexagon / Intergraph
- GE support
- Any vendor TAC or support case
- License coordination
- Product defect reporting
- Feature requests

For each, extract:
| Date | Vendor | Issue | My_Role | Resolution | Business_Impact |

This shows vendor relationship management and escalation handling.
```

---

## PROMPT 4: AMP and Major Project Support

Critical for showing project delivery burden:

```
Search my sent emails from 2024 to present for anything related to:
- AMP (Automation Modernization Program)
- Console upgrades
- TDC to Experion migration or cutover
- C300 installations
- Graphics migration or HMI upgrades
- ASM (Abnormal Situation Management)
- FAT (Factory Acceptance Test)
- SAT (Site Acceptance Test)
- Commissioning
- Project handoff issues
- Contractor deliverable quality
- Post-project problems or fixes

For each, extract:
| Date | Project_Phase | Issue | Root_Cause | My_Role | Time_Spent | Was_This_Preventable |

Where Was_This_Preventable = Yes (should have been caught in project) or No (legitimate post-startup issue)
```

---

## PROMPT 5: Training and Knowledge Transfer

Shows mentorship and knowledge leadership:

```
Search my sent emails from the past 3 years where I:
- Provided training (formal or informal)
- Created documentation or procedures
- Answered "how do I..." questions
- Onboarded new team members
- Explained system concepts
- Shared lessons learned
- Developed standards or guidelines

For each, extract:
| Date | Recipient | Topic | Type | Outcome |

Where Type = Formal Training, Documentation, Mentoring, Procedure Development, Standards Work
```

---

## PROMPT 6: High-Complexity Problem Solving

Shows Lead-level technical depth:

```
Search my sent emails from the past 3 years for issues that were:
- Difficult to diagnose
- Required investigation over multiple days
- Involved multiple systems or disciplines
- Required root cause analysis
- Led to permanent fixes or process improvements
- Prevented recurrence of problems

Look for phrases like:
- "root cause"
- "the problem was"
- "it turned out"
- "after investigation"
- "permanently fixed"
- "process improvement"
- "lessons learned"

For each, extract:
| Date | Issue | Investigation_Approach | Root_Cause | Resolution | Improvement_Made |
```

### Alternative: PowerShell Direct Extraction

If Copilot has difficulty with this prompt, use this PowerShell script for direct Outlook extraction:

1. Save this as `extract_rca_emails.ps1`
2. Run in PowerShell: `.\extract_rca_emails.ps1`
3. Results saved to `Downloads\RCA_Export.csv`

```powershell
# Export difficult-investigation emails from Sent Items (last 3 years)
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

$cutoff = (Get-Date).AddMonths(-36)
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

---

## PROMPT 7: PLC_SIS Email Group Leadership

Since you monitor this and few others step up:

```
Search the PLC_SIS email group messages from the past 2 years. Identify threads where I responded or provided guidance.

For each, extract:
| Date | Topic | Was_I_First_Responder | Issue_Type | Resolution |

Also summarize:
- Total threads I responded to
- Topics where I was the primary responder
- Knowledge areas I consistently covered
- Gaps where others didn't respond and I filled in
```

---

## PROMPT 8: Alarm Management Leadership

Your Tiger Team role and alarm expertise:

```
Search my sent emails from the past 3 years involving:
- DynAMo system
- Alarm rationalization
- Alarm management metrics or KPIs
- Nuisance alarm investigation
- Alarm configuration
- Alarm Tiger Team
- Corporate alarm standards
- Site alarm performance

For each, extract:
| Date | Topic | Scope | My_Role | Sites_Affected | Outcome |

This documents alarm management program leadership.
```

---

## How to Compile Results

### Step 1: Run Prompts
Run each prompt (or the ones most relevant) for your target time periods.

### Step 2: Export to Excel
Copy each Copilot result into a separate sheet or combine into one master sheet.

### Step 3: Add Your Judgment
For each entry, add:
- **Time_Spent_Hrs:** Your estimate
- **Root_Cause_Category:** PC Issue, AMP Delivery, Vendor, Obsolete Equipment, Training Gap, Not PC
- **AMP_Related:** Yes/No
- **Was_PC_Job:** Yes/No/Partial
- **Business_Impact:** Production, Safety, Compliance, Efficiency, Low
- **Lead_Engineer_Indicator:** What makes this Lead-level work?

### Step 4: Analyze Patterns
- Total issues by year
- Breakdown by system, area, complexity
- Cross-site vs. single-site
- Vendor escalations handled
- Training/mentorship provided
- AMP burden quantified

---

## Key Metrics for Lead Engineer Case

When you present, highlight:

| Metric | What It Proves |
|--------|----------------|
| **Total issues over 3 years** | Volume and consistency |
| **Multi-site involvement** | Cross-site technical authority |
| **Vendor escalations handled** | External relationship management |
| **Training/mentorship instances** | Knowledge leadership |
| **Complex investigations led** | Technical depth |
| **AMP support burden** | Organizational contribution beyond job description |
| **Time invested** | Commitment and workload |
| **% NOT actually PC issues** | Diagnostic value even when handing off |

---

## Sample Findings to Aim For

> "Over the past 3 years, I documented 500+ technical support interactions:
> - 40% involved cross-functional coordination
> - 15% required vendor escalation that I managed
> - 25+ instances of training or mentorship
> - 80+ hours supporting AMP that could have been avoided with better project delivery
> - Work spanning 5 sites, not just local support
> - Consistent coverage of PLC_SIS group when others don't respond"

---

*These prompts are designed to extract evidence of Lead Engineer-level performance, not just senior engineer break-fix work.*
