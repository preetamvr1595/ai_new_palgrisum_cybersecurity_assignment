from schemas.plagiarism import MatchedSource, MatchType

def aggregate_matches(exact_matches: list[dict], semantic_matches: list[dict]) -> list[MatchedSource]:
    """
    Merges exact matches and semantic matches, prioritizing exact matches to prevent duplicate flagging of the same source.
    """
    final_sources = []
    seen_sources = set()
    
    # Add Exact Matches First
    for m in exact_matches:
        source = MatchedSource(
            source_url_or_id=m["source_id"],
            source_name=m["source_name"],
            matched_text=m["matched_text"],
            similarity_percentage=m["similarity"] * 100,
            match_type=MatchType(m["type"])
        )
        final_sources.append(source)
        seen_sources.add(m["source_id"])
        
    # Add Semantic Matches (if not already exact-matched)
    for m in semantic_matches:
        if m["source_id"] not in seen_sources:
            source = MatchedSource(
                source_url_or_id=m["source_id"],
                source_name=m["source_name"],
                matched_text=m["matched_text"],
                similarity_percentage=m["similarity"] * 100,
                match_type=MatchType(m["type"])
            )
            final_sources.append(source)
            seen_sources.add(m["source_id"])
            
    return final_sources
