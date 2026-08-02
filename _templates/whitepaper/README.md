# Whitepaper Template

Professional whitepaper formatting with consistent styling, properly formatted tables, and strategic page breaks.

## Quick Start

1. **Edit your content:**
   - Open `document.md`
   - Replace title, authors, and content
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

## Markdown Best Practices

### Structure

```markdown
# Title (H1) - appears once per document

<div style="page-break-after: always;"></div>

## Major Section (H2) - gets page break before

### Subsection (H3) - no automatic page break

#### Detail level (H4) - don't overuse
```

### Tables

Use pipe syntax only:

```markdown
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data     | Data     | Data     |
```

NOT space-separated text (those become text, not tables).

### Emphasis

- **Bold** for concepts and important terms (sparingly)
- *Italic* for foreign words or special references
- Normal text for everything else

Avoid excessive emphasis throughout the document.

## Page Break Strategy

The `add_page_breaks.py` script adds page breaks before every H2 heading. For a 20-30 page whitepaper:
- 1 page break before Introduction
- 1 page break before each major section (~8 sections)
- 1 page break before Conclusion
- 1 page break before Appendices

Result: ~15-20 page breaks for professional layout.

## Validation Before Submission

Run through the checklist in the document-formatting skill:

- [ ] Title on own page
- [ ] Major sections on new pages
- [ ] All tables have headers and borders
- [ ] No AI formatting tells (mixed fonts, excessive emphasis, etc.)
- [ ] Consistent heading sizes and colors
- [ ] Proper paragraph spacing

Total validation time: ~20 minutes

## Troubleshooting

**Issue: "pandoc not found"**
```powershell
choco install pandoc
```

**Issue: Tables render as text**
- Cause: Using space-separated columns instead of pipe syntax
- Fix: Convert to `| Column | Data |` format

**Issue: Page breaks in wrong places**
- Pandoc converts H2 as major sections
- If you want breaks before different heading levels, edit `add_page_breaks.py`
- Change `Heading 2` to `Heading 1` or `Heading 3`

**Issue: Column widths still wrong after running script**
- Verify `fix_table_widths.py` ran without errors
- Check for empty tables (0 columns) in markdown
- Manually open DOCX and verify tables exist

## Additional Resources

- Complete documentation: `.github/skills/document-formatting/SKILL.md`
- AI tells checklist: See skill documentation
- Pandoc docs: https://pandoc.org/
- python-docx docs: https://python-docx.readthedocs.io/

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review document-formatting skill for comprehensive guidance
3. Examine the real-world example (ACM-to-APO Migration Whitepaper) for a complete working project
