# AI Formatting Tells - Before & After Examples

## Overview

This reference document provides **visual examples** of the most common "obvious AI tells" in markdown-to-DOCX conversions and shows how to fix them. Use this alongside `markdown-to-docx-styling.instructions.md`.

---

## 1. Heading Inconsistency - THE MOST COMMON AI TELL

### ❌ **BEFORE (Unprofessional - AI Generated)**

```
# 1. Introduction to Migration
16pt, Black, Bold

## 1.1 Business Context  
14pt, Dark Blue, Bold

### 1.1.1 Strategic Drivers
18pt, Light Blue, Bold

## 1.2 Technical Scope
14pt, Black, Bold (different from 1.1!)

### 1.2.1 Database Systems
11pt, Dark Gray, Bold

# 2. Migration Planning
18pt, Navy Blue, Bold (different from "1"!)

## 2.1 Assessment Phase
12pt, Black, Bold

## 2.2 Execution Phase
16pt, Teal, Bold
```

**Why This Screams "AI":**
- Every heading is different size
- Colors don't follow pattern (Black → Blue → Light Blue → Black → Gray...)
- No visual hierarchy (H1 smaller than some H3s)
- Reader has to work to understand structure
- Looks like document assembled from multiple sources

---

### ✅ **AFTER (Professional - Consistent)**

```
# 1. Introduction to Migration
28pt, Dark Blue RGB(31,78,121), Bold

## 1.1 Business Context  
16pt, Dark Blue RGB(31,78,121), Bold

### 1.1.1 Strategic Drivers
13pt, Light Blue RGB(68,114,196), Bold

## 1.2 Technical Scope
16pt, Dark Blue RGB(31,78,121), Bold

### 1.2.1 Database Systems
13pt, Light Blue RGB(68,114,196), Bold

# 2. Migration Planning
28pt, Dark Blue RGB(31,78,121), Bold

## 2.1 Assessment Phase
16pt, Dark Blue RGB(31,78,121), Bold

## 2.2 Execution Phase
16pt, Dark Blue RGB(31,78,121), Bold
```

**Why This Works:**
- ALL H1 same size/color/weight
- ALL H2 same size/color/weight  
- ALL H3 same size/color/weight
- Clear visual hierarchy: H1 (largest) → H2 (medium) → H3 (smallest)
- Consistent colors: H1+H2 dark blue, H3 light blue
- Reader immediately understands structure
- Professional, publication-ready appearance

---

## 2. List Formatting Chaos - SECOND MOST COMMON AI TELL

### ❌ **BEFORE (Unprofessional - Variable Indentation)**

```
* First topic
  * Sub-topic A
    * Detail 1
  * Sub-topic B
* Second topic
    * Sub-sub-topic (indented more than first sub-topic!)
      * Extra detail
* Third topic
  - Different bullet type!
  - Another item with different bullet
    * Mixed back to asterisk
    * Another item
```

**Problems:**
- Indentation: 0.25" → 0.5" → 1.2" (should be consistent 0.5" increment)
- Sub-topic B indented MORE than Sub-topic A
- Bullet types change: asterisks, then dashes, then asterisks again
- Spacing after items varies (sometimes 0pt, sometimes 6pt)

---

### ✅ **AFTER (Professional - Consistent)**

```
• First topic
  ◦ Sub-topic A
    - Detail 1
  ◦ Sub-topic B
• Second topic
  ◦ Sub-sub-topic (same indent as other Level 2 items)
    - Extra detail
• Third topic
  ◦ Item type 1
  ◦ Item type 2
    - Sub-item under type 2
    - Another sub-item
```

**Standards Applied:**
- Level 1: 0.25" indent, • bullet, 6pt spacing
- Level 2: 0.5" indent, ◦ bullet, 3pt spacing
- Level 3: 0.75" indent, - bullet, 3pt spacing
- Bullet symbols NEVER change within same level
- Every Level 1 item followed by 6pt space
- Every Level 2 item followed by 3pt space

---

## 3. Font & Size Chaos - THIRD MOST COMMON AI TELL

### ❌ **BEFORE (Mixed Fonts & Sizes)**

```
Body text in Calibri 11pt

Some terms in Arial 11pt

Other emphasized text in Times New Roman 12pt

Key concepts sometimes 13pt in Calibri Bold

Other important stuff 11pt but italicized in Georgia

Random text at 10pt in Courier

Code examples in 9pt Arial
```

