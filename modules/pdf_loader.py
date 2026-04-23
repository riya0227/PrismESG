import pdfplumber
from typing import Iterator, Tuple

def extract_pages(pdf_path: str) -> Iterator[Tuple[int, str]]:
    """
    Stream PDF pages one by one.
    This is SAFE for large PDFs.
    """
    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if text:
                yield page_number, text
