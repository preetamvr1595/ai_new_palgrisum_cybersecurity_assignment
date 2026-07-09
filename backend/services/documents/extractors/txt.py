from typing import Dict, Any, Tuple
import os

def extract_txt(file_path: str) -> Tuple[str, Dict[str, Any]]:
    """
    Extracts text from a TXT file. Attempts to handle encoding gracefully.
    """
    text_content = ""
    encoding = "utf-8"
    
    # Attempt UTF-8 first, fallback to Latin-1
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text_content = f.read()
    except UnicodeDecodeError:
        encoding = "latin-1"
        with open(file_path, 'r', encoding='latin-1') as f:
            text_content = f.read()

    metadata = {
        "file_size": os.path.getsize(file_path),
        "encoding": encoding,
        "line_count": len(text_content.splitlines())
    }

    return text_content, metadata
