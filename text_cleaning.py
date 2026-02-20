import re

def clean_text(text: str) -> str:
    """
    Deterministic text cleaning.
    No NLP intelligence here — intentionally.
    """
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^a-zA-Z0-9.,()%\- ]', '', text)
    return text.strip()
