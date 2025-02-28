import sys
import os
import re
import datetime
import PyPDF2
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import openai

# Get original working directory
original_dir = os.environ.get("ORIG_PWD", os.getcwd())

def resolve_path(path):
    if not os.path.isabs(path):
        return os.path.join(original_dir, path)
    return path

def read_pdf(file_path):
    extracted_text = ""
    
    # Try text extraction with PyPDF2
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            num_pages = len(pdf_reader.pages)
            print(f"\nReading '{file_path}' using PyPDF2 ({num_pages} pages):")
            for i, page in enumerate(pdf_reader.pages):
                text = page.extract_text()
                if text:
                    text = text.strip()
                    extracted_text += text + "\n"
                print(f"\n--- Page {i + 1} ---")
                print(text if text else "[No text extracted]")
            print("\n" + "=" * 40 + "\n")
    except Exception as e:
        print(f"Error reading '{file_path}' with PyPDF2: {e}")

    # If extraction failed or yielded blank output, fallback to OCR
    if not extracted_text.strip():
        print(f"No text extracted from '{file_path}' using PyPDF2. Falling back to OCR...")
        try:
            images = convert_from_path(file_path, dpi=300)
            for i, image in enumerate(images):
                ocr_text = pytesseract.image_to_string(image).strip()
                print(f"\n--- OCR Page {i + 1} ---")
                print(ocr_text if ocr_text else "[No OCR text extracted]")
                extracted_text += ocr_text + "\n"
            print("\n" + "=" * 40 + "\n")
        except Exception as e:
            print(f"Error processing '{file_path}' with OCR: {e}")
    
    return extracted_text

def generate_filename(text):
    """
    Uses the OpenAI API to generate a filename in the format:
    'YYYY-MM-DD File_Topic'
    where the date is either extracted from the text or defaults to today's date.
    """
    prompt = (
        "You are an assistant that generates a descriptive filename for a PDF based on its content. "
        "Analyze the text below and generate a filename in the exact format 'YYYY-MM-DD File_Topic', where: "
        "- YYYY-MM-DD is a relevant date found in the text or the current date if none exists, and "
        "- File_Topic is a concise description of the document's topic (words separated by underscores). "
        "Only output the filename in that exact format without any additional text.\n\n"
        "Text:\n"
        f"{text}\n\n"
        "Filename:"
    )
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # or "gpt-3.5-turbo"
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=20,
            temperature=0.5,
        )
        filename = response.choices[0].message.content.strip()
        # Remove any surrounding quotes if present
        filename = filename.strip('"')
        return filename
    except Exception as e:
        print(f"Error generating filename: {e}")
        # Fallback: use current date and a generic topic
        fallback_date = datetime.datetime.now().strftime("%Y-%m-%d")
        return f"{fallback_date}_Document"

def main():
    # If command-line arguments are provided, use them; else prompt the user.
    if len(sys.argv) > 1:
        pdf_files = [resolve_path(f) for f in sys.argv[1:]]
    else:
        user_input = input("Enter space-separated full-path filenames of .pdf files: ")
        pdf_files = user_input.split()

    # Process each file
    for file_path in pdf_files:
        if file_path.lower().endswith('.pdf'):
            text = read_pdf(file_path)
            if text.strip():
                filename = generate_filename(text)
                print(f"Suggested filename for '{file_path}': {filename}")
                
                # Optionally, rename the file:
                new_path = os.path.join(os.path.dirname(file_path), filename + ".pdf")
                # Uncomment the following to actually rename the file:
                # try:
                #     os.rename(file_path, new_path)
                #     print(f"Renamed '{file_path}' to '{new_path}'")
                # except Exception as e:
                #     print(f"Error renaming '{file_path}': {e}")
            else:
                print(f"No text extracted from '{file_path}'. Skipping filename generation.")
        else:
            print(f"Skipping '{file_path}': not a PDF file.")

if __name__ == "__main__":
    main()

