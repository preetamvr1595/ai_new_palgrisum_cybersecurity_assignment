from fastapi import APIRouter, HTTPException, BackgroundTasks
from schemas.paraphraser import ParaphraseRequest, ParaphraseResponse
from services.paraphraser.pipeline import process_paraphrase
import uuid
import time

router = APIRouter()

@router.post("/", response_model=ParaphraseResponse)
async def paraphrase_text(request: ParaphraseRequest):
    """
    Synchronous endpoint to paraphrase a snippet of text.
    """
    start_time = time.time()
    
    if not request.text or len(request.text.strip()) < 10:
        raise HTTPException(status_code=400, detail="Text too short for paraphrasing.")
        
    report_id = str(uuid.uuid4())
    
    # Run Pipeline
    try:
        result = await process_paraphrase(
            text=request.text, 
            mode=request.mode, 
            strength=request.strength, 
            protected_keywords=request.protected_keywords
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Paraphrasing failed: {str(e)}")
        
    response = ParaphraseResponse(
        report_id=report_id,
        original_text=request.text,
        paraphrased_text=result["paraphrased_text"],
        mode=request.mode,
        strength=request.strength,
        protected_keywords=request.protected_keywords,
        quality_metrics=result["quality_metrics"],
        diff_view=result["diff_view"],
        generation_time_ms=int((time.time() - start_time) * 1000)
    )
    
    return response

@router.get("/report/{report_id}")
async def get_paraphrase_report(report_id: str):
    """
    Mock endpoint to fetch past paraphrase reports.
    """
    return {"message": f"Details for paraphrase report {report_id} would be fetched here."}
