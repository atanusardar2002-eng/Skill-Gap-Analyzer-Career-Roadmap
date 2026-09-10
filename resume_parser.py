"""
Resume Parser Module
Extracts and sanitizes text content from PDF and Plain Text resumes.
"""

import io
from typing import Optional
from pypdf import PdfReader


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract text from uploaded PDF file bytes using pypdf."""
    try:
        reader = PdfReader(io.BytesIO(file_bytes))
        extracted_text = []
        for page_idx, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if page_text:
                extracted_text.append(f"--- Page {page_idx + 1} ---\n{page_text}")
        
        full_text = "\n\n".join(extracted_text).strip()
        return full_text if full_text else "No readable text found in the PDF. It may contain scanned images."
    except Exception as e:
        return f"Error extracting PDF: {str(e)}"


def extract_text_from_txt(file_bytes: bytes) -> str:
    """Extract text from uploaded TXT file bytes."""
    try:
        return file_bytes.decode("utf-8", errors="replace").strip()
    except Exception as e:
        return f"Error reading text file: {str(e)}"


def parse_resume(file_bytes: bytes, filename: str) -> str:
    """
    Parses resume content based on file extension.
    Returns cleaned, sanitized text.
    """
    ext = filename.lower().split(".")[-1]
    if ext == "pdf":
        text = extract_text_from_pdf(file_bytes)
    elif ext in ["txt", "md"]:
        text = extract_text_from_txt(file_bytes)
    else:
        text = "Unsupported file type. Please upload a PDF or TXT file."
        
    # Basic sanitization
    text = text.replace("\x00", "").strip()
    # Cap excessive length if over 20,000 chars (approx 5-6 dense pages)
    if len(text) > 25000:
        text = text[:25000] + "\n\n...[Content truncated for analysis efficiency]..."
    return text
