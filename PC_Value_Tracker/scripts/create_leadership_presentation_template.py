"""
Create Leadership Presentation PowerPoint Template
===================================================
Generates a professional PowerPoint template for presenting
technical assistance value to leadership.

Template follows modern corporate design with:
- Title slide
- Executive summary
- Key metrics dashboard
- System breakdown charts
- Success stories
- Call to action / recommendations

Usage:
    python scripts/create_leadership_presentation_template.py

Outputs: templates/Leadership_Presentation_Template.pptx
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pathlib import Path


# Design colors - Professional teal and gray palette
PRIMARY_COLOR = RGBColor(94, 168, 167)      # Teal #5EA8A7
SECONDARY_COLOR = RGBColor(39, 120, 132)   # Deep Teal #277884
ACCENT_COLOR = RGBColor(254, 68, 71)       # Coral #FE4447
DARK_TEXT = RGBColor(28, 40, 51)           # Dark Blue-Gray #1C2833
LIGHT_BG = RGBColor(244, 246, 246)         # Off-White #F4F6F6


def add_title_slide(prs):
    """Slide 1: Title slide."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout
    
    # Background
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = PRIMARY_COLOR
    
    # Main title
    title_box = slide.shapes.add_textbox(
        Inches(0.5), Inches(2.5),
        Inches(9), Inches(1.5)
    )
    title_frame = title_box.text_frame
    title_frame.text = 'Technical Assistance Value Report'
    title_para = title_frame.paragraphs[0]
    title_para.font.size = Pt(44)
    title_para.font.bold = True
    title_para.font.color.rgb = RGBColor(255, 255, 255)
    title_para.alignment = PP_ALIGN.CENTER
    
    # Subtitle
    subtitle_box = slide.shapes.add_textbox(
        Inches(0.5), Inches(4.2),
        Inches(9), Inches(0.8)
    )
    subtitle_frame = subtitle_box.text_frame
    subtitle_frame.text = '[Period: Month/Quarter YYYY]'
    subtitle_para = subtitle_frame.paragraphs[0]
    subtitle_para.font.size = Pt(24)
    subtitle_para.font.color.rgb = RGBColor(255, 255, 255)
    subtitle_para.alignment = PP_ALIGN.CENTER
    
    # Presenter name
    name_box = slide.shapes.add_textbox(
        Inches(0.5), Inches(6.5),
        Inches(9), Inches(0.5)
    )
    name_frame = name_box.text_frame
    name_frame.text = '[Presenter Name] | Process Controls'
    name_para = name_frame.paragraphs[0]
    name_para.font.size = Pt(18)
    name_para.font.color.rgb = RGBColor(255, 255, 255)
    name_para.alignment = PP_ALIGN.CENTER


