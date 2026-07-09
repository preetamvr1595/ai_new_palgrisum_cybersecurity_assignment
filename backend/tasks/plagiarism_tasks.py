from celery import shared_task
import logging
from services.documents.pipeline import process_document
from services.plagiarism.pipeline import process_plagiarism_check
from schemas.plagiarism import PlagiarismReport
import uuid
import time

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def batch_plagiarism_check_task(self, document_id: str, file_path: str, original_filename: str, threshold: float):
    """
    Celery task that combines Phase 9 extraction with Phase 16 Plagiarism Check for large documents.
    """
    logger.info(f"Starting batch plagiarism check for {document_id}")
    start_time = time.time()
    
    try:
        # 1. Extract Text
        extraction_result = process_document(file_path, original_filename)
        text = extraction_result["text"]
        
        # 2. Process
        result = process_plagiarism_check(text, threshold)
        
        # 3. Generate Report
        report_id = str(uuid.uuid4())
        response = PlagiarismReport(
            report_id=report_id,
            overall_similarity_percentage=result["overall_similarity_percentage"],
            risk_level=result["risk_level"],
            matched_sources=result["matched_sources"],
            highlighted_segments=result["highlighted_segments"],
            generation_time_ms=int((time.time() - start_time) * 1000)
        )
        
        logger.info(f"Successfully checked plagiarism for document {document_id}")
        
        # db.save_plagiarism_report(response.dict())
        
        return {"status": "SUCCESS", "report_id": report_id}
        
    except Exception as exc:
        logger.error(f"Failed to check plagiarism for document {document_id}: {str(exc)}")
        raise self.retry(exc=exc, countdown=60)
