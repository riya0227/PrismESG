# ingestion/pdf_loader.py

import pdfplumber
from typing import Iterator, Tuple


def extract_pages(pdf_path: str) -> Iterator[Tuple[int, str]]:
    """
    Stream PDF pages one by one.
    Safe for large PDFs and handles edge cases.
    """

    try:
        with pdfplumber.open(pdf_path) as pdf:

            for page_number, page in enumerate(pdf.pages, start=1):

                try:
                    text = page.extract_text()

                    # -------- Handle empty / None --------
                    if not text:
                        continue

                    # -------- Normalize text --------
                    text = normalize_text(text)

                    if len(text.strip()) == 0:
                        continue

                    yield page_number, text

                except Exception as page_error:
                    print(f"⚠️ Error reading page {page_number}: {page_error}")
                    continue

    except Exception as e:
        raise RuntimeError(f"Failed to open PDF: {pdf_path}. Error: {str(e)}")


# -----------------------------
# HELPER: CLEAN PDF TEXT
# -----------------------------
def normalize_text(text: str) -> str:
    """
    Fix common PDF extraction issues:
    - broken line breaks
    - extra spaces
    """

    # Replace line breaks inside sentences
    text = text.replace("\n", " ")

    # Remove excessive spaces
    text = " ".join(text.split())

    return text