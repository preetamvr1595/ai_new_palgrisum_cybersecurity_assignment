from celery import shared_task
import logging
from services.documents.pipeline import process_document
from services.humanizer.pipeline import process_humanization
from schemas.humanizer import HumanizationMode, HumanizationStrength, HumanizerResponse
import uuid
import time
import asyncio

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def batch_humanize_document_task(self, document_id: str, file_path: str, original_filename: str, mode: str, strength: str):
    """
    Celery task that combines Phase 9 extraction with Phase 13 Humanization for large documents.
    """
    logger.info(f"Starting batch humanization for {document_id}")
    start_time = time.time()
    
    try:
        # 1. Extract Text (Phase 9)
        extraction_result = process_document(file_path, original_filename)
        text = extraction_result["text"]
        
        # We must run the async pipeline synchronously within Celery
        loop = asyncio.get_event_loop()
        h_mode = HumanizationMode(mode)
        h_strength = HumanizationStrength(strength)
        
        result = loop.run_until_complete(process_humanization(text, h_mode, h_strength))
        
        # 3. Generate Report
        report_id = str(uuid.uuid4())
        response = HumanizerResponse(
            report_id=report_id,
            original_text=text,
            humanized_text=result["humanized_text"],
            mode=h_mode,
            strength=h_strength,
            quality_scores=result["quality_scores"],
            diff_view=result["diff_view"],
            generation_time_ms=int((time.time() - start_time) * 1000)
        )
        
        logger.info(f"Successfully humanized document {document_id}")
        
        # db.save_humanizer_report(response.dict())
        
        return {"status": "SUCCESS", "report_id": report_id}
        
    except Exception as exc:
        logger.error(f"Failed to humanize document {document_id}: {str(exc)}")
        raise self.retry(exc=exc, countdown=60)