**Problems:**
- 4 different fonts: Calibri, Arial, Times New Roman, Georgia, Courier
- 5 different sizes: 9pt, 10pt, 11pt, 12pt, 13pt
- Emphasis random: bold, italic, different font, different size
- No pattern—looks like document assembled from different sources
- Reader confused: is this term important because it's larger or different font?

---

### ✅ **AFTER (Single Font, Consistent Sizes)**

```
Body text in Calibri 11pt

Some terms in **bold** (emphasis added via formatting, not font change)

Other emphasized text in *italic* (grammatical emphasis only)

Key concepts in **bold** (same font, just bold)

Important information highlighted in callout box

`Code examples` in Courier New 11pt (monospace ONLY for code)
```

**Standards Applied:**
- Font: Calibri 11pt for all body text (no exceptions)
- Emphasis: **bold** for structural terms, *italic* for foreign words only
- Code: Courier New 11pt (monospace ONLY for code)
- Size variations: Never change font size for emphasis (use bold/italic instead)

---

## 4. Table Styling - PROFESSIONAL VS. PLAIN

### ❌ **BEFORE (Plain, Hard to Read)**

```
| Feature | Description | Priority |
|---------|-------------|----------|
| Authentication | User login system | High |
| Database | Data storage layer | High |
| API | REST endpoints | Medium |
| UI | User interface | Medium |
| Monitoring | System health checks | Low |
| Backup | Data recovery | Low |
```

**How It Renders (Bad):**
- All rows same color (white)
- Header not visually distinct from data
- Hard to scan—rows blur together
- No visual hierarchy
- Looks like hastily-assembled data

---

### ✅ **AFTER (Professional, Easy to Scan)**

```
| Feature | Description | Priority |
|---------|-------------|----------|
| Authentication | User login system | High |
| Database | Data storage layer | High |
| API | REST endpoints | Medium |
| Monitoring | System health checks | Medium |
| Backup | Data recovery | Low |
```

**When Rendered with Template:**
- Header row: Dark Blue background RGB(31,78,121), white text, bold
- Row 1 (Authentication): White background
- Row 2 (Database): Light Gray background RGB(242,242,242)
- Row 3 (API): White background
- Row 4 (Monitoring): Light Gray background
- Row 5 (Backup): White background
- All text: Calibri 11pt, left-aligned
- Alternating rows create clear visual scanning pattern

**Why It Works:**
- Eyes immediately focus on header (dark background)
- Alternating row colors guide reading left-to-right
- No cognitive load—natural eye movement
- Professional appearance

---

## 5. Emphasis Pattern Chaos - RANDOM BOLD/ITALIC

### ❌ **BEFORE (Random Emphasis)**

```
The migration process involves three key phases: ***planning***, **execution**, and *monitoring*. 
Some teams use the term <u>critical path</u> to describe dependencies. 
Data validation is __important__ while communication is *essential* and configuration is ***critical***.
The key insight: don't skip this step!
Conversely, sometimes ***really important concepts*** are emphasized too much.
```

**Problems:**
- "planning" is bold+italic
- "execution" is bold only
- "monitoring" is italic only
- "critical path" is underlined
- "important" is underlined
- "essential" is italic
- "critical" is bold+italic
- "really important concepts" is bold+italic (overdone)
- NO pattern—reader can't tell what emphasis type means

---

### ✅ **AFTER (Consistent Emphasis)**

```
The migration process involves three key phases: **planning**, **execution**, and **monitoring**. 
Some teams use the term "critical path" to describe dependencies. 
**Data validation** is essential while **communication** is critical and **configuration** requires care.
The key insight: don't skip this step!
Conversely, important concepts should use consistent emphasis only when introducing them.
```

**Standards Applied:**
- First mention of concept: **bold** only
- Foreign/Latin terms: *italic* only
- Never mix bold+italic on same term
- "Really important" doesn't mean MORE emphasis—means same emphasis

---

## 6. Paragraph Spacing - DENSE VS. READABLE

### ❌ **BEFORE (Dense, Hard to Read)**

```
[No spacing before this paragraph. Starts at margin.]
The migration process requires careful planning and coordination across multiple teams.
Database administrators must validate data integrity before cutover.
Network engineers need to prepare connectivity for new systems.
Quality assurance teams should develop comprehensive test plans.
[No spacing here either - paragraph immediately follows previous]
All teams should begin preparations immediately to meet the Q3 deadline.
Project managers will coordinate weekly status meetings starting next month.
```

