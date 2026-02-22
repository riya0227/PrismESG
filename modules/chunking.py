from typing import List
from .schemas import TextChunk
from .text_cleaning import clean_text

def chunk_page(
    document_id: str,
    page_number: int,
    raw_text: str,
    min_length: int = 50
) -> List[TextChunk]:
    """
    Convert a single PDF page into paragraph-level chunks.
    """

    cleaned_text = clean_text(raw_text)
    paragraphs = cleaned_text.split(". ")

    chunks: List[TextChunk] = []

    for idx, para in enumerate(paragraphs):
        para = para.strip()
        if len(para) >= min_length:
            chunk_id = f"{document_id}_p{page_number}_{idx}"
            chunks.append(
                TextChunk(
                    document_id=document_id,
                    page_number=page_number,
                    chunk_id=chunk_id,
                    text=para
                )
            )

    return chunks
