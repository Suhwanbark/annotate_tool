"""PDF preprocessing utilities using PyMuPDF and optional OCR."""
import hashlib
import json
import os
from typing import List

import fitz  # PyMuPDF
from PIL import Image

from utils import ensure_dir

try:
    import pytesseract
except Exception:  # pragma: no cover
    pytesseract = None


def preprocess_pdf(pdf_path: str, project_dir: str, ocr: bool = False) -> List[dict]:
    """Convert PDF into page PNGs and extract text.

    Returns list of metadata dictionaries for each page.
    """
    ensure_dir(project_dir)
    pages_dir = os.path.join(project_dir, "pages")
    ensure_dir(pages_dir)

    doc = fitz.open(pdf_path)
    meta: List[dict] = []
    for i, page in enumerate(doc, start=1):
        pix = page.get_pixmap()
        img_path = os.path.join(pages_dir, f"{i}.png")
        pix.save(img_path)
        text = page.get_text("text")
        ocr_text = ""
        if ocr and pytesseract is not None:
            try:
                ocr_text = pytesseract.image_to_string(Image.open(img_path))
            except Exception:
                ocr_text = ""
        meta.append(
            {
                "page": i,
                "width": pix.width,
                "height": pix.height,
                "text": text,
                "ocr": ocr_text,
                "image_path": img_path,
                "tokens": text.split(),
            }
        )
    meta_path = os.path.join(pages_dir, "metadata.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)
    return meta


def pdf_sha256(pdf_path: str) -> str:
    h = hashlib.sha256()
    with open(pdf_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

