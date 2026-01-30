# Skills Audit Results

Date: January 30, 2026

## Summary

Out of 4 document processing skills, only **1 is used frequently** enough to justify global auto-loading.

## Detailed Audit

### ✅ KEEP: xlsx
- **Used weekly?** YES
- **Projects using it:** Training, SpendTracker, PC_Value_Tracker, Skill Matrix, Integrity Audits
- **Teaches AI something it doesn't know?** YES - openpyxl formula recalculation, complex formatting
- **Tools exist?** YES - recalc.py verified in skill folder
- **Action:** Keep in `.github/skills/xlsx/`
- **Token cost:** ~2,500 tokens (justified by frequent use)

### ⚠️ MOVE: pptx
- **Used weekly?** NO - Single use case (Skill Matrix promotion, 01/30/26)
- **Teaches AI something it doesn't know?** YES - html2pptx workflow, template manipulation
- **Tools exist?** Needs verification (multiple Python scripts referenced)
- **Action:** Move to `_reference/pptx-skill/` OR make project-specific at `Skill Matrix/.github/skills/pptx/`
- **Token cost:** ~2,500 tokens (wasted on 99% of sessions)
- **Savings:** ~2,500 tokens per session when not needed

### ⚠️ MOVE: docx
- **Used weekly?** NO - No .docx creation/editing found in workspace scan
- **Teaches AI something it doesn't know?** Likely YES - Tracked changes, comments, OOXML
- **Tools exist?** Needs verification
- **Action:** Move to `_reference/docx-skill/`
- **Token cost:** ~2,500 tokens (wasted if not used)
- **Savings:** ~2,500 tokens per session when not needed

### ⚠️ MOVE: pdf
- **Used weekly?** NO - Minimal use (occasional PDF text extraction)
- **Teaches AI something it doesn't know?** Partially - Basic extraction is standard knowledge
- **Tools exist?** Needs verification
- **Action:** Move to `_reference/pdf-skill/`
- **Token cost:** ~2,500 tokens (wasted if not used)
- **Savings:** ~2,500 tokens per session when not needed

## Projected Token Savings

**Current Setup:**
- 4 skills × ~2,500 tokens each = ~10,000 tokens per session
- All loaded automatically regardless of need

**Optimized Setup:**
- 1 skill (xlsx) = ~2,500 tokens per session
- Other 3 skills loaded on-demand only

**Savings:**
- ~7,500 tokens saved per session (75% reduction)
- Only load pptx/docx/pdf when explicitly needed

## Implementation Plan

1. **Create archive locations:**
   ```powershell
   mkdir _reference\docx-skill
   mkdir _reference\pdf-skill
   mkdir _reference\pptx-skill
   ```

2. **Move skills:**
   ```powershell
   Move-Item .github\skills\docx _reference\docx-skill
   Move-Item .github\skills\pdf _reference\pdf-skill
   Move-Item .github\skills\pptx _reference\pptx-skill
   ```

3. **Update references in copilot-instructions.md:**
   - Remove mentions of docx, pdf, pptx from auto-loaded skills
   - Add note about on-demand skills in _reference

4. **Test on-demand loading:**
   ```
   "Use the pptx skill from _reference/pptx-skill/ to create a presentation"
   ```

## Alternative: Project-Specific Skills

For pptx (only used in Skill Matrix project):
```powershell
mkdir "Skill Matrix\.github\skills"
Move-Item .github\skills\pptx "Skill Matrix\.github\skills\pptx"
```

This makes the skill available ONLY when working in the Skill Matrix project.

## Next Steps

- [ ] Verify which tools exist in each skill folder
- [ ] Move docx, pdf, pptx to _reference
- [ ] Update copilot-instructions.md
- [ ] Test that xlsx skill still loads automatically
- [ ] Test on-demand loading of moved skills
- [ ] Monitor token usage after changes

## Audit Questions Answered

1. **Do I use this weekly?**
   - xlsx: YES
   - pptx: NO (once ever)
   - docx: NO (not found)
   - pdf: NO (minimal extraction only)

2. **Does it teach AI something it doesn't know?**
   - xlsx: YES (recalc.py, openpyxl specifics)
   - pptx: YES (html2pptx, template workflows)
   - docx: Likely YES (OOXML, tracked changes)
   - pdf: Partially (basic extraction is standard)

3. **Does it reference tools that exist?**
   - xlsx: YES (recalc.py verified)
   - pptx: NEEDS VERIFICATION
   - docx: NEEDS VERIFICATION
   - pdf: NEEDS VERIFICATION

## The Hard Question

> Do you actually need all four document skills loaded globally?

**Answer:** NO. Only xlsx is used frequently enough to justify auto-loading. The other three waste ~7,500 tokens per session for functionality rarely (or never) used.
