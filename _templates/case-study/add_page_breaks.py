#!/usr/bin/env python3
"""
Add page breaks before major section headings in DOCX.

This script post-processes a Pandoc-generated DOCX file to add page breaks
before each major section (Heading 2 level), creating professional layout.
"""

import sys
from docx import Document
from docx.shared import Pt
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def add_page_break_before(paragraph):
    """Insert a page break before a paragraph."""
    p = paragraph._element
    pPr = p.get_or_add_pPr()
    
    # Create page break element
    pageBreak = OxmlElement('w:pageBreakBefore')
    pPr.insert(0, pageBreak)

def add_page_breaks_to_docx(input_file, output_file):
    """
    Add page breaks before major section headings.
    
    Args:
        input_file: Path to Pandoc-generated DOCX
        output_file: Path to save modified DOCX
    """
    doc = Document(input_file)
    
    page_breaks_added = 0
    sections_found = []
    
    for i, para in enumerate(doc.paragraphs):
        # Check if this is a major section heading (Heading 2)
        style_name = para.style.name if para.style else ""
        
        if style_name == "Heading 2":
            sections_found.append(para.text[:50])  # Store first 50 chars
            add_page_break_before(para)
            page_breaks_added += 1
            print(f"  ✓ Page break before: {para.text[:50]}...")
    
    # Save modified document
    doc.save(output_file)
    
    return page_breaks_added, sections_found

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python add_page_breaks.py <input_docx> <output_docx>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    print(f"\n=== ADDING PAGE BREAKS ===\n")
    print(f"Input:  {input_file}")
    print(f"Output: {output_file}\n")
    
    try:
        num_breaks, sections = add_page_breaks_to_docx(input_file, output_file)
        
        print(f"\n✅ Complete!")
        print(f"   Added {num_breaks} page breaks")
        print(f"   Sections: {num_breaks}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
