from PIL import Image
import pytesseract

# Set the path to your local tesseract.exe
pytesseract.pytesseract.tesseract_cmd = r"c:\Users\GF99\Documentation\.github\tesseract-main\tesseract.exe"

# Path to your image file
image_path = r"C:\Users\GF99\Documentation\temp_docx_extract\AI\IMG_4385.jpg"

# Open the image
img = Image.open(image_path)

# Extract text using pytesseract
text = pytesseract.image_to_string(img)

# Print the extracted text
print("Extracted Text:\n")
print(text)

# Optionally, save the extracted text to a file
with open("extracted_text.txt", "w", encoding="utf-8") as f:
    f.write(text)
