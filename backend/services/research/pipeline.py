from .query_engine import explore_topic
from .lit_review_engine import generate_literature_review
from .knowledge_extractor import extract_knowledge_graph
from schemas.research import ResearchQueryRequest, ResearchMode

async def process_research_query(request: ResearchQueryRequest) -> dict:
    """
    Master orchestrator for the Research Assistant.
    """
    
    if request.mode == ResearchMode.EXPLORE:
        sources = await explore_topic(request.query)
        # Mocking an insight generation step
        graph = extract_knowledge_graph(request.query)
        
        return {
            "title": f"Exploration: {request.query}",
            "executive_summary": "Here are the top sources and knowledge concepts related to your query.",
            "detailed_findings": [],
            "key_insights": ["The field is highly active with multiple recent publications."],
            "discovered_sources": sources,
            "knowledge_graph": graph
        }
        
    elif request.mode == ResearchMode.LIT_REVIEW:
        # In a real pipeline, we'd fetch the sources first, then review them.
        sources = await explore_topic(request.query)
        review = await generate_literature_review(request.query, sources)
        
        return {
            "title": review["title"],
            "executive_summary": review["executive_summary"],
            "detailed_findings": review["detailed_findings"],
            "key_insights": review["key_insights"],
            "discovered_sources": sources,
            "knowledge_graph": None
        }
    
    else:
        raise ValueError("Unsupported Research Mode")
