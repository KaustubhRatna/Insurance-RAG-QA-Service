# parser/document_parser.py

import requests
import tempfile
import os
import io
from typing import Literal
import pdfplumber
import pymupdf4llm
from docx import Document as DocxDocument

def parse_pdf_plain(buffer: bytes) -> str:
    """
    Extracts raw text from PDF using pdfplumber.
    """
    text_parts = []
    with pdfplumber.open(io.BytesIO(buffer)) as pdf:
        for page in pdf.pages:
            text_parts.append(page.extract_text() or "")
    return "\n\n".join(text_parts)

def parse_pdf_markdown(path: str) -> str:
    """
    Converts PDF to Markdown via pymupdf4llm.
    Expects a file path, so we write buffer to a temp file.
    """
    return pymupdf4llm.to_markdown(path, write_images=False)

def parse_docx(buffer: bytes) -> str:
    """
    Extract raw text from a DOCX buffer using python-docx.
    """
    doc = DocxDocument(io.BytesIO(buffer))
    paragraphs = [p.text for p in doc.paragraphs]
    return "\n\n".join(paragraphs)

def parse_plain_text(buffer: bytes) -> str:
    """
    Decode plain-text or email content.
    """
    return buffer.decode('utf-8', errors='ignore')

def get_document_text(
    document_url: str,
    mode: Literal["plain","markdown"] = "markdown"
) -> str:
    """
    Downloads the document at `document_url`, infers its type
    (PDF, DOCX, TXT/EML) and returns its extracted text.

    - For PDFs:
      - mode="plain": uses pdfplumber
      - mode="markdown": uses pymupdf4llm.to_markdown

    - For DOCX: uses python-docx
    - For TXT or EML: decodes UTF-8
    """
    # 1) Download
    resp = requests.get(document_url, stream=True, timeout=30)
    resp.raise_for_status()
    buffer = resp.content

    # 2) Determine type
    content_type = resp.headers.get("content-type", "")
    ext = os.path.splitext(document_url)[1].lower().lstrip(".")

    # 3) Dispatch parser
    if 'pdf' in content_type or "application/pdf" in content_type or ext == "pdf":
        if mode == "markdown":
            # write to temp file for pypdf4llm
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tf:
                tf.write(buffer)
                tf_path = tf.name
            try:
                return parse_pdf_markdown(tf_path)
            finally:
                os.remove(tf_path)
        else:
            return parse_pdf_plain(buffer)

    elif (
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document" in content_type
        or ext == "docx"
    ):
        return parse_docx(buffer)

    elif (
        "text/plain" in content_type
        or ext in {"txt", "eml"}
    ):
        return parse_plain_text(buffer)

    else:
        raise ValueError(f"Unsupported document type: {content_type or ext}")
