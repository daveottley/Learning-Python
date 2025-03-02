import sys
import os
import re
import datetime
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Ensure your API key is set as an environment variable, e.g.:
# export OPENAI_API_KEY="your-api-key"

# Get original working directory from ORIG_PWD (if set) or fallback to current working directory.
original_dir = os.environ.get("ORIG_PWD", os.getcwd())

def resolve_path(path):
    if not os.path.isabs(path):
        return os.path.join(original_dir, path)
    return path

def read_pdf(file_path):
    extracted_text = ""
    try:
        images = convert_from_path(file_path, dpi=300)
        for i, image in enumerate(images):
            ocr_text = pytesseract.image_to_string(image).strip()
            print(f"--- OCR Page {i + 1} ---")
            print(ocr_text if ocr_text else "[No OCR text extracted]")
            extracted_text += ocr_text + "\n"
    except Exception as e:
        # Error handling omitted to ensure only the OCR output is printed.
        pass
    return extracted_text

def main():
    # If command-line arguments are provided, use them; otherwise, prompt the user.
    if len(sys.argv) > 1:
        pdf_files = [resolve_path(f) for f in sys.argv[1:]]
    else:
        user_input = input("Enter space-separated full-path filenames of .pdf files: ")
        pdf_files = user_input.split()

    # Process each file.
    for file_path in pdf_files:
        if file_path.lower().endswith('.pdf'):
            read_pdf(file_path)
        # Non-PDF files are silently skipped to adhere to the output requirements.

if __name__ == "__main__":
    main()

