import PyPDF2
import sys

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            
            print(f"Total pages: {len(pdf_reader.pages)}\n")
            print("=" * 80)
            
            for page_num, page in enumerate(pdf_reader.pages, 1):
                page_text = page.extract_text()
                text += f"\n--- Page {page_num} ---\n"
                text += page_text
                print(f"\n--- Page {page_num} ---\n")
                print(page_text)
            
            return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    else:
        pdf_path = "Integrity/INT-500 Administering Your Integrity Software .pdf"
    
    print(f"Extracting text from: {pdf_path}\n")
    extract_text_from_pdf(pdf_path)
