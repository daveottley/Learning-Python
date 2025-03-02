import sys
import os
import re
import datetime
import subprocess
from openai import OpenAI

MODEL = "o3-mini"
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Ensure your API key is set as an environment variable, e.g.:
# export OPENAI_API_KEY="your-api-key"

# Get original working directory from ORIG_PWD (if set) or fallback to current working directory.
original_dir = os.environ.get("ORIG_PWD", os.getcwd())

def resolve_path(path):
    if not os.path.isabs(path):
        return os.path.join(original_dir, path)
    return path

def get_pdf_text(file_path):
    """
    Calls pdfprint.py on the given file to obtain its text content.
    """
    try:
        # Call pdfprint.py as a subprocess and capture its output.
        result = subprocess.run(
            ["python", "pdfprint.py", file_path],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error processing '{file_path}' with pdfprint.py: {e}")
        return ""

def generate_suggested_filename(text):
    """
    Uses the OpenAI API to generate a filename in the format:
    'YYYY-MM-DD File_Topic'
    where the date is either extracted from the text or defaults to today's date.
    """
    prompt = (
        "You are an assistant that generates a descriptive filename for a PDF based on its content. "
        "Analyze the text below and generate a filename in the exact format 'YYYY-MM-DD File_Topic', where: "
        "- YYYY-MM-DD is a relevant date found in the text or the current date if none exists. "
        "Prefer due dates to notice dates, and "
        "- File_Topic is a concise description of the document's topic (words separated by underscores). "
        "Only output the filename in that exact format without any additional text.\n\n"
        "Text:\n"
        f"{text}\n\n"
        "Filename:"
    )

    try:
        response = client.chat.completions.create(
            model= MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        filename = response.choices[0].message.content.strip()
        # Remove any surrounding quotes if present.
        filename = filename.strip('"')
        return filename
    except Exception as e:
        print(f"Error generating filename: {e}")
        # Fallback: use today's date and a generic topic.
        fallback_date = datetime.datetime.now().strftime("%Y-%m-%d")
        return f"{fallback_date}_Document"

def rename_file(old_path, new_path):
    """
    Renames the file from old_path to new_path, handling collisions.
    """
    if os.path.exists(new_path):
        print(f"Cannot rename '{old_path}' to '{new_path}': target file already exists.")
        return False
    try:
        os.rename(old_path, new_path)
        print(f"Renamed '{old_path}' to '{new_path}'")
        return True
    except Exception as e:
        print(f"Error renaming '{old_path}' to '{new_path}': {e}")
        return False

def main():
    # Determine if the force flag (-f) is used.
    force = False
    args = sys.argv[1:]
    if "-f" in args:
        force = True
        args.remove("-f")
    
    # If command-line arguments (other than -f) are provided, use them; otherwise, prompt the user.
    if args:
        pdf_files = [resolve_path(f) for f in args]
    else:
        user_input = input("Enter space-separated full-path filenames of .pdf files: ")
        pdf_files = [resolve_path(f) for f in user_input.split()]

    # Process each PDF file.
    for file_path in pdf_files:
        if not file_path.lower().endswith('.pdf'):
            print(f"Skipping '{file_path}': not a PDF file.")
            continue

        # Get text content by calling pdfprint.py.
        text_content = get_pdf_text(file_path)
        if not text_content.strip():
            print(f"No text content obtained from '{file_path}'. Skipping renaming.")
            continue

        # Generate a suggested filename from the text content.
        suggested_name = generate_suggested_filename(text_content)
        if not suggested_name:
            print(f"Could not generate a suggested filename for '{file_path}'. Skipping.")
            continue
        
        # Ensure the suggested filename ends with the .pdf extension.
        if not suggested_name.lower().endswith('.pdf'):
            suggested_name += '.pdf'
        
        # Construct the new file path in the same directory as the original file.
        new_file_path = os.path.join(os.path.dirname(file_path), suggested_name)
        if os.path.abspath(new_file_path) == os.path.abspath(file_path):
            print(f"File '{file_path}' already has the suggested name. Skipping.")
            continue

        if force:
            # Automatically rename without prompting.
            rename_file(file_path, new_file_path)
        else:
            # Display the suggested filename and ask for confirmation.
            print(f"Suggested new filename for '{file_path}':")
            print(f"  {new_file_path}")
            choice = input("Do you want to rename the file to this? (y/N): ").strip().lower()
            if choice == "y":
                rename_file(file_path, new_file_path)
            else:
                print(f"Skipped renaming '{file_path}'.")

if __name__ == "__main__":
    main()

