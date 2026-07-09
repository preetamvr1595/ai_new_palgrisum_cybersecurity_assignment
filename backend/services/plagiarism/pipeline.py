from .fingerprinter import find_exact_matches
from .semantic_search import semantic_engine
from .aggregator import aggregate_matches
from .highlighter import generate_highlights
from schemas.plagiarism import RiskLevel

def process_plagiarism_check(text: str, threshold: float) -> dict:
    """
    Orchestrates the Plagiarism Detection Pipeline.
    """
    
    # 1. Exact Match Scan (N-Grams)
    exact_matches = find_exact_matches(text)
    
    # 2. Semantic Match Scan (Embeddings)
    semantic_matches = semantic_engine.search_embeddings(text, threshold=threshold)
    
    # 3. Aggregation
    aggregated_sources = aggregate_matches(exact_matches, semantic_matches)
    
    # 4. Highlight Mapping
    highlights = generate_highlights(text, aggregated_sources)
    
    # 5. Overall Calculation
    overall_sim = 0.0
    risk_level = RiskLevel.LOW
    
    if aggregated_sources:
        # Simplified: max similarity found
        overall_sim = max([s.similarity_percentage for s in aggregated_sources])
        
        if overall_sim > 80:
            risk_level = RiskLevel.VERY_HIGH
        elif overall_sim > 50:
            risk_level = RiskLevel.HIGH
        elif overall_sim > 20:
            risk_level = RiskLevel.MODERATE
            
    return {
        "overall_similarity_percentage": overall_sim,
        "risk_level": risk_level,
        "matched_sources": aggregated_sources,
        "highlighted_segments": highlights
    }
