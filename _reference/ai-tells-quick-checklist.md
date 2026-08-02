# Quick Reference: AI Formatting Tells Checklist

**Use this 2-minute checklist to validate any markdown→DOCX conversion**

---

## SECTION 1: HEADERS (30 seconds)

Quick visual scan while scrolling:

- [ ] **ALL H1 headers** same size, color, weight?
- [ ] **ALL H2 headers** same size, color, weight?
- [ ] **ALL H3 headers** same size, color, weight?
- [ ] **Heading hierarchy visible?** (H1 largest → H2 medium → H3 smallest)
- [ ] **No more than 3 heading levels?** (no H4+)
- [ ] **Only 2 colors used?** (Dark Blue for H1/H2, Light Blue for H3)

**If ANY fail:** ❌ REJECT - Rerun with `--reference-doc=template.docx`

---

## SECTION 2: BODY TEXT (30 seconds)

Pick any paragraph and check:

- [ ] **Font:** Calibri (NOT Arial, Times New Roman, Georgia)
- [ ] **Size:** 11pt (NOT 10pt, 12pt, 13pt)
- [ ] **Line spacing:** 1.15pt (NOT single, double, or 1.5)
- [ ] **Paragraph spacing:** 6pt after (NOT 0pt, NOT 12pt)
- [ ] **Alignment:** Left (NOT justified)

**If ANY fail:** ❌ REJECT - Check template application

---

## SECTION 3: LISTS (1 minute)

Find any bulleted list and check:

- [ ] **Level 1 indent:** 0.25" (consistent across ALL lists)
- [ ] **Level 2 indent:** 0.5" (consistent across ALL lists)
- [ ] **Level 1 bullet style:** • (same for entire document)
- [ ] **Level 2 bullet style:** ◦ (same for entire document)
- [ ] **No more than 3 levels?** (no 4th level nesting)
- [ ] **Spacing after Level 1:** 6pt (NOT 0pt, NOT 12pt)
- [ ] **Spacing after Level 2:** 3pt (NOT 0pt, NOT 6pt)

**If ANY fail:** ❌ REJECT - Lists need style standardization

---

## SECTION 4: EMPHASIS (30 seconds)

Scan for text formatting:

- [ ] **NO text is BOTH bold AND italic?** (no ***term***)
- [ ] **Bold used ONLY for:** First mention of concepts, defined terms
- [ ] **Italic used ONLY for:** Foreign words, Latin phrases
- [ ] **NO underlined text?** (except hyperlinks - automatic)
- [ ] **Consistent emphasis pattern?** (all similar concepts same emphasis)

**If ANY fail:** ❌ REJECT - Random emphasis is AI tell #5

---

## SECTION 5: TABLES (1 minute)

Find any table and check:

- [ ] **Header row has dark background?** (Dark Blue preferred)
- [ ] **Header text is white?** (NOT black on dark background)
- [ ] **Body rows alternate white/light gray?**
- [ ] **ALL tables use SAME style?** (not different colors per table)
- [ ] **Consistent cell padding?** (0.05" top/bottom, 0.1" left/right)

**If ANY fail:** ❌ REJECT - Tables need styling

---

## SECTION 6: CALLOUT BOXES (30 seconds)

Look for warnings, key takeaways, important notes:

- [ ] **Warnings in red callout box?** (NOT plain text)
- [ ] **Key takeaways in orange/yellow box?** (NOT plain text)
- [ ] **Callout boxes have colored left border?**
- [ ] **Consistent styling across all callouts?**

**If ANY fail:** ⚠️ WARNING - Important info may be missed

---

## SECTION 7: COLORS (30 seconds)

Quick scan of all text colors in document:

- [ ] **Headers use ONLY:** Dark Blue or Light Blue
- [ ] **Body text:** Black ONLY
- [ ] **Total colors used:** 2-3 maximum
- [ ] **No random colors?** (no green, purple, orange in headers)
- [ ] **Color palette consistent?** (H1+H2 same color, H3 different)

**If ANY fail:** ❌ REJECT - Random colors are AI tell #7

---

## SECTION 8: WHITESPACE (30 seconds)

Visual impression:

- [ ] **Document looks readable?** (NOT dense/cramped)
- [ ] **Paragraphs clearly separated?** (breathing room between)
- [ ] **Headings have space before them?** (12pt minimum)
- [ ] **Lists have space between items?** (6pt minimum Level 1)
- [ ] **No solid blocks of text?** (like reading an essay)

**If ANY fail:** ❌ REJECT - Dense paragraphs are AI tell #8

---

## SECTION 9: FONTS (30 seconds)

- [ ] **All body text:** Calibri
- [ ] **All headings:** Calibri
- [ ] **Code blocks ONLY:** Courier New
- [ ] **Total fonts used:** 2 maximum (Calibri + Courier)
- [ ] **NO serif fonts?** (Times New Roman, Georgia = REJECTED)

**If ANY fail:** ❌ REJECT - Mixed fonts are AI tell #3

---

## SECTION 10: TABLE OF CONTENTS (30 seconds)

- [ ] **Document > 10 pages?**
  - [ ] YES → Must have TOC (auto-generated from headers)
  - [ ] NO → Optional but recommended > 5 pages
- [ ] **TOC has page numbers?**
- [ ] **TOC page numbers clickable/linked?**
- [ ] **TOC shows H1-H3 only?** (NOT H4+)

**If fails and > 10 pages:** ❌ REJECT - Add TOC before distribution

---

## SCORING

**Count failures:**

- **0 failures:** ✅ READY - Approve and distribute
- **1-2 failures:** ⚠️ REVIEW - Minor fixes needed (5 min)
- **3+ failures:** ❌ REJECT - Major styling issues (rerun with template)

---

## QUICK FIX: Most Common Issue

**All 3+ fails?** Try this:

```bash
pandoc -f docx -t docx \
  --reference-doc=ACM_APO_Whitepaper_Template.docx \
  -o output_FIXED.docx \
  input.docx
```

This fixes 90% of issues automatically. Re-check after running.

---

## RED FLAGS - IMMEDIATE REJECTION

Stop checking. Reject immediately:

- ❌ Headers in 5+ different sizes
- ❌ Lists with random indentation (0.1", 0.4", 1.2")
- ❌ Mixed fonts (Arial + Calibri + Times New Roman)
- ❌ Entire paragraphs in bold/italic
- ❌ No spacing between paragraphs (dense block)
- ❌ All tables same color (no header distinction)
- ❌ 50-page doc with NO table of contents
- ❌ Document entirely in one color scheme (no hierarchy)

---

## TEMPLATE LOCATION

```
C:\_Documentation\Alarm Reporting\APO\1_Deliverables\
  Whitepaper\Drafts\ACM_APO_Whitepaper_Template.docx
```

## DETAILED INSTRUCTIONS

Read full guidelines in:
- `markdown-to-docx-styling.instructions.md` (14 sections, comprehensive)
- `ai-formatting-tells-examples.md` (before/after examples)

## TIME ESTIMATE

- Quick visual scan: 2 minutes
- Full detailed check: 5-10 minutes
- Complete validation: 15 minutes with detailed checklist

---

**Print this page and post at your desk as a quick reference!**
