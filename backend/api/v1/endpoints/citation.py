from fastapi import APIRouter, HTTPException
from schemas.citation import CitationRequest, CitationResponse, ReferenceMetadata, ExportFormat
from services.citation.pipeline import process_citation_request
from services.citation.export_framework import export_references
import uuid
import time
from fastapi.responses import PlainTextResponse

router = APIRouter()

@router.post("/generate", response_model=CitationResponse)
async def generate_citation(request: CitationRequest):
    """
    Synchronous endpoint to generate a citation from DOI, URL, or Manual Entry.
    """
    start_time = time.time()
    
    if not request.doi and not request.url and not request.manual_metadata:
        raise HTTPException(status_code=400, detail="Must provide DOI, URL, or manual_metadata.")
        
    citation_id = str(uuid.uuid4())
    
    try:
        formatted = process_citation_request(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Citation generation failed: {str(e)}")
        
    response = CitationResponse(
        citation_id=citation_id,
        formatted=formatted,
        generation_time_ms=int((time.time() - start_time) * 1000)
    )
    
    return response

@router.post("/export")
async def export_bibliography(references: list[ReferenceMetadata], format: ExportFormat = ExportFormat.BIBTEX):
    """
    Exports a list of references into a BibTeX or JSON string.
    """
    try:
        export_string = export_references(references, format)
        return PlainTextResponse(export_string)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")
