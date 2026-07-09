from celery import shared_task
from services.documents.pipeline import process_document
import logging
import os

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def process_document_task(self, document_id: str, file_path: str, original_filename: str):
    """
    Celery task to handle asynchronous document processing.
    """
    logger.info(f"Starting processing for document {document_id}")
    
    try:
        # Update database status to PROCESSING here (mocked for now)
        # db.update_document_status(document_id, "PROCESSING")
        
        result = process_document(file_path, original_filename)
        
        # Save result to database (mocked for now)
        # db.save_document_analysis(document_id, result)
        # db.update_document_status(document_id, "COMPLETED")
        
        logger.info(f"Successfully processed document {document_id}. Word count: {result['word_count']}")
        
        # Cleanup temp file
        if os.path.exists(file_path):
            os.remove(file_path)
            
        return {"status": "SUCCESS", "document_id": document_id}
        
    except Exception as exc:
        logger.error(f"Failed to process document {document_id}: {str(exc)}")
        # db.update_document_status(document_id, "FAILED")
        
        # Cleanup temp file on failure
        if os.path.exists(file_path):
            os.remove(file_path)
            
        # Retry for transient errors
        raise self.retry(exc=exc, countdown=60)
