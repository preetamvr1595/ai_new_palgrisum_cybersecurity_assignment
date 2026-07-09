from celery import shared_task
import logging
from services.documents.pipeline import process_document
from services.grammar.pipeline import process_grammar
from schemas.grammar import CorrectionMode, WritingMode, GrammarResponse
import uuid
import time
import asyncio

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def batch_grammar_check_task(self, document_id: str, file_path: str, original_filename: str, c_mode: str, w_mode: str):
    """
    Celery task that combines Phase 9 extraction with Phase 15 Grammar Analysis for large documents.
    """
    logger.info(f"Starting batch grammar check for {document_id}")
    start_time = time.time()
    
    try:
        # 1. Extract Text
        extraction_result = process_document(file_path, original_filename)
        text = extraction_result["text"]
        
        # We must run the async pipeline synchronously within Celery
        loop = asyncio.get_event_loop()
        correction_mode = CorrectionMode(c_mode)
        writing_mode = WritingMode(w_mode)
        
        result = loop.run_until_complete(
            process_grammar(text, correction_mode, writing_mode)
        )
        
        # 3. Generate Report
        report_id = str(uuid.uuid4())
        response = GrammarResponse(
            report_id=report_id,
            original_text=text,
            corrected_text=result["corrected_text"],
            detected_tone=result["detected_tone"],
            scores=result["scores"],
            suggestions=result["suggestions"],
            generation_time_ms=int((time.time() - start_time) * 1000)
        )
        
        logger.info(f"Successfully analyzed document {document_id}")
        
        # db.save_grammar_report(response.dict())
        
        return {"status": "SUCCESS", "report_id": report_id}
        
    except Exception as exc:
        logger.error(f"Failed to check grammar for document {document_id}: {str(exc)}")
        raise self.retry(exc=exc, countdown=60)
