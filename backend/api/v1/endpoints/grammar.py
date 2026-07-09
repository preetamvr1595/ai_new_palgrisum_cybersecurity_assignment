from fastapi import APIRouter, HTTPException, BackgroundTasks
from schemas.grammar import GrammarRequest, GrammarResponse
from services.grammar.pipeline import process_grammar
import uuid
import time

router = APIRouter()

@router.post("/check", response_model=GrammarResponse)
async def check_grammar(request: GrammarRequest):
    """
    Synchronous endpoint to check grammar and style for a snippet of text.
    """
    start_time = time.time()
    
    if not request.text or len(request.text.strip()) == 0:
        raise HTTPException(status_code=400, detail="Text cannot be empty.")
        
    report_id = str(uuid.uuid4())
    
    try:
        result = await process_grammar(request.text, request.correction_mode, request.writing_mode)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Grammar analysis failed: {str(e)}")
        
    response = GrammarResponse(
        report_id=report_id,
        original_text=request.text,
        corrected_text=result["corrected_text"],
        detected_tone=result["detected_tone"],
        scores=result["scores"],
        suggestions=result["suggestions"],
        generation_time_ms=int((time.time() - start_time) * 1000)
    )
    
    return response

@router.get("/report/{report_id}")
async def get_grammar_report(report_id: str):
    """
    Mock endpoint to fetch past grammar reports.
    """
    return {"message": f"Details for grammar report {report_id} would be fetched here."}
