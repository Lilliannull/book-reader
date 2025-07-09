import os
import fitz  # PyMuPDF
from ebooklib import epub
from bs4 import BeautifulSoup

def extract_pdf_text(path):
    doc = fitz.open(path)
    return "\n".join([page.get_text() for page in doc])

def extract_txt_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def extract_epub_text(path):
    book = epub.read_epub(path)
    text = ''
    for item in book.get_items():
        if item.get_type() == epub.EpubHtml:
            soup = BeautifulSoup(item.get_content(), 'html.parser')
            text += soup.get_text()
    return text

def extract_text_by_extension(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == '.pdf':
        return extract_pdf_text(path)
    elif ext == '.txt':
        return extract_txt_text(path)
    elif ext == '.epub':
        return extract_epub_text(path)
    else:
        return "Unsupported file type."
