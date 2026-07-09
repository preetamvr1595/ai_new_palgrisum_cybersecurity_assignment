from celery import shared_task
import logging
from services.research.doc_analysis_engine import analyze_document
from services.research.knowledge_extractor import extract_knowledge_graph
from schemas.research import ResearchReport
import uuid
import time

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def batch_document_analysis_task(self, document_id: str, file_path: str, original_filename: str):
    """
    Celery task for deeply analyzing a large document, extracting insights, and building a Knowledge Graph.
    """
    logger.info(f"Starting batch document analysis for {document_id}")
    start_time = time.time()
    
    try:
        # 1. Analyze Document (Integrates with Phase 9)
        analysis_result = analyze_document(document_id, file_path, original_filename)
        
        # 2. Extract Knowledge Graph
        # We pass a mocked string here, but in prod we pass the full extracted text
        graph = extract_knowledge_graph(analysis_result["executive_summary"])
        
        # 3. Generate Report
        report_id = str(uuid.uuid4())
        response = ResearchReport(
            report_id=report_id,
            title=analysis_result["title"],
            executive_summary=analysis_result["executive_summary"],
            detailed_findings=analysis_result["detailed_findings"],
            key_insights=analysis_result["key_insights"],
            discovered_sources=[],
            knowledge_graph=graph,
            generation_time_ms=int((time.time() - start_time) * 1000)
        )
        
        logger.info(f"Successfully analyzed document {document_id}")
        
        # db.save_research_report(response.dict())
        
        return {"status": "SUCCESS", "report_id": report_id}
        
    except Exception as exc:
        logger.error(f"Failed to analyze document {document_id}: {str(exc)}")
        raise self.retry(exc=exc, countdown=60)
