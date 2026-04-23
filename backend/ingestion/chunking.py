# ingestion/chunking.py

from typing import List, Dict
import re
from .text_cleaning import clean_text


def split_into_sentences(text: str) -> List[str]:
    """
    Better sentence splitting using regex.
    """
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if len(s.strip()) > 0]


def chunk_page(
    document_id: str,
    page_number: int,
    raw_text: str,
    min_length: int = 50,
    max_length: int = 300
) -> List[Dict]:
    """
    Convert a single PDF page into chunks using sentence grouping.
    """

    cleaned_text = clean_text(raw_text)

    # -------- Split into sentences --------
    sentences = split_into_sentences(cleaned_text)

    chunks: List[Dict] = []

    current_chunk = ""
    chunk_id_counter = 0

    for sentence in sentences:

        # If adding sentence exceeds max length → save chunk
        if len(current_chunk) + len(sentence) > max_length:

            if len(current_chunk) >= min_length:
                chunks.append(build_chunk(
                    document_id,
                    page_number,
                    chunk_id_counter,
                    current_chunk
                ))
                chunk_id_counter += 1

            current_chunk = sentence

        else:
            current_chunk += " " + sentence

    # -------- Add last chunk --------
    if len(current_chunk) >= min_length:
        chunks.append(build_chunk(
            document_id,
            page_number,
            chunk_id_counter,
            current_chunk
        ))

    return chunks


# -----------------------------
# HELPER
# -----------------------------
def build_chunk(document_id, page_number, idx, text):
    return {
        "document_id": document_id,
        "page_number": page_number,
        "chunk_id": f"{document_id}_p{page_number}_{idx}",
        "text": text.strip(),
        "length": len(text)
    }