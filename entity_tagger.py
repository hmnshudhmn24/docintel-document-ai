"""Simple regex-based entity extraction for demo purposes."""
import re

def extract_entities(text):
    entities = {}
    emails = re.findall(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", text)
    dates = re.findall(r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b", text)
    amounts = re.findall(r"\b\$?\d{1,3}(?:[.,]\d{3})*(?:[.,]\d+)?\s?(?:USD|INR|EUR|Rs|\$)?\b", text)
    entities['emails'] = list(dict.fromkeys(emails))
    entities['dates'] = list(dict.fromkeys(dates))
    entities['amounts'] = list(dict.fromkeys([a.strip() for a in amounts if a.strip()]))
    return entities
