"""LayoutLM helper (optional) - provided for completeness but not used by default.
"""
from transformers import LayoutLMv3Processor, LayoutLMv3ForQuestionAnswering

def load_layoutlm(model_name='microsoft/layoutlmv3-base'):
    proc = LayoutLMv3Processor.from_pretrained(model_name)
    model = LayoutLMv3ForQuestionAnswering.from_pretrained(model_name)
    return proc, model
