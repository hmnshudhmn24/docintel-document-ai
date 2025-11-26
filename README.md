# 🧾 DOCINTEL — Document AI

**DOCINTEL** extracts structured insights from scanned PDFs and images using **naver-clova-ix/donut-base** (Donut). It supports OCR fallback, entity extraction, and document summarization via Donut on page images.

> ⚠️ Install system dependencies: `poppler` and `tesseract` for pdf2image and pytesseract respectively.

## Quickstart

1. Create venv & install dependencies:
```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. Run API server:
```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

3. Upload a PDF and call endpoints (see examples/demo_commands.txt).

## Files
- `ocr_extractor.py` — PDF→images→OCR pipeline
- `pdf_loader.py` — extract embedded text from PDFs
- `entity_tagger.py` — regex-based entity extraction
- `summarize_doc.py` — DONUT-based summarizer for page images
- `app.py` — FastAPI server with upload/summary endpoints

## Notes
- Donut requires vision-encoder-decoder inference which may need GPU for speed.
- For text-only PDFs consider using `extract_text_from_pdf` then a text summarizer instead of Donut.
- This repo is a prototype/demo. Validate on your data before production use.
