import sys
import os
import PyPDF2

original_dir = os.environ.get("ORIG_PWD", os.getcwd())

def resolve_path(path):
    if not os.path.isabs(path):
        return os.path.join(original_dir, path)
    return path

def read_pdf(file_path):
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            num_pages = len(pdf_reader.pages)
            print(f"\nReading '{file_path}' ({num_pages} pages):")
            for i, page in enumerate(pdf_reader.pages):
                text = page.extract_text()
                print(f"\n--- Page {i + 1} ---")
                print(text)
            print("\n" + "=" * 40 + "\n")
    except Exception as e:
        print(f"Error reading '{file_path}': {e}")


def main():
    # Check if any command-line arguments were provided 
    # (excluding the script name)
    if len(sys.argv) > 1:
        pdf_files = [resolve_path(f) for f in sys.argv[1:]]
    else:
        user_input = input("Enter space-separated full-path filenames of .pdf files: ")
        pdf_files = user_input.split()

    # Loop through each file and process if it's a PDF
    for file_path in pdf_files:
        if file_path.lower().endswith('.pdf'):
            read_pdf(file_path)
        else:
            print(f"Skipping '{file_path}': not a PDF file.")

if __name__ == "__main__":
    main()
