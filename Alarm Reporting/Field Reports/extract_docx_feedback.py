#!/usr/bin/env python3
"""Extract text from Honeywell BGP Feedback Word document"""
from docx import Document
from pathlib import Path

def extract_docx_text(docx_path):
    """Extract all text from a Word document"""
    try:
        doc = Document(docx_path)
        text = []
        for para in doc.paragraphs:
            if para.text.strip():  # Only include non-empty paragraphs
                text.append(para.text)
        return "\n\n".join(text)
    except Exception as e:
        return f"Error extracting Word document: {e}"

if __name__ == "__main__":
    docx_file = Path(__file__).parent / "Honeywell_BGP_Feedback.docx"
    
    print("Extracting Honeywell BGP Feedback Word Document...")
    print("=" * 80)
    feedback_text = extract_docx_text(docx_file)
    
    output_file = Path(__file__).parent / "extracted_feedback.txt"
    output_file.write_text(feedback_text, encoding='utf-8')
    print(f"Saved to: {output_file}")
    print(f"Length: {len(feedback_text)} characters")
    print("\nFirst 500 characters:")
    print("=" * 80)
    print(feedback_text[:500])
