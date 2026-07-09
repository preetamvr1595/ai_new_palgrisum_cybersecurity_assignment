from typing import Optional, List
import uuid
from sqlalchemy.orm import Session
from backend.db.models.document import Document
from backend.repository.base import CRUDBase
from pydantic import BaseModel

class DocumentCreate(BaseModel):
    user_id: uuid.UUID
    title: str
    file_name: Optional[str] = None
    file_type: Optional[str] = None
    file_size: Optional[int] = None
    storage_path: Optional[str] = None
    word_count: Optional[int] = None

class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    file_name: Optional[str] = None
    file_type: Optional[str] = None
    file_size: Optional[int] = None
    storage_path: Optional[str] = None
    word_count: Optional[int] = None
    status: Optional[str] = None

class CRUDDocument(CRUDBase[Document, DocumentCreate, DocumentUpdate]):
    def get_by_user(self, db: Session, *, user_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[Document]:
        return db.query(Document).filter(Document.user_id == user_id).offset(skip).limit(limit).all()

document_repo = CRUDDocument(Document)
