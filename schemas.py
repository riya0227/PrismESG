from dataclasses import dataclass

@dataclass
class TextChunk:
    document_id: str
    page_number: int
    chunk_id: str
    text: str
