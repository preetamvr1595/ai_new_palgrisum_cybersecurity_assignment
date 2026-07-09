from celery import shared_task
import logging
from services.documents.pipeline import process_document
from services.paraphraser.pipeline import process_paraphrase
from schemas.paraphraser import ParaphraseMode, ParaphraseStrength, ParaphraseResponse
import uuid
import time
import asyncio

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def batch_paraphrase_document_task(self, document_id: str, file_path: str, original_filename: str, mode: str, strength: str, protected_keywords: list):
    """
    Celery task that combines Phase 9 extraction with Phase 14 Paraphrasing for large documents.
    """
    logger.info(f"Starting batch paraphrasing for {document_id}")
    start_time = time.time()
    
    try:
        # 1. Extract Text (Phase 9)
        extraction_result = process_document(file_path, original_filename)
        text = extraction_result["text"]
        
        # We must run the async pipeline synchronously within Celery
        loop = asyncio.get_event_loop()
        p_mode = ParaphraseMode(mode)
        p_strength = ParaphraseStrength(strength)
        
        result = loop.run_until_complete(
            process_paraphrase(text, p_mode, p_strength, protected_keywords)
        )
        
        # 3. Generate Report
        report_id = str(uuid.uuid4())
        response = ParaphraseResponse(
            report_id=report_id,
            original_text=text,
            paraphrased_text=result["paraphrased_text"],
            mode=p_mode,
            strength=p_strength,
            protected_keywords=protected_keywords,
            quality_metrics=result["quality_metrics"],
            diff_view=result["diff_view"],
            generation_time_ms=int((time.time() - start_time) * 1000)
        )
        
        logger.info(f"Successfully paraphrased document {document_id}")
        
        # db.save_paraphraser_report(response.dict())
        
        return {"status": "SUCCESS", "report_id": report_id}
        
    except Exception as exc:
        logger.error(f"Failed to paraphrase document {document_id}: {str(exc)}")
        raise self.retry(exc=exc, countdown=60)
