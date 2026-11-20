import aiofiles
import os
import re
import urllib
import uuid

def sanitize_filename(filename: str) -> str:
    """Sanitize filename to prevent directory traversal and remove invalid characters."""
    base = os.path.basename(filename)
    sanitized = re.sub(r'[^a-zA-Z0-9_\-\.]', '_', base)
    sanitized = re.sub(r'\.+', '.', sanitized).strip('._-')
    return sanitized or f"report_{uuid.uuid4().hex[:8]}"

async def write_to_file(filename: str, text: str) -> None:
    """Asynchronously write text to a file in UTF-8 encoding ensuring directory exists.

    Args:
        filename (str): The filename to write to.
        text (str): The text to write.
    """
    dirname = os.path.dirname(filename)
    if dirname:
        os.makedirs(dirname, exist_ok=True)
    text_utf8 = text.encode('utf-8', errors='replace').decode('utf-8')

    async with aiofiles.open(filename, "w", encoding='utf-8') as file:
        await file.write(text_utf8)

async def write_text_to_md(text: str, filename: str = "") -> str:
    """Writes text to a Markdown file and returns the file path.

    Args:
        text (str): Text to write to the Markdown file.
        filename (str): Base file name.

    Returns:
        str: The file path of the generated Markdown file.
    """
    safe_name = sanitize_filename(filename) if filename else f"report_{uuid.uuid4().hex[:8]}"
    file_path = f"outputs/{safe_name}.md"
    await write_to_file(file_path, text)
    return file_path

async def write_md_to_pdf(text: str, filename: str = "") -> str:
    """Converts Markdown text to a PDF file and returns the file path."""
    safe_name = sanitize_filename(filename) if filename else f"report_{uuid.uuid4().hex[:8]}"
    file_path = f"outputs/{safe_name}.pdf"

    try:
        from md2pdf.core import md2pdf
        dirname = os.path.dirname(file_path)
        if dirname:
            os.makedirs(dirname, exist_ok=True)
        md2pdf(file_path,
               md_content=text,
               css_file_path="./frontend/pdf_styles.css",
               base_url=None)
        print(f"Report written to {file_path}")
    except Exception as e:
        print(f"Error in converting Markdown to PDF: {e}")
        return ""

    encoded_file_path = urllib.parse.quote(file_path)
    return encoded_file_path

async def write_md_to_word(text: str, filename: str = "") -> str:
    """Converts Markdown text to a DOCX file and returns the file path."""
    safe_name = sanitize_filename(filename) if filename else f"report_{uuid.uuid4().hex[:8]}"
    file_path = f"outputs/{safe_name}.docx"

    try:
        import mistune
        from docx import Document
        from htmldocx import HtmlToDocx

        dirname = os.path.dirname(file_path)
        if dirname:
            os.makedirs(dirname, exist_ok=True)
        html = mistune.html(text)
        doc = Document()
        HtmlToDocx().add_html_to_document(html, doc)
        doc.save(file_path)
        print(f"Report written to {file_path}")
        encoded_file_path = urllib.parse.quote(file_path)
        return encoded_file_path
    except Exception as e:
        print(f"Error in converting Markdown to DOCX: {e}")
        return ""
