import os
import subprocess
import pypandoc

def convert_md_to_docx_and_pdf_via_pandoc():
    current_directory = os.getcwd()
    print(f"Scanning directory: {current_directory} for .md files...")

    try:
        pandoc_path = pypandoc.get_pandoc_path()
        print(f"Pandoc is installed and found at: {pandoc_path}")
    except Exception as e:
        print(f"Error: Pandoc not found or not in PATH. Please install Pandoc (https://pandoc.org/installing.html). Error: {e}")
        return

    for filename in os.listdir(current_directory):
        if filename.endswith(".md"):
            md_filepath = os.path.join(current_directory, filename)
            base_name = os.path.splitext(filename)[0]
            docx_filepath = os.path.join(current_directory, f"{base_name}.docx")
            pdf_filepath = os.path.join(current_directory, f"{base_name}.pdf")

            print(f"\nProcessing '{filename}'...")

            # 1. Convert .md to .docx using pandoc (no changes here, this works)
            try:
                pypandoc.convert_file(md_filepath, 'docx', outputfile=docx_filepath)
                print(f"Successfully converted '{filename}' to '{os.path.basename(docx_filepath)}'")
                pass
            except Exception as e:
                print(f"Error converting '{filename}' to .docx using Pandoc: {e}")
                continue # Move to the next file if .docx conversion fails

            # 2. Convert .docx to .pdf using pandoc with wkhtmltopdf
            try:
                # Crucial Change: Convert DOCX to HTML first, then to PDF using wkhtmltopdf
                # Pandoc will handle this pipeline: docx -> html -> pdf (via wkhtmltopdf)
                pypandoc.convert_file(
                    docx_filepath,
                    'pdf',
                    format='docx',  # Specify the input format explicitly
                    outputfile=pdf_filepath,
                    extra_args=['--pdf-engine=wkhtmltopdf', '--to=html'] # Tell Pandoc to use HTML as intermediate
                )
                print(f"Successfully converted '{os.path.basename(docx_filepath)}' to '{os.path.basename(pdf_filepath)}' using wkhtmltopdf.")
            except Exception as e:
                print(f"Error converting '{os.path.basename(docx_filepath)}' to .pdf using wkhtmltopdf: {e}")
                print(f"Detailed error: {e}") # Print the full error for more debugging if needed

if __name__ == "__main__":
    convert_md_to_docx_and_pdf_via_pandoc()
