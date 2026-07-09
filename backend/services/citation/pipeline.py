from .metadata_extractor import extract_metadata
from .formatter import format_citation
from schemas.citation import CitationRequest, FormattedCitation

def process_citation_request(request: CitationRequest) -> FormattedCitation:
    """
    Orchestrates the entire Citation Pipeline: extraction -> validation -> formatting.
    """
    # 1. Metadata Extraction / Resolution
    metadata = extract_metadata(doi=request.doi, url=request.url, manual_data=request.manual_metadata)
    
    # 2. Validation (Mocked: Ensure required fields exist)
    if not metadata.title:
        metadata.title = "Untitled Source"
        
    # 3. Style Formatting
    formatted = format_citation(metadata, request.style)
    
    return formatted
