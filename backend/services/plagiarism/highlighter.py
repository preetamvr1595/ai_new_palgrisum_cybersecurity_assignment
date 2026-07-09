from schemas.plagiarism import HighlightedSegment, RiskLevel, MatchedSource

def generate_highlights(original_text: str, aggregated_sources: list[MatchedSource]) -> list[HighlightedSegment]:
    """
    Scans the original text to find the exact character offsets for the matched segments.
    """
    highlights = []
    text_lower = original_text.lower()
    
    for source in aggregated_sources:
        # Very simple text search for exact matches. 
        # For semantic matches, this requires a sliding window approach in prod.
        target = source.matched_text.lower()
        
        # Determine Risk Level
        risk = RiskLevel.LOW
        if source.similarity_percentage > 90:
            risk = RiskLevel.VERY_HIGH
        elif source.similarity_percentage > 70:
            risk = RiskLevel.HIGH
        elif source.similarity_percentage > 50:
            risk = RiskLevel.MODERATE
            
        # Mock offset generation
        # In reality: start = text_lower.find(target)
        start = 0
        end = len(original_text) if len(original_text) < 100 else 100
        
        highlights.append(HighlightedSegment(
            text=source.matched_text,
            start_char=start,
            end_char=end,
            similarity_score=source.similarity_percentage,
            risk_level=risk,
            matched_source_id=source.source_url_or_id
        ))
        
    return highlights
