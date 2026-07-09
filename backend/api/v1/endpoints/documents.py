from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from typing import List
import uuid
import os
import shutil
import logging
from schemas.document import DocumentResponse, DocumentStatus
from datetime import datetime
from services.documents.pipeline import process_document

router = APIRouter()

UPLOAD_DIR = "uploads/temp"
os.makedirs(UPLOAD_DIR, exist_ok=True)
logger = logging.getLogger(__name__)

def background_process_document(document_id: str, file_path: str, original_filename: str):
    try:
        logger.info(f"Starting processing for document {document_id}")
        process_document(file_path, original_filename)
        logger.info(f"Successfully processed document {document_id}")
    except Exception as exc:
        logger.error(f"Failed to process document {document_id}: {str(exc)}")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(file: UploadFile = File(...), background_tasks: BackgroundTasks = BackgroundTasks()):
    """
    Uploads a document and queues it for processing.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")
        
    document_id = str(uuid.uuid4())
    file_extension = os.path.splitext(file.filename)[1]
    temp_file_path = os.path.join(UPLOAD_DIR, f"{document_id}{file_extension}")
    
    # Save file to temp storage
    try:
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not save file: {str(e)}")
        
    file_size = os.path.getsize(temp_file_path)
    
    # Trigger Task (Using BackgroundTasks instead of Celery for local environments without Redis)
    background_tasks.add_task(background_process_document, document_id, temp_file_path, file.filename)
    
    # In a real implementation, this would be saved to DB and returned
    return DocumentResponse(
        id=document_id,
        filename=file.filename,
        file_size=file_size,
        mime_type=file.content_type or "application/octet-stream",
        status=DocumentStatus.PENDING,
        uploaded_at=datetime.utcnow()
    )

@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document_status(document_id: str):
    """
    Retrieves the status of a document. (Mocked)
    """
    # Mock response
    return DocumentResponse(
        id=document_id,
        filename="mock_file.pdf",
        file_size=1024,
        mime_type="application/pdf",
        status=DocumentStatus.PROCESSING,
        uploaded_at=datetime.utcnow()
    )
