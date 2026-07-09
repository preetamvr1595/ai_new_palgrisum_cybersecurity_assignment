import magic
from .validation import validate_file
from .security import scan_file_for_viruses
from .cleaner import extract_content_metadata
from .extractors.pdf import extract_pdf
from .extractors.docx import extract_docx
from .extractors.txt import extract_txt
from .extractors.csv import extract_csv
from typing import Dict, Any

class DocumentProcessingError(Exception):
    pass

def process_document(file_path: str, original_filename: str) -> Dict[str, Any]:
    """
    Orchestrates the entire document processing pipeline:
    1. Validate
    2. Security Scan
    3. Extract Text & Metadata based on mime type
    4. Clean & Analyze text
    """
    
    # 1. Validation
    validate_file(file_path, original_filename)
    
    # 2. Security Scan
    scan_file_for_viruses(file_path)
    
    # 3. Extraction
    mime = magic.Magic(mime=True)
    detected_mime = mime.from_file(file_path)
    
    raw_text = ""
    file_metadata = {}
    
    if detected_mime == 'application/pdf':
        raw_text, file_metadata = extract_pdf(file_path)
    elif detected_mime == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        raw_text, file_metadata = extract_docx(file_path)
    elif detected_mime == 'text/plain':
        raw_text, file_metadata = extract_txt(file_path)
    elif detected_mime == 'text/csv':
        raw_text, file_metadata = extract_csv(file_path)
    else:
        raise DocumentProcessingError(f"Extractor not implemented for mime type: {detected_mime}")
        
    # 4. Cleaning and Analysis
    cleaned_text, language, word_count = extract_content_metadata(raw_text)
    
    return {
        "text": cleaned_text,
        "language": language,
        "word_count": word_count,
        "metadata": file_metadata
    }