def add_executive_summary(prs):
    """Slide 2: Executive Summary."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # Title
    title_box = slide.shapes.add_textbox(
        Inches(0.5), Inches(0.5),
        Inches(9), Inches(0.6)
    )
    title_frame = title_box.text_frame
    title_frame.text = 'Executive Summary'
    title_para = title_frame.paragraphs[0]
    title_para.font.size = Pt(32)
    title_para.font.bold = True
    title_para.font.color.rgb = PRIMARY_COLOR
    
    # Content boxes
    content = [
        ('Key Achievements', '[Highlight top 2-3 accomplishments]'),
        ('Notable Trends', '[1-2 patterns observed]'),
        ('Strategic Impact', '[How this work supports business goals]')
    ]
    
    y_pos = 1.5
    for heading, placeholder in content:
        # Heading
        heading_box = slide.shapes.add_textbox(
            Inches(0.8), Inches(y_pos),
            Inches(8.4), Inches(0.4)
        )
        heading_frame = heading_box.text_frame
        heading_frame.text = heading
        heading_para = heading_frame.paragraphs[0]
        heading_para.font.size = Pt(20)
        heading_para.font.bold = True
        heading_para.font.color.rgb = SECONDARY_COLOR
        
        # Content
        content_box = slide.shapes.add_textbox(
            Inches(0.8), Inches(y_pos + 0.45),
            Inches(8.4), Inches(1.0)
        )
        content_frame = content_box.text_frame
        content_frame.text = placeholder
        content_frame.word_wrap = True
        content_para = content_frame.paragraphs[0]
        content_para.font.size = Pt(16)
        content_para.font.color.rgb = DARK_TEXT
        
        y_pos += 1.7


def add_metrics_dashboard(prs):
    """Slide 3: Key Metrics Dashboard."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # Title
    title_box = slide.shapes.add_textbox(
        Inches(0.5), Inches(0.5),
        Inches(9), Inches(0.6)
    )
    title_frame = title_box.text_frame
    title_frame.text = 'Key Metrics'
    title_para = title_frame.paragraphs[0]
    title_para.font.size = Pt(32)
    title_para.font.bold = True
    title_para.font.color.rgb = PRIMARY_COLOR
    
    # Metric cards (2 rows x 3 columns)
    metrics = [
        ('Total Issues', '[#]', 'Technical requests handled'),
        ('Systems Supported', '[#]', 'Different control systems'),
        ('High Complexity', '[#]', 'Major/significant issues'),
        ('Cross-Site Support', '[#]', 'Multi-site coordination'),
        ('Avg Response Time', '[X hours]', 'Time to resolution'),
        ('Uptime Protected', '[X%]', 'Production impact avoided')
    ]
    
    row = 0
    col = 0
    for i, (label, value, description) in enumerate(metrics):
        x = 0.5 + col * 3.2
        y = 1.5 + row * 2.3
        
        # Card background
        card = slide.shapes.add_shape(
            1,  # Rectangle
            Inches(x), Inches(y),
            Inches(3.0), Inches(2.0)
        )
        card.fill.solid()
        card.fill.fore_color.rgb = LIGHT_BG
        card.line.color.rgb = PRIMARY_COLOR
        card.line.width = Pt(2)
        
        # Value (big number)
        value_box = slide.shapes.add_textbox(
            Inches(x + 0.2), Inches(y + 0.3),
            Inches(2.6), Inches(0.7)
        )
        value_frame = value_box.text_frame
        value_frame.text = value
        value_para = value_frame.paragraphs[0]
        value_para.font.size = Pt(36)
        value_para.font.bold = True
        value_para.font.color.rgb = ACCENT_COLOR
        value_para.alignment = PP_ALIGN.CENTER
        
        # Label
        label_box = slide.shapes.add_textbox(
            Inches(x + 0.2), Inches(y + 1.0),
            Inches(2.6), Inches(0.4)
        )
        label_frame = label_box.text_frame
        label_frame.text = label
        label_para = label_frame.paragraphs[0]
        label_para.font.size = Pt(14)
        label_para.font.bold = True
        label_para.font.color.rgb = DARK_TEXT
        label_para.alignment = PP_ALIGN.CENTER
        
        # Description
        desc_box = slide.shapes.add_textbox(
            Inches(x + 0.2), Inches(y + 1.4),
            Inches(2.6), Inches(0.4)
        )
        desc_frame = desc_box.text_frame
        desc_frame.text = description
        desc_frame.word_wrap = True
        desc_para = desc_frame.paragraphs[0]
        desc_para.font.size = Pt(10)
        desc_para.font.color.rgb = DARK_TEXT
        desc_para.alignment = PP_ALIGN.CENTER
        
        col += 1
        if col == 3:
            col = 0
            row += 1


