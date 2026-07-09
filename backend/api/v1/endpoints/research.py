from fastapi import APIRouter, HTTPException, BackgroundTasks
from schemas.research import ResearchQueryRequest, ResearchReport
from services.research.pipeline import process_research_query
import uuid
import time

router = APIRouter()

@router.post("/query", response_model=ResearchReport)
async def query_research(request: ResearchQueryRequest):
    """
    Synchronous endpoint for topic exploration and generating short literature reviews.
    """
    start_time = time.time()
    
    if not request.query or len(request.query.strip()) == 0:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
        
    report_id = str(uuid.uuid4())
    
    try:
        result = await process_research_query(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Research processing failed: {str(e)}")
        
    response = ResearchReport(
        report_id=report_id,
        title=result["title"],
        executive_summary=result["executive_summary"],
        detailed_findings=result["detailed_findings"],
        key_insights=result["key_insights"],
        discovered_sources=result.get("discovered_sources", []),
        knowledge_graph=result.get("knowledge_graph"),
        generation_time_ms=int((time.time() - start_time) * 1000)
    )
    
    return response

@router.get("/report/{report_id}")
async def get_research_report(report_id: str):
    """
    Mock endpoint to fetch past research reports.
    """
    return {"message": f"Details for research report {report_id} would be fetched here."}
