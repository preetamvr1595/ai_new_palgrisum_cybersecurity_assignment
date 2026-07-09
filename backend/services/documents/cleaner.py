import re
from langdetect import detect
from typing import Tuple

def clean_text(text: str) -> str:
    """
    Removes excessive whitespace, null bytes, and non-printable characters.
    """
    # Remove null bytes
    text = text.replace('\x00', '')
    
    # Normalize excessive newlines
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Normalize excessive spaces
    text = re.sub(r' {2,}', ' ', text)
    
    return text.strip()

def extract_content_metadata(text: str) -> Tuple[str, str, int]:
    """
    Cleans text and extracts language and word count.
    Returns (cleaned_text, language_code, word_count)
    """
    cleaned_text = clean_text(text)
    word_count = len(cleaned_text.split())
    
    language = "unknown"
    try:
        if cleaned_text:
            language = detect(cleaned_text)
    except Exception:
        pass
        
    return cleaned_text, language, word_count