**How It Looks:**
- Solid block of text (like you're reading an essay)
- Paragraphs run into each other
- Eyes get tired
- Feels like a wall of words
- Reader wants to give up

---

### ✅ **AFTER (Professional Spacing)**

```
[6pt spacing before this paragraph adds breathing room]

The migration process requires careful planning and coordination across multiple teams.

[6pt spacing after this paragraph]

Database administrators must validate data integrity before cutover. Network engineers 
need to prepare connectivity for new systems. Quality assurance teams should develop 
comprehensive test plans.

[6pt spacing after this paragraph creates clear break]

All teams should begin preparations immediately to meet the Q3 deadline. Project managers 
will coordinate weekly status meetings starting next month.

[6pt spacing after paragraph]
```

**Standards Applied:**
- 6pt spacing AFTER every paragraph (not before)
- Creates visual breathing room
- Sections clearly separated
- Much more scannable
- Professional appearance

---

## 7. Callout Box Usage - IMPORTANT INFO GETS LOST

### ❌ **BEFORE (Lost in Text)**

```
**WARNING:** This step will delete all temporary files from the system. Make sure you have 
backed up any important data before proceeding. This action cannot be undone.

The deletion process runs in background. You can check progress in the Activity Monitor.
```

**Problem:**
- Warning is just bold text
- Gets lost in sea of other bold text  
- Reader might miss it
- Doesn't convey urgency
- Indistinguishable from regular bold content

---

### ✅ **AFTER (Callout Box)**

```
┌─ CRITICAL WARNING ─────────────────────────────────────────┐
│ This step will delete all temporary files from the system.  │
│ Back up any important data before proceeding. This action   │
│ cannot be undone.                                           │
└───────────────────────────────────────────────────────────────┘

The deletion process runs in background. Check progress in Activity Monitor.
```

**When Rendered with Template:**
- Light red background RGB(255,217,217)
- Red left border (3pt) RGB(255,0,0)
- Dark red text RGB(192,0,0)
- Bold header "CRITICAL WARNING:"
- Stands out immediately
- Reader can't miss it

---

## 8. Color Palette - CHAOS VS. COORDINATED

### ❌ **BEFORE (Random Colors)**

```
Heading 1: Black
Heading 2: Dark Blue
Heading 3: Navy Blue
Heading 4: Purple
Body Text: Black
Emphasized Terms: Red
Important Info: Green
Warnings: Orange
Code: Brown
```

**Problems:**
- 7 different colors with no apparent scheme
- Colors don't communicate hierarchy
- Reader confused: what makes a color choice?
- Looks amateurish, unprofessional
- Hard to track what each color means

---

### ✅ **AFTER (Coordinated Palette)**

```
Heading 1: Dark Blue RGB(31,78,121)
Heading 2: Dark Blue RGB(31,78,121)
Heading 3: Light Blue RGB(68,114,196)
Heading 4: Black RGB(0,0,0)
Body Text: Black RGB(0,0,0)
Warnings: Red RGB(255,0,0)
Key Takeaway: Orange RGB(255,140,0)
Code: Courier New (same color as body text)
```

**Logic:**
- Header colors show hierarchy: Dark → Light → Black
- Only 2 main colors (Dark Blue + Light Blue)
- Accents (Red/Orange) reserved for callouts
- Reader immediately understands: Dark Blue = important, Light Blue = supporting
- Professional, coordinated appearance

---

## 9. Table of Contents - AMATEUR VS. PROFESSIONAL

### ❌ **BEFORE (No TOC)**

```
50-page document

Reader opens page 1, sees "Introduction"

Reader needs "Appendices" information

Reader manually scrolls through 50 pages looking for "Appendices"

Reader gives up, closes document
```

---

### ✅ **AFTER (Automatic TOC)**

```
Page 1: Introduction

Page 2: Table of Contents (auto-generated)
    1. Executive Summary ..................... 3
    2. Migration Scope ...................... 5
    3. Pre-Migration Assessment ............. 8
    ...
    8. Appendices ......................... 45

Page 3-44: Content

Page 45: Appendices (reader navigates directly via TOC link)
```

**Benefits:**
- Reader can jump to any section immediately
- Professional appearance
- Expected in any document > 10 pages
- Auto-generated from headers (no manual maintenance)

---

## 10. Complete Before/After Document

### ❌ **BEFORE (Multiple AI Tells)**

[See markdown formatting - multiple issues compounded]

```markdown
# Migration Strategy

## Overview
This document explains the strategy for migrating from ACM to APO. The key phases
include planning and execution. Teams must be ready for the cutover.

* Planning Phase
  - Assessment
    * Database review
    * System analysis
  - Preparation
    * Develop test plans
    * Train personnel
* Execution Phase
  - Cutover activities
    * Data migration
    * System verification
  - Post-cutover validation

### Critical Warnings
**IMPORTANT** - Backup all data before starting migration
*Key Point* - Test in non-production first
Do NOT skip validation steps

Some systems need special configuration while others don't need much setup.
```

**AI Tells Present:**
- Inconsistent heading sizes
- List indentation varies (0.25" → 0.5" → 1.2")
- Mix of bullet styles (*, -, *)
- Random emphasis: bold, italic, underline, bold+italic
- No spacing between paragraphs
- Warnings not distinguished
- No table of contents

---

### ✅ **AFTER (Professional)**

```markdown
# Migration Strategy

## Overview

This document explains the strategy for migrating from ACM to APO. The key phases 
include **planning** and **execution**. Teams must be ready for the cutover.

## Key Phases

### Planning Phase

* Assessment
  ◦ Database review
  ◦ System analysis
* Preparation
  ◦ Develop test plans
  ◦ Train personnel

### Execution Phase

* Cutover activities
  ◦ Data migration
  ◦ System verification
* Post-cutover validation
  ◦ Validate all systems
  ◦ Confirm data integrity

## Critical Requirements

> **CRITICAL WARNING:** Back up all data before starting migration.
> This step cannot be reversed.

> **KEY TAKEAWAY:** Always test in non-production environments first.
> This practice prevents production issues.

**Data migration** is essential while **system configuration** requires special attention.

Do not skip any validation steps.
```

**Professional Elements:**
- Consistent heading hierarchy
- Proper list indentation (0.25" / 0.5")
- Single bullet type per level
- Consistent emphasis pattern
- Proper spacing between sections
- Callout boxes for warnings
- Clear structure and scanability

---

## Practical Validation Workflow

### Step 1: Open Converted DOCX
- Open in Microsoft Word
- Set zoom to 100%

### Step 2: Visual Scan (30 seconds)
- Do headers look consistent? (same sizes, colors?)
- Do lists look aligned? (or staggered/indented randomly?)
- Is document dense? (paragraphs crammed) or readable? (with spacing)
- Do any tables have styled headers?

### Step 3: Spot Check Sections
**Scan headers:**
- All H1 same size?
- All H2 same size?
- All H3 same size?

**Scan lists:**
- All Level 1 bullets same size?
- All Level 2 sub-bullets indented consistently?

**Scan emphasis:**
- Bold terms consistent?
- No text both bold AND italic?

**Scan colors:**
- Only 2-3 colors used?
- Same colors used consistently?

### Step 4: Full Checklist (5 minutes)
- Use the validation checklist in `markdown-to-docx-styling.instructions.md` Section 11

### Step 5: Fix Any Issues
- Most common: Re-run with `--reference-doc=template.docx` flag
- Template automatically corrects 90% of issues

---

## Red Flags - IMMEDIATE REJECTION

If your document has ANY of these, it's not ready:

- ❌ Headers in different colors/sizes
- ❌ Lists with inconsistent indentation
- ❌ Multiple fonts (Calibri, Arial, Times New Roman mixed)
- ❌ Bold AND italic on same word
- ❌ Underlined text (except links)
- ❌ Dense paragraphs (0pt spacing)
- ❌ Tables with all-white rows
- ❌ No Table of Contents (if > 10 pages)
- ❌ Warnings in plain text (not callout boxes)
- ❌ Text in 6 different colors

---

## Quick Decision Tree

```
Does document look professionally formatted?
├─ YES → Check against validation checklist
│   ├─ All items pass? → Ready to distribute
│   └─ Some items fail? → Fix specific issues
└─ NO → Likely multiple AI tells
    ├─ Re-run with --reference-doc template? → 90% of issues fixed
    └─ Still problems? → Manually fix per checklist
```

---

## Remember

**The Goal:** Make it OBVIOUS that a human reviewed this document and cared about quality.

**The Reality:** AI-generated content often shows tells through inconsistent formatting.

**The Solution:** Apply consistent styling rules and use templates to automate corrections.

**The Result:** Professional, publication-ready documents that don't scream "AI generated."
