#!/usr/bin/env python3
"""
Extract text from field report PDFs for analysis
"""
import pypdf
import sys
from pathlib import Path

def extract_pdf_text(pdf_path):
    """Extract all text from a PDF file"""
    try:
        reader = pypdf.PdfReader(pdf_path)
        text = []
        for i, page in enumerate(reader.pages, 1):
            page_text = page.extract_text()
            text.append(f"=== Page {i} ===\n{page_text}\n")
        return "\n".join(text)
    except Exception as e:
        return f"Error extracting PDF: {e}"

if __name__ == "__main__":
    # Extract Marathon Anacortes report
    anacortes_pdf = Path(__file__).parent / "BGPPlus_MarathonAnacortes_2025_12_09_bks comments.pdf"
    detroit_pdf = Path(__file__).parent / "Site BGP Report - MPC Detroit_V1.pdf"
    
    print("Extracting Marathon Anacortes Report...")
    print("=" * 80)
    anacortes_text = extract_pdf_text(anacortes_pdf)
    
    output_file = Path(__file__).parent / "extracted_anacortes.txt"
    output_file.write_text(anacortes_text, encoding='utf-8')
    print(f"Saved to: {output_file}")
    print(f"Length: {len(anacortes_text)} characters\n")
    
    print("Extracting MPC Detroit Report...")
    print("=" * 80)
    detroit_text = extract_pdf_text(detroit_pdf)
    
    output_file = Path(__file__).parent / "extracted_detroit.txt"
    output_file.write_text(detroit_text, encoding='utf-8')
    print(f"Saved to: {output_file}")
    print(f"Length: {len(detroit_text)} characters")
