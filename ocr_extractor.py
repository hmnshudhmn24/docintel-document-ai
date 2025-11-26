"""OCR extraction using pdf2image + pytesseract for scanned pages."""
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
from utils import load_config
import os

def pdf_to_images(pdf_path, dpi=None, out_dir=None):
    cfg = load_config()
    dpi = dpi or cfg.get('ocr', {}).get('dpi', 300)
    pages = convert_from_path(pdf_path, dpi=dpi)
    paths = []
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    for i, img in enumerate(pages, start=1):
        path = os.path.join(out_dir or '.', f'page_{i}.png')
        img.save(path, 'PNG')
        paths.append(path)
    return paths

def ocr_image(path, lang=None):
    cfg = load_config()
    lang = lang or cfg.get('ocr', {}).get('lang', 'eng')
    img = Image.open(path)
    text = pytesseract.image_to_string(img, lang=lang)
    return text

def extract_full_text(pdf_path, do_ocr=True):
    # Try embedded text first
    try:
        from pdf_loader import extract_text_from_pdf
        txt = extract_text_from_pdf(pdf_path)
        if txt and len(txt) > 200:
            return txt, []  # return text and empty ocr pages list
    except Exception:
        txt = ''
    # fallback to OCR
    pages = pdf_to_images(pdf_path, out_dir='./temp_pages')
    ocr_texts = []
    for p in pages:
        ocr_texts.append(ocr_image(p))
    full = '\n\n'.join(ocr_texts)
    return full, ocr_texts
