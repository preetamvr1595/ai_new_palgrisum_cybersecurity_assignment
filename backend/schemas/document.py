from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum

class DocumentStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class DocumentBase(BaseModel):
    filename: str
    file_size: int
    mime_type: str

class DocumentCreate(DocumentBase):
    owner_id: str

class DocumentResponse(DocumentBase):
    id: str
    status: DocumentStatus
    uploaded_at: datetime
    metadata_extracted: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True

class DocumentAnalysis(BaseModel):
    document_id: str
    extracted_text: str
    language: str
    word_count: int
    page_count: Optional[int] = None
