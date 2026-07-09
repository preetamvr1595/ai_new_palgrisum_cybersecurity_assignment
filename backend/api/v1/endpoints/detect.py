from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional
import uuid
import time

from schemas.detection import DetectionReport
from services.detector.explainer import explain_text
from services.detector.aggregator import aggregate_scores, calculate_risk_category
from services.detector.drift_monitor import drift_monitor
from services.detector.report_generator import generate_pdf_report

router = APIRouter()

class TextDetectRequest(BaseModel):
    text: str
    document_id: Optional[str] = None

@router.post("/", response_model=DetectionReport)
async def detect_text(request: TextDetectRequest, background_tasks: BackgroundTasks):
    """
    Synchronous endpoint for short-to-medium text detection.
    """
    start_time = time.time()
    
    if not request.text or len(request.text.strip()) < 50:
        raise HTTPException(status_code=400, detail="Text too short for reliable analysis.")
        
    report_id = str(uuid.uuid4())
    
    # 1. Explainability & Inference
    paragraph_analyses = explain_text(request.text)
    
    # 2. Aggregation
    para_scores = [p.ai_probability for p in paragraph_analyses]
    aggregated = aggregate_scores(para_scores)
    
    # 3. Log to Drift Monitor
    drift_monitor.log_prediction(aggregated["overall_ai_score"])
    
    # 4. Construct Report
    report = DetectionReport(
        report_id=report_id,
        document_id=request.document_id,
        overall_human_score=aggregated["overall_human_score"],
        overall_ai_score=aggregated["overall_ai_score"],
        overall_confidence=aggregated["overall_confidence"],
        risk_classification=calculate_risk_category(aggregated["overall_ai_score"]),
        paragraph_breakdown=paragraph_analyses,
        generation_time_ms=int((time.time() - start_time) * 1000)
    )
    
    # Optionally queue a background task to save the report to the DB or generate a PDF
    background_tasks.add_task(generate_pdf_report, report)
    
    return report

@router.get("/report/{report_id}")
async def get_report_pdf(report_id: str):
    """
    Mock endpoint to fetch the PDF report (in reality, return FileResponse)
    """
    return {"message": f"Report {report_id} would be downloaded here."}
