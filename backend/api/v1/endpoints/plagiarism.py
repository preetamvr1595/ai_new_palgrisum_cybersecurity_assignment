from fastapi import APIRouter, HTTPException, BackgroundTasks
from schemas.plagiarism import PlagiarismRequest, PlagiarismReport
from services.plagiarism.pipeline import process_plagiarism_check
import uuid
import time

router = APIRouter()

@router.post("/check", response_model=PlagiarismReport)
async def check_plagiarism(request: PlagiarismRequest):
    """
    Synchronous endpoint to check plagiarism against the internal content index.
    """
    start_time = time.time()
    
    if not request.text or len(request.text.strip()) == 0:
        raise HTTPException(status_code=400, detail="Text cannot be empty.")
        
    report_id = str(uuid.uuid4())
    
    try:
        result = process_plagiarism_check(request.text, request.threshold)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Plagiarism check failed: {str(e)}")
        
    response = PlagiarismReport(
        report_id=report_id,
        overall_similarity_percentage=result["overall_similarity_percentage"],
        risk_level=result["risk_level"],
        matched_sources=result["matched_sources"],
        highlighted_segments=result["highlighted_segments"],
        generation_time_ms=int((time.time() - start_time) * 1000)
    )
    
    return response

@router.get("/report/{report_id}")
async def get_plagiarism_report(report_id: str):
    """
    Mock endpoint to fetch past plagiarism reports.
    """
    return {"message": f"Details for plagiarism report {report_id} would be fetched here."}
