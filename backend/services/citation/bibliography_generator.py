from schemas.citation import FormattedCitation

def generate_bibliography(citations: list[FormattedCitation]) -> list[str]:
    """
    Takes a list of formatted citations, sorts them alphabetically by Author (standard for APA/MLA),
    and returns a clean list of strings ready to be rendered in a UI or PDF.
    """
    
    # Sort alphabetically by the full reference string (which starts with Author usually)
    sorted_citations = sorted(citations, key=lambda x: x.full_reference.lower())
    
    return [c.full_reference for c in sorted_citations]
