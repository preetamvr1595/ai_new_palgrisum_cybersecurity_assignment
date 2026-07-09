from celery import shared_task
import logging
from services.documents.pipeline import process_document
from services.detector.explainer import explain_text
from services.detector.aggregator import aggregate_scores, calculate_risk_category
from services.detector.report_generator import generate_pdf_report
from schemas.detection import DetectionReport
import uuid
import time

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def batch_analyze_document_task(self, document_id: str, file_path: str, original_filename: str):
    """
    Celery task that combines Phase 9 extraction with Phase 12 detection.
    """
    logger.info(f"Starting batch analysis for {document_id}")
    start_time = time.time()
    
    try:
        # 1. Extract Text (Phase 9)
        extraction_result = process_document(file_path, original_filename)
        text = extraction_result["text"]
        
        # 2. Detect (Phase 12)
        paragraph_analyses = explain_text(text)
        para_scores = [p.ai_probability for p in paragraph_analyses]
        aggregated = aggregate_scores(para_scores)
        
        # 3. Generate Report
        report_id = str(uuid.uuid4())
        report = DetectionReport(
            report_id=report_id,
            document_id=document_id,
            overall_human_score=aggregated["overall_human_score"],
            overall_ai_score=aggregated["overall_ai_score"],
            overall_confidence=aggregated["overall_confidence"],
            risk_classification=calculate_risk_category(aggregated["overall_ai_score"]),
            paragraph_breakdown=paragraph_analyses,
            generation_time_ms=int((time.time() - start_time) * 1000)
        )
        
        # Save PDF report
        pdf_path = generate_pdf_report(report)
        logger.info(f"Successfully generated report PDF at {pdf_path}")
        
        # db.save_report(report.dict())
        
        return {"status": "SUCCESS", "report_id": report_id}
        
    except Exception as exc:
        logger.error(f"Failed to analyze document {document_id}: {str(exc)}")
        raise self.retry(exc=exc, countdown=60)