def add_system_breakdown(prs):
    """Slide 4: System Breakdown Chart."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # Title
    title_box = slide.shapes.add_textbox(
        Inches(0.5), Inches(0.5),
        Inches(9), Inches(0.6)
    )
    title_frame = title_box.text_frame
    title_frame.text = 'Issues by System'
    title_para = title_frame.paragraphs[0]
    title_para.font.size = Pt(32)
    title_para.font.bold = True
    title_para.font.color.rgb = PRIMARY_COLOR
    
    # Chart placeholder
    chart_box = slide.shapes.add_textbox(
        Inches(1.5), Inches(2.0),
        Inches(7), Inches(4)
    )
    chart_frame = chart_box.text_frame
    chart_frame.text = '[INSERT CHART HERE]\n\n' \
                      'Recommended: Bar chart or pie chart showing\n' \
                      'distribution of issues across control systems'
    chart_para = chart_frame.paragraphs[0]
    chart_para.font.size = Pt(18)
    chart_para.font.italic = True
    chart_para.font.color.rgb = SECONDARY_COLOR
    chart_para.alignment = PP_ALIGN.CENTER


def add_success_stories(prs):
    """Slide 5: Success Stories / Impact Examples."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # Title
    title_box = slide.shapes.add_textbox(
        Inches(0.5), Inches(0.5),
        Inches(9), Inches(0.6)
    )
    title_frame = title_box.text_frame
    title_frame.text = 'Success Stories'
    title_para = title_frame.paragraphs[0]
    title_para.font.size = Pt(32)
    title_para.font.bold = True
    title_para.font.color.rgb = PRIMARY_COLOR
    
    # Story cards
    stories = [
        ('Major Issue Resolved', '[Brief description of complex problem solved]',
         'Impact: [Production saved, downtime avoided, cost savings]'),
        ('Cross-Site Collaboration', '[Example of multi-site coordination]',
         'Impact: [Standardization achieved, best practices shared]'),
        ('Training & Knowledge Transfer', '[How you enabled others]',
         'Impact: [Team capability improved, self-sufficiency increased]')
    ]
    
    y_pos = 1.5
    for title, description, impact in stories:
        # Story card background
        card = slide.shapes.add_shape(
            1,  # Rectangle
            Inches(0.8), Inches(y_pos),
            Inches(8.4), Inches(1.3)
        )
        card.fill.solid()
        card.fill.fore_color.rgb = LIGHT_BG
        card.line.color.rgb = SECONDARY_COLOR
        card.line.width = Pt(1)
        
        # Title
        title_box = slide.shapes.add_textbox(
            Inches(1.0), Inches(y_pos + 0.1),
            Inches(8.0), Inches(0.3)
        )
        title_frame = title_box.text_frame
        title_frame.text = title
        title_para = title_frame.paragraphs[0]
        title_para.font.size = Pt(16)
        title_para.font.bold = True
        title_para.font.color.rgb = SECONDARY_COLOR
        
        # Description
        desc_box = slide.shapes.add_textbox(
            Inches(1.0), Inches(y_pos + 0.45),
            Inches(8.0), Inches(0.35)
        )
        desc_frame = desc_box.text_frame
        desc_frame.text = description
        desc_para = desc_frame.paragraphs[0]
        desc_para.font.size = Pt(12)
        desc_para.font.color.rgb = DARK_TEXT
        
        # Impact
        impact_box = slide.shapes.add_textbox(
            Inches(1.0), Inches(y_pos + 0.85),
            Inches(8.0), Inches(0.3)
        )
        impact_frame = impact_box.text_frame
        impact_frame.text = impact
        impact_para = impact_frame.paragraphs[0]
        impact_para.font.size = Pt(12)
        impact_para.font.italic = True
        impact_para.font.color.rgb = ACCENT_COLOR
        
        y_pos += 1.5


