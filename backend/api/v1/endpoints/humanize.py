from fastapi import APIRouter, HTTPException, BackgroundTasks
from schemas.humanizer import HumanizerRequest, HumanizerResponse
from services.humanizer.pipeline import process_humanization
import uuid
import time

router = APIRouter()

@router.post("/", response_model=HumanizerResponse)
async def humanize_text(request: HumanizerRequest):
    """
    Synchronous endpoint to humanize a snippet of text.
    """
    start_time = time.time()
    
    if not request.text or len(request.text.strip()) < 20:
        raise HTTPException(status_code=400, detail="Text too short for humanization.")
        
    report_id = str(uuid.uuid4())
    
    # Run Pipeline
    try:
        result = await process_humanization(request.text, request.mode, request.strength)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Humanization failed: {str(e)}")
        
    response = HumanizerResponse(
        report_id=report_id,
        original_text=request.text,
        humanized_text=result["humanized_text"],
        mode=request.mode,
        strength=request.strength,
        quality_scores=result["quality_scores"],
        diff_view=result["diff_view"],
        generation_time_ms=int((time.time() - start_time) * 1000)
    )
    
    # db.save_humanizer_report(response.dict())
    
    return response

@router.get("/report/{report_id}")
async def get_humanize_report(report_id: str):
    """
    Mock endpoint to fetch past humanizer reports.
    """
    return {"message": f"Details for humanized report {report_id} would be fetched here."}
