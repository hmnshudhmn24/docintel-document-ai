"""PDF text extraction using PyMuPDF (fitz) for embedded text layers."""
import fitz

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    texts = []
    for page in doc:
        txt = page.get_text('text') or ''
        texts.append(txt)
    return '\n\n'.join(texts)
