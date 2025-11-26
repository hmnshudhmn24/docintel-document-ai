"""Summarization using DONUT (naver-clova-ix/donut-base) via Hugging Face.
This module uses Donut's processor and VisionEncoderDecoderModel for docVQA-style prompts.
"""
from transformers import DonutProcessor, VisionEncoderDecoderModel
from PIL import Image
from utils import load_config

_processor = None
_model = None

def _init(model_name):
    global _processor, _model
    if _processor is None or _model is None:
        _processor = DonutProcessor.from_pretrained(model_name)
        _model = VisionEncoderDecoderModel.from_pretrained(model_name)
    return _processor, _model

def summarize_image(image_path, model_name=None, max_length=250):
    cfg = load_config()
    model_name = model_name or cfg.get('model', {}).get('name')
    processor, model = _init(model_name)
    image = Image.open(image_path).convert('RGB')
    task_prompt = '<s_docvqa><s_question>Summarize the document:</s_question>'
    inputs = processor(image, task_prompt, return_tensors='pt')
    output = model.generate(**inputs, max_new_tokens=max_length)
    decoded = processor.batch_decode(output, skip_special_tokens=True)[0]
    return decoded

def summarize_text(text, chunk_size=1000, model_name=None):
    # naive: summarize by extracting first chunk and running model on placeholder image (not ideal for text-only)
    # For text-heavy docs, use text summarization pipeline instead; here we return a simple extractive summary.
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    if not lines:
        return ''
    summary = ' '.join(lines[:min(5, len(lines))])
    return summary
