import magic
import os

ALLOWED_MIME_TYPES = {
    'application/pdf': '.pdf',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',
    'text/plain': '.txt',
    'text/csv': '.csv'
}

MAX_FILE_SIZE_MB = 50
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

class DocumentValidationError(Exception):
    pass

def validate_file(file_path: str, original_filename: str):
    """
    Validates the file size and mime type using python-magic.
    """
    if not os.path.exists(file_path):
        raise DocumentValidationError("File does not exist.")
        
    file_size = os.path.getsize(file_path)
    if file_size > MAX_FILE_SIZE_BYTES:
        raise DocumentValidationError(f"File exceeds maximum allowed size of {MAX_FILE_SIZE_MB}MB.")
        
    # Strictly validate mime type
    mime = magic.Magic(mime=True)
    detected_mime = mime.from_file(file_path)
    
    if detected_mime not in ALLOWED_MIME_TYPES:
        raise DocumentValidationError(f"Unsupported file type: {detected_mime}. Allowed types: PDF, DOCX, TXT, CSV.")
        
    return True
