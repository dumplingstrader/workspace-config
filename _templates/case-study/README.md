# Case Study Template

Professional case study formatting with consistent styling, properly formatted metrics tables, and strategic page breaks.

## Quick Start

1. **Edit your content:**
   - Open `document.md`
   - Replace title, project info, and content
   - Use provided structure as guide

2. **Generate DOCX:**
   ```powershell
   pandoc -f markdown -t docx --reference-doc="template.docx" -o temp.docx document.md
   python add_page_breaks.py temp.docx temp_breaks.docx
   python fix_table_widths.py temp_breaks.docx document-final.docx
   rm temp.docx temp_breaks.docx
   ```

3. **Convert to PDF:**
   ```powershell
   # Using Word COM (Windows)
   $word = New-Object -ComObject Word.Application
   $word.Visible = $false
   $doc = $word.Documents.Open((Resolve-Path "document-final.docx").Path, $false, $true)
   $doc.SaveAs([ref]$pdfPath, [ref]17)
   $doc.Close()
   $word.Quit()
   ```

## Files in This Template

| File | Purpose |
|------|---------|
| `document.md` | Your markdown source (edit this) |
| `template.docx` | Locked styling template |
| `add_page_breaks.py` | Insert page breaks before H2 sections |
| `fix_table_widths.py` | Format table widths and borders |
| `README.md` | This file |

## Case Study Structure

### Essential Sections

1. **Overview** - Hook the reader with problem + outcome
2. **Challenge** - Provide context and impact
3. **Solution** - Describe methodology and implementation
4. **Results** - Quantify improvements where possible
5. **Lessons Learned** - Be honest about what worked and what didn't
6. **Recommendations** - Guide others in similar situations

### Tips for Effective Case Studies

- **Be specific** - Use real numbers, dates, and names (if appropriate)
- **Tell a story** - Walk readers through the journey
- **Be honest** - Include challenges, not just successes
- **Focus on relevance** - Explain why this case study matters to the audience
- **Use metrics** - Tables showing before/after are powerful
- **Avoid marketing speak** - Let the results speak for themselves

## Markdown Best Practices

### Structure

```markdown
# Project Title (H1)

<div style="page-break-after: always;"></div>

## Major Section (H2) - automatic page break before

### Subsection (H3) - no automatic page break

#### Details (H4) - use sparingly
```

### Tables

Metrics tables are powerful in case studies:

```markdown
| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Response Time | 2 hours | 15 min | 87% faster |
| Error Rate | 12% | 1.2% | 90% reduction |
```

Avoid space-separated text; use pipe syntax only.

### Content Guidelines

- Keep paragraphs varied length (don't all 3 sentences)
- Use **bold** sparingly for key metrics or concepts
- Let numbers/data speak for themselves
- Avoid hype language ("revolutionary", "game-changing")

## Page Breaks

The `add_page_breaks.py` script adds page breaks before each H2 heading. For an 8-12 page case study:
- 1 page break before Challenge
- 1 page break before Solution
- 1 page break before Results
- 1 page break before Lessons Learned

Result: Professional layout with natural section breaks.

## Validation Before Sharing

- [ ] Title/metadata clear and accurate
- [ ] Problem statement compelling and quantified
- [ ] Solution methodology clear and reproducible
- [ ] Results include specific metrics (not vague claims)
- [ ] Lessons learned are honest, not defensive
- [ ] Recommendations are actionable
- [ ] All tables properly formatted with headers
- [ ] No AI tells (mixed fonts, excessive emphasis, generic phrases)

Total validation time: ~15 minutes

## Troubleshooting

**Issue: "pandoc not found"**
```powershell
choco install pandoc
```

**Issue: Tables look like text**
- Make sure you're using `| Column | Data |` syntax
- NOT spaces between data

**Issue: Page breaks in wrong places**
- Check if your section headings are truly H2 (`## Title`)
- H1 and H3 won't get automatic breaks

## Real-World Examples

See the complete workspace for examples:
- ACM-to-APO Migration Whitepaper (technical whitepaper example)
- Document-formatting skill (comprehensive reference)

## Additional Resources

- Complete documentation: `.github/skills/document-formatting/SKILL.md`
- Whitepaper template: `_templates/whitepaper/`
- Pandoc docs: https://pandoc.org/
- python-docx docs: https://python-docx.readthedocs.io/

## Support

Questions or issues? Check:

1. This README troubleshooting section
2. Document-formatting skill for comprehensive guidance
3. Sample templates in `_templates/` for working examples
