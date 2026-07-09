import logging
from services.documents.pipeline import process_document

logger = logging.getLogger(__name__)

def analyze_document(document_id: str, file_path: str, original_filename: str) -> dict:
    """
    Interfaces with Phase 9 Extraction to read a document and generate summaries.
    """
    logger.info(f"Analyzing Document: {document_id}")
    
    # 1. Extract Text
    extraction = process_document(file_path, original_filename)
    text = extraction["text"]
    
    # 2. Mock Analysis
    return {
        "title": original_filename,
        "executive_summary": "An in-depth analysis of the provided document text.",
        "detailed_findings": [
            f"The document contains {len(text.split())} words.",
            "Primary themes detected align with the research query."
        ],
        "key_insights": [
            "Insight 1 extracted from document.",
            "Insight 2 extracted from document."
        ]
    }
