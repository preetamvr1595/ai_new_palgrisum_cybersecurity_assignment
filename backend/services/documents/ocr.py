import pytesseract
from PIL import Image
import os
import logging

logger = logging.getLogger(__name__)

def process_image_ocr(image_path: str) -> str:
    """
    Uses Tesseract OCR to extract text from an image.
    Requires Tesseract to be installed on the host system.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError("Image file not found for OCR.")
        
    try:
        logger.info(f"Running OCR on {image_path}")
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        logger.error(f"OCR Pipeline failed: {str(e)}")
        raise