def add_recommendations(prs):
    """Slide 6: Recommendations / Call to Action."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # Title
    title_box = slide.shapes.add_textbox(
        Inches(0.5), Inches(0.5),
        Inches(9), Inches(0.6)
    )
    title_frame = title_box.text_frame
    title_frame.text = 'Recommendations'
    title_para = title_frame.paragraphs[0]
    title_para.font.size = Pt(32)
    title_para.font.bold = True
    title_para.font.color.rgb = PRIMARY_COLOR
    
    # Recommendations list
    recommendations = [
        'Invest in [training/equipment/resources]',
        'Standardize [process/documentation]',
        'Expand support to [new area/system]',
        'Schedule regular [reviews/maintenance]'
    ]
    
    y_pos = 1.8
    for i, rec in enumerate(recommendations, 1):
        # Number circle
        circle = slide.shapes.add_shape(
            9,  # Oval
            Inches(1.0), Inches(y_pos),
            Inches(0.4), Inches(0.4)
        )
        circle.fill.solid()
        circle.fill.fore_color.rgb = ACCENT_COLOR
        circle.line.color.rgb = ACCENT_COLOR
        
        # Number text
        num_box = slide.shapes.add_textbox(
            Inches(1.0), Inches(y_pos),
            Inches(0.4), Inches(0.4)
        )
        num_frame = num_box.text_frame
        num_frame.text = str(i)
        num_para = num_frame.paragraphs[0]
        num_para.font.size = Pt(18)
        num_para.font.bold = True
        num_para.font.color.rgb = RGBColor(255, 255, 255)
        num_para.alignment = PP_ALIGN.CENTER
        
        # Recommendation text
        text_box = slide.shapes.add_textbox(
            Inches(1.6), Inches(y_pos),
            Inches(7.2), Inches(0.6)
        )
        text_frame = text_box.text_frame
        text_frame.text = rec
        text_frame.word_wrap = True
        text_para = text_frame.paragraphs[0]
        text_para.font.size = Pt(18)
        text_para.font.color.rgb = DARK_TEXT
        
        y_pos += 0.9


def add_questions_slide(prs):
    """Slide 7: Questions slide."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # Background
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = SECONDARY_COLOR
    
    # Questions text
    questions_box = slide.shapes.add_textbox(
        Inches(0.5), Inches(3.0),
        Inches(9), Inches(1.5)
    )
    questions_frame = questions_box.text_frame
    questions_frame.text = 'Questions?'
    questions_para = questions_frame.paragraphs[0]
    questions_para.font.size = Pt(60)
    questions_para.font.bold = True
    questions_para.font.color.rgb = RGBColor(255, 255, 255)
    questions_para.alignment = PP_ALIGN.CENTER
    
    # Contact info
    contact_box = slide.shapes.add_textbox(
        Inches(0.5), Inches(5.0),
        Inches(9), Inches(0.5)
    )
    contact_frame = contact_box.text_frame
    contact_frame.text = '[Your Name] | [Email] | [Phone]'
    contact_para = contact_frame.paragraphs[0]
    contact_para.font.size = Pt(18)
    contact_para.font.color.rgb = RGBColor(255, 255, 255)
    contact_para.alignment = PP_ALIGN.CENTER


def create_template():
    """Generate complete PowerPoint template."""
    
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(7.5)
    
    print("\n" + "="*60)
    print("Creating Leadership Presentation Template")
    print("="*60)
    
    print("\n📊 Adding slides:")
    
    add_title_slide(prs)
    print("  ✓ Slide 1: Title")
    
    add_executive_summary(prs)
    print("  ✓ Slide 2: Executive Summary")
    
    add_metrics_dashboard(prs)
    print("  ✓ Slide 3: Key Metrics Dashboard")
    
    add_system_breakdown(prs)
    print("  ✓ Slide 4: System Breakdown")
    
    add_success_stories(prs)
    print("  ✓ Slide 5: Success Stories")
    
    add_recommendations(prs)
    print("  ✓ Slide 6: Recommendations")
    
    add_questions_slide(prs)
    print("  ✓ Slide 7: Questions")
    
    # Save presentation
    output_path = Path('templates/Leadership_Presentation_Template.pptx')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    prs.save(output_path)
    
    print("\n" + "="*60)
    print("✓ Presentation template saved:")
    print(f"  {output_path}")
    print("\n📋 Template structure:")
    print("  1. Title slide (customize period and name)")
    print("  2. Executive summary (key achievements)")
    print("  3. Metrics dashboard (6 key metrics)")
    print("  4. System breakdown (chart placeholder)")
    print("  5. Success stories (3 impact examples)")
    print("  6. Recommendations (4 action items)")
    print("  7. Questions (contact info)")
    print("\n🎨 Design: Professional teal and coral palette")
    print("📝 All placeholder text marked with [brackets]")
    print("="*60)


if __name__ == '__main__':
    create_template()
