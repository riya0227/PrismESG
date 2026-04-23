# ingestion/text_cleaning.py

import re


def clean_text(text: str) -> str:
    """
    Deterministic text cleaning.
    Keeps semantic meaning intact for ESG analysis.
    """

    if not text:
        return ""

    # -------- Normalize unicode bullets/dashes --------
    text = text.replace("•", " ")
    text = text.replace("–", "-")
    text = text.replace("—", "-")

    # -------- Remove weird non-printable characters --------
    text = re.sub(r"[^\x20-\x7E]", " ", text)

    # -------- Preserve important symbols --------
    # Keep: .,()%-:/$
    text = re.sub(r"[^a-zA-Z0-9.,()%\-:/$ ]", "", text)

    # -------- Normalize whitespace --------
    text = re.sub(r"\s+", " ", text)

    return text.strip()