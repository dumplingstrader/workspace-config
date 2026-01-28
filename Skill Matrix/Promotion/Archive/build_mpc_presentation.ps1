# PowerPoint Presentation Builder for MPC Template
# Creates 15-slide promotion presentation using MPC corporate template

# Open working presentation
$powerpoint = New-Object -ComObject PowerPoint.Application
$powerpoint.Visible = [Microsoft.Office.Core.MsoTriState]::msoTrue

$filepath = Join-Path $PWD "working.pptx"
$presentation = $powerpoint.Presentations.Open($filepath)

Write-Host "Building presentation with MPC template..." -ForegroundColor Cyan
Write-Host "Total slides: $($presentation.Slides.Count)" -ForegroundColor Gray

# Slide content array
$slideContent = @(
    @{
        Title = "Site Lead Process Controls Engineer`nA Case for Readiness"
        Content = "Tony Chiu`nSenior Process Controls Engineer`nJanuary 30, 2026`n`nPurpose: Seeking your recommendation on path forward"
    },
    @{
        Title = "Today's Objective"
        Content = "What I'm Asking For:`n• Your assessment of my readiness for Site Lead PCS Engineer role`n• Identification of any gaps you see`n• Guidance on next steps - development plan or recommendation to PCG Technologist/Chris`n`nWhat I'm NOT Asking For:`n• An immediate promotion decision (I understand this is a multi-step process)`n• Special treatment or shortcuts`n`nMy Goal: Earn your recommendation to move this conversation forward"
    },
    @{
        Title = "How I Understand the Site Lead PCS Role"
        Content = "Based on MPC's expectations, a Site Lead PCS Engineer:`n`n• Technical Authority: Multi-site platform ownership, escalation point`n• Corporate Influence: Shapes enterprise standards, represents site`n• Business Leadership: Owns budgets, vendor relationships, strategic planning`n• Crisis Management: Leads high-complexity technical problem-solving`n• Talent Development: Mentors team, builds capability for the future`n• Cross-Functional Leadership: Aligns Operations, Engineering, IT, Safety, Finance`n`nQuestion for you: Does this align with how you see the role?"
    },
    @{
        Title = "The Reality—I'm Already Performing at This Level"
        Content = "Over the past 18-24 months, my responsibilities have expanded:`n`n• Multi-site technical authority (Carson, Wilmington + 3 external sites)`n• Corporate alarm governance contributor (Tiger Team)`n• Platform ownership (Integrity, DynAMo, Mark VIe, Safety Manager)`n• Budget/vendor management ($2M+ annual licensing, multi-year contracts)`n• Training program development (Python, SIS, PLC—200+ hours)`n• High-risk crisis leadership (LARINT01 rebuild, Mark VIe restoration)`n`nI'm not asking to grow into this role—I'm asking for recognition of the leadership I'm already providing."
    },
    @{
        Title = "Evidence #1: LARINT01 Integrity Platform Ownership"
        Content = "The Challenge: LARINT01 failed catastrophically, complete loss of SIS lifecycle tracking`n`nMy Response:`n• Led complete server rebuild from scratch (6 weeks)`n• Redesigned SFTP/SQL data pipelines for reliability`n• Restored 99%+ uptime and audit-ready compliance`n• Cost avoidance: $150K+ (prevented emergency replacement)`n• Created comprehensive documentation`n`nLeadership Demonstrated:`n✓ Crisis management under pressure`n✓ Deep technical expertise`n✓ Cross-functional coordination`n✓ Strategic thinking (built for sustainability)"
    },
    @{
        Title = "Evidence #2: Corporate Alarm Governance Leadership"
        Content = "The Challenge: MPC needed enterprise-wide alarm management strategy`n`nMy Contributions:`n• Active Tiger Team Contributor: Proposed fixes adopted at multiple sites`n• Multi-Site DynAMo SME: Deployed at Carson, Wilmington; supporting 3 more sites`n• Metrics Architecture: Designed PI-based alarm dashboards for executive visibility`n• Alarm Reduction: 30-50% reduction at deployed sites`n• Standards Development: Contributed to enterprise alarm management playbook`n`nLeadership Demonstrated:`n✓ Corporate-level influence`n✓ Multi-site technical coordination`n✓ Strategic thinking (enterprise standards, not just local fixes)"
    },
    @{
        Title = "Evidence #3: GE Mark VIe Crisis Resolution"
        Content = "The Challenge: Gas turbine control systems experiencing repeated critical failures`n`nMy Response:`n• Led root cause analysis (network latency, firmware mismatch, corrupted HMI)`n• Coordinated GE TAC escalation with detailed technical evidence`n• Implemented remediation (firmware updates, network reconfig, HMI rebuild)`n• Developed training program to address competency gaps`n• Result: Zero unplanned GTG trips since resolution`n`nLeadership Demonstrated:`n✓ High-complexity problem solving`n✓ Vendor relationship management`n✓ Risk mitigation for critical assets"
    },
    @{
        Title = "Evidence #4: Budget & Vendor Strategy Ownership"
        Content = "The Scope:`n• Annual Licensing: $2M+ across Honeywell, Schneider, GE`n• Strategic Planning: 2025-2029 PCG budget (multi-year horizon)`n• Contract Negotiations: 5-year Honeywell renewals, Schneider CFA, GE support`n• Vendor Relationships: Primary technical contact for escalations`n`nThe Impact:`n• Zero licensing lapses or surprise renewals`n• Favorable contract terms through technical credibility`n• Improved cash flow forecasting for Finance`n`nLeadership Demonstrated:`n✓ Business acumen and financial responsibility`n✓ Strategic planning (multi-year horizon)`n✓ Cross-functional coordination"
    },
    @{
        Title = "Evidence #5: Talent Development & Knowledge Transfer"
        Content = "The Challenge: New engineers need 12-18 months to become productive`n`nMy Contributions:`n• Structured Onboarding: Created hands-on training labs (ACM, DynAMo, Integrity, Python, SIS, PLCs)`n• Mentorship: 1:1 guidance for 5+ engineers (technical skills + career development)`n• Training Delivery: 200+ hours across Python, PLC5/SLC/ControlLogix, SIS lifecycle`n• Documentation: Built technical library with troubleshooting guides`n• Result: 50% reduction in time-to-productivity for new hires`n`nLeadership Demonstrated:`n✓ Investment in team's future capability`n✓ Knowledge preservation`n✓ Strategic thinking (building pipeline, not just solving today's problems)"
    },
    @{
        Title = "By the Numbers - Quantified Impact"
        Content = "Sites Supported: 5 (Carson, Wilmington, Salt Lake City, Detroit, Anacortes)`nSystems Owned: 15+ (Integrity, DynAMo x5, Experion, TDC, Mark VIe, Safety Manager)`nAnnual Budget: $2M+ (licensing + multi-year strategic planning)`nCost Avoidance: $150K+ (LARINT01 rebuild alone)`nTraining Hours: 200+ delivered across Python, SIS, PLCs`nEngineers Mentored: 5+ with structured onboarding`nAlarm Reduction: 30-50% at deployed sites`nGTG Reliability: Zero unplanned trips post-Mark VIe resolution"
    },
    @{
        Title = "Stakeholder Validation"
        Content = "Operations: ""DynAMo deployment gave us visibility we never had"" | ""Tony's the person we call when critical systems are down""`n`nSafety: Integrity rebuild restored audit-ready SIS compliance | Training programs improved team's SIS lifecycle knowledge`n`nCorporate Teams: ""Tony's proposed fixes being adopted at other sites"" | PCG recognition of multi-site SME role`n`nVendors (Honeywell, GE, Schneider): Prioritized TAC support due to technical credibility | Invited to contribute to product development`n`nFinance/Supply Chain: Licensing strategy eliminated surprise renewals | Vendor negotiations secured favorable terms"
    },
    @{
        Title = "What I Bring to the Lead Role"
        Content = "Technical Depth:`n✓ Expert across DCS, SIS, alarm management, APC, OT cybersecurity`n✓ Crisis leadership proven under pressure`n✓ Multi-platform fluency`n`nBusiness Acumen:`n✓ Budget ownership and strategic planning`n✓ Vendor negotiation and relationship management`n✓ Cost-benefit analysis and ROI thinking`n`nLeadership Maturity:`n✓ Corporate-level influence and collaboration`n✓ Cross-functional stakeholder alignment`n✓ Talent development and succession planning`n✓ Knowledge preservation and documentation`n`nStrategic Vision:`n✓ Multi-year planning horizon`n✓ Infrastructure modernization initiatives`n✓ Building team capability for future challenges"
    },
    @{
        Title = "Addressing the ""But..."""
        Content = """The role is new—we're still defining it""`n→ I can help shape what this role should be based on work I'm already doing`n`n""You need more corporate visibility""`n→ I'm actively contributing to Tiger Team, supporting 3 external sites, representing MPC at HUG. Where do you see gaps?`n`n""You haven't been in Senior long enough""`n→ I've been performing Lead-level responsibilities for 18-24 months. What specific tenure benchmark?`n`n""We need PCG Technologist alignment""`n→ Absolutely. What's the best way to engage them? Should I present directly or would you prefer to frame the conversation first?`n`nMy Ask: If there are gaps, let's make them specific and addressable—not vague concerns."
    },
    @{
        Title = "The Path Forward—What I Need from You"
        Content = "Today's Decision Points:`n`n1. Assessment: Based on what you've seen, where do I stand relative to Site Lead expectations?`n`n2. Gaps: What specific areas do you see as gaps? (Technical skills? Corporate relationships? People leadership?)`n`n3. Next Steps: What's the path forward?`n   • Option A: Development plan to close identified gaps (with timeline and milestones)`n   • Option B: Recommendation to PCG Technologist for alignment discussion`n   • Option C: Direct recommendation to Chris (if you feel I'm ready)`n`nWhat I Commit To:`n• If gaps exist, I'll build a development plan and execute on it`n• Continued delivery of Lead-level performance`n• Open communication and receptiveness to feedback"
    },
    @{
        Title = "The Bottom Line"
        Content = "I'm not asking for a new role to be created.`nI'm not asking to grow into responsibilities I don't have yet.`n`nI'm asking for recognition of the leadership I'm already providing to MPC every day.`n`nFormalizing the Site Lead role would:`n✓ Enable clearer authority for decisions I'm already making`n✓ Strengthen vendor and cross-site relationships with appropriate title`n✓ Support succession planning and talent development initiatives`n✓ Align my responsibilities with appropriate organizational recognition`n`nThank you for considering this. I'm ready for your feedback and next steps."
    }
)

# Update each slide
for ($i = 1; $i -le 15; $i++) {
    $slide = $presentation.Slides.Item($i)
    $content = $slideContent[$i - 1]
    
    # Update title (shape 1 is usually the title)
    if ($slide.Shapes.Count -ge 1) {
        $slide.Shapes.Item(1).TextFrame.TextRange.Text = $content.Title
    }
    
    # Add content text box if it doesn't exist
    if ($slide.Shapes.Count -lt 2) {
        $textbox = $slide.Shapes.AddTextbox(1, 30, 90, 660, 300)  # msoTextOrientationHorizontal=1
    } else {
        $textbox = $slide.Shapes.Item(2)
    }
    
    $textbox.TextFrame.TextRange.Text = $content.Content
    $textbox.TextFrame.TextRange.Font.Size = 14
    $textbox.TextFrame.WordWrap = $true
    
    Write-Host "✓ Slide $i`: $($content.Title)" -ForegroundColor Green
}

# Save the updated presentation
$outputFile = Join-Path $PWD "Site_Lead_PCS_Engineer_Presentation_01_30_26.pptx"
$presentation.SaveAs($outputFile)

Write-Host "`n✓ Presentation created successfully!" -ForegroundColor Green
Write-Host "   File: Site_Lead_PCS_Engineer_Presentation_01_30_26.pptx" -ForegroundColor Cyan
Write-Host "`nNext step: Open the file and adjust formatting as needed (fonts, colors, bullet points)" -ForegroundColor Yellow

# Close PowerPoint
$presentation.Close()
$powerpoint.Quit()
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($powerpoint) | Out-Null
[System.GC]::Collect()
[System.GC]::WaitForPendingFinalizers()
