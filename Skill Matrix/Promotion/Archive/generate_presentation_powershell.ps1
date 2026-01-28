# PowerPoint Presentation Generator
# Creates Site Lead PCS Engineer promotion presentation

# Create PowerPoint application object
$powerpoint = New-Object -ComObject PowerPoint.Application
$powerpoint.Visible = [Microsoft.Office.Core.MsoTriState]::msoTrue

# Create presentation with 16:9 layout
$presentation = $powerpoint.Presentations.Add()
$presentation.PageSetup.SlideWidth = 720  # 10 inches in points
$presentation.PageSetup.SlideHeight = 405  # 5.625 inches (16:9)

# Color palette
$navyBlue = [System.Drawing.ColorTranslator]::ToOle([System.Drawing.Color]::FromArgb(28, 40, 51))  # #1C2833
$slateGray = [System.Drawing.ColorTranslator]::ToOle([System.Drawing.Color]::FromArgb(46, 64, 83))  # #2E4053
$profBlue = [System.Drawing.ColorTranslator]::ToOle([System.Drawing.Color]::FromArgb(68, 114, 196))  # #4472C4
$gold = [System.Drawing.ColorTranslator]::ToOle([System.Drawing.Color]::FromArgb(191, 154, 74))  # #BF9A4A
$white = [System.Drawing.ColorTranslator]::ToOle([System.Drawing.Color]::White)
$lightGray = [System.Drawing.ColorTranslator]::ToOle([System.Drawing.Color]::FromArgb(244, 246, 246))  # #F4F6F6

Write-Host "Creating slides..." -ForegroundColor Cyan

# Slide 1: Title Slide
$slide1 = $presentation.Slides.Add(1, 12)  # ppLayoutBlank
$slide1.FollowMasterBackground = $false
$slide1.Background.Fill.ForeColor.RGB = $navyBlue
$slide1.Background.Fill.Solid()

$title1 = $slide1.Shapes.AddTextbox(1, 50, 120, 620, 100)
$title1.TextFrame.TextRange.Text = "Site Lead Process Controls Engineer`nA Case for Readiness"
$title1.TextFrame.TextRange.Font.Size = 40
$title1.TextFrame.TextRange.Font.Bold = $true
$title1.TextFrame.TextRange.Font.Color.RGB = $white
$title1.TextFrame.TextRange.Font.Name = "Arial"
$title1.TextFrame.TextRange.ParagraphFormat.Alignment = 2  # Center

$subtitle1 = $slide1.Shapes.AddTextbox(1, 50, 240, 620, 120)
$subtitle1.TextFrame.TextRange.Text = "Tony Chiu`nSenior Process Controls Engineer`nJanuary 30, 2026`n`nPurpose: Seeking your recommendation on path forward"
$subtitle1.TextFrame.TextRange.Font.Size = 16
$subtitle1.TextFrame.TextRange.Font.Color.RGB = $lightGray
$subtitle1.TextFrame.TextRange.Font.Name = "Arial"
$subtitle1.TextFrame.TextRange.ParagraphFormat.Alignment = 2  # Center
Write-Host "✓ Slide 1: Title" -ForegroundColor Green

# Slide 2: Today's Objective
$slide2 = $presentation.Slides.Add(2, 12)  # ppLayoutBlank
$slide2.FollowMasterBackground = $false
$slide2.Background.Fill.ForeColor.RGB = $white
$slide2.Background.Fill.Solid()

$title2 = $slide2.Shapes.AddTextbox(1, 50, 40, 620, 50)
$title2.TextFrame.TextRange.Text = "Today's Objective"
$title2.TextFrame.TextRange.Font.Size = 32
$title2.TextFrame.TextRange.Font.Bold = $true
$title2.TextFrame.TextRange.Font.Color.RGB = $navyBlue
$title2.TextFrame.TextRange.Font.Name = "Arial"

$line2 = $slide2.Shapes.AddLine(50, 95, 670, 95)
$line2.Line.ForeColor.RGB = $profBlue
$line2.Line.Weight = 3

$content2 = $slide2.Shapes.AddTextbox(1, 50, 110, 620, 260)
$content2.TextFrame.TextRange.Text = "What I'm Asking For:
• Your assessment of my readiness for Site Lead PCS Engineer role
• Identification of any gaps you see
• Guidance on next steps—whether that's a development plan or recommendation to PCG Technologist/Chris

What I'm NOT Asking For:
• An immediate promotion decision (I understand this is a multi-step process)
• Special treatment or shortcuts

My Goal: Earn your recommendation to move this conversation forward"
$content2.TextFrame.TextRange.Font.Size = 14
$content2.TextFrame.TextRange.Font.Color.RGB = $slateGray
$content2.TextFrame.TextRange.Font.Name = "Arial"
Write-Host "✓ Slide 2: Today's Objective" -ForegroundColor Green

# Slide 3: Role Understanding
$slide3 = $presentation.Slides.Add(3, 12)
$slide3.FollowMasterBackground = $false
$slide3.Background.Fill.ForeColor.RGB = $white
$slide3.Background.Fill.Solid()

$title3 = $slide3.Shapes.AddTextbox(1, 50, 40, 620, 50)
$title3.TextFrame.TextRange.Text = "How I Understand the Site Lead PCS Role"
$title3.TextFrame.TextRange.Font.Size = 28
$title3.TextFrame.TextRange.Font.Bold = $true
$title3.TextFrame.TextRange.Font.Color.RGB = $navyBlue
$title3.TextFrame.TextRange.Font.Name = "Arial"

$line3 = $slide3.Shapes.AddLine(50, 85, 670, 85)
$line3.Line.ForeColor.RGB = $profBlue
$line3.Line.Weight = 3

$content3 = $slide3.Shapes.AddTextbox(1, 50, 100, 620, 270)
$content3.TextFrame.TextRange.Text = "Based on MPC's expectations, a Site Lead PCS Engineer:

• Technical Authority: Multi-site platform ownership, escalation point
• Corporate Influence: Shapes enterprise standards, represents site
• Business Leadership: Owns budgets, vendor relationships, strategic planning
• Crisis Management: Leads high-complexity technical problem-solving
• Talent Development: Mentors team, builds capability for the future
• Cross-Functional Leadership: Aligns Operations, Engineering, IT, Safety, Finance

Question for you: Does this align with how you see the role?"
$content3.TextFrame.TextRange.Font.Size = 13
$content3.TextFrame.TextRange.Font.Color.RGB = $slateGray
$content3.TextFrame.TextRange.Font.Name = "Arial"
Write-Host "✓ Slide 3: Role Understanding" -ForegroundColor Green

# Save presentation
$filename = "Site_Lead_PCS_Engineer_Presentation_01_30_26.pptx"
$filepath = Join-Path $PWD $filename
$presentation.SaveAs($filepath)
Write-Host "`n✓ Presentation created successfully: $filename" -ForegroundColor Green

# Close PowerPoint
$presentation.Close()
$powerpoint.Quit()
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($powerpoint) | Out-Null
[System.GC]::Collect()
[System.GC]::WaitForPendingFinalizers()

Write-Host "`nNote: This is a simplified version with 3 slides. For the complete 15-slide presentation," -ForegroundColor Yellow
Write-Host "consider using the Node.js-based approach or manually adding remaining slides in PowerPoint." -ForegroundColor Yellow
