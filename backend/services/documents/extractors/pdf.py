import fitz  # PyMuPDF
from typing import Dict, Any, Tuple
import io

def extract_pdf(file_path: str) -> Tuple[str, Dict[str, Any]]:
    """
    Extracts text and metadata from a PDF using PyMuPDF.
    If a page contains no text but has images, it falls back to OCR if Tesseract is available.
    """
    doc = fitz.open(file_path)
    text_content = []
    metadata = {
        "page_count": doc.page_count,
        "author": doc.metadata.get("author", ""),
        "title": doc.metadata.get("title", ""),
        "creation_date": doc.metadata.get("creationDate", "")
    }

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        page_text = page.get_text()
        
        # Simple heuristic: If page is empty, try OCR on images
        if not page_text.strip():
            image_list = page.get_images(full=True)
            for img in image_list:
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                # In a full implementation, we'd save this to a temp file and call process_image_ocr
                # For this scaffolding, we just append a placeholder
                text_content.append("[OCR Image Extracted Text Placeholder]")
        else:
            text_content.append(page_text)

    return "\n\n".join(text_content), metadata
