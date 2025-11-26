"""FastAPI app for DOCINTEL: upload PDF, extract text/OCR, get entities, summarize."""
import os, uuid, tempfile
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from utils import ensure_dir, load_config, save_json
from ocr_extractor import extract_full_text, pdf_to_images
from entity_tagger import extract_entities
from summarize_doc import summarize_image, summarize_text

app = FastAPI(title='DOCINTEL API')

cfg = load_config()
STORAGE = cfg.get('storage_dir', './storage')
ensure_dir(STORAGE)

class QARequest(BaseModel):
    question: str

@app.post('/upload_pdf')
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail='Only PDF files are allowed')
    doc_id = str(uuid.uuid4())
    save_path = os.path.join(STORAGE, f"{doc_id}_{file.filename}")
    with open(save_path, 'wb') as f:
        f.write(await file.read())
    return {'doc_id': doc_id, 'filename': file.filename, 'path': save_path}

@app.get('/doc/{doc_id}/text')
def get_text(doc_id: str):
    files = [f for f in os.listdir(STORAGE) if f.startswith(doc_id+'_')]
    if not files:
        raise HTTPException(status_code=404, detail='Document not found')
    path = os.path.join(STORAGE, files[0])
    text, ocr_pages = extract_full_text(path)
    return {'doc_id': doc_id, 'text': text, 'ocr_pages_count': len(ocr_pages)}

@app.get('/doc/{doc_id}/entities')
def get_entities(doc_id: str):
    files = [f for f in os.listdir(STORAGE) if f.startswith(doc_id+'_')]
    if not files:
        raise HTTPException(status_code=404, detail='Document not found')
    path = os.path.join(STORAGE, files[0])
    text, _ = extract_full_text(path)
    ents = extract_entities(text)
    return JSONResponse(content={'doc_id': doc_id, 'entities': ents})

@app.post('/doc/{doc_id}/summarize')
def post_summarize(doc_id: str):
    files = [f for f in os.listdir(STORAGE) if f.startswith(doc_id+'_')]
    if not files:
        raise HTTPException(status_code=404, detail='Document not found')
    path = os.path.join(STORAGE, files[0])
    # convert to images and summarize first page with DONUT
    pages = pdf_to_images(path, out_dir=tempfile.mkdtemp())
    if not pages:
        text, _ = extract_full_text(path)
        summary = summarize_text(text)
        return {'doc_id': doc_id, 'summary': summary}
    # use first page image
    summary = summarize_image(pages[0])
    return {'doc_id': doc_id, 'summary': summary}
