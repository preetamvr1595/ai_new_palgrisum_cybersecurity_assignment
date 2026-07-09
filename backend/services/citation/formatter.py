from schemas.citation import ReferenceMetadata, CitationStyle, FormattedCitation

def _format_apa_7(meta: ReferenceMetadata) -> FormattedCitation:
    authors = ", ".join(meta.authors) if meta.authors else "Unknown Author"
    year = f"({meta.publication_year})" if meta.publication_year else "(n.d.)"
    
    # Construct Full Reference
    if meta.source_type == "journal_article":
        full = f"{authors}. {year}. {meta.title}. {meta.journal_name}, {meta.volume}. https://doi.org/{meta.doi}"
    elif meta.source_type == "website":
        full = f"{authors}. {year}. {meta.title}. {meta.publisher}. Retrieved {meta.access_date}, from {meta.url}"
    else:
        full = f"{authors}. {year}. {meta.title}. {meta.publisher}."

    # Construct In-Text
    first_author = meta.authors[0].split(",")[0] if meta.authors else "Unknown"
    in_text = f"({first_author}, {meta.publication_year or 'n.d.'})"
    
    return FormattedCitation(in_text=in_text, full_reference=full, style=CitationStyle.APA_7, metadata=meta)

def _format_mla_9(meta: ReferenceMetadata) -> FormattedCitation:
    authors = ", ".join(meta.authors) if meta.authors else "Unknown Author"
    
    # Construct Full Reference
    if meta.source_type == "journal_article":
        full = f"{authors}. \"{meta.title}.\" {meta.journal_name}, vol. {meta.volume}, {meta.publication_year}. DOI: {meta.doi}."
    elif meta.source_type == "website":
        full = f"{authors}. \"{meta.title}.\" {meta.publisher}, {meta.publication_year}, {meta.url}. Accessed {meta.access_date}."
    else:
        full = f"{authors}. {meta.title}. {meta.publisher}, {meta.publication_year}."

    # Construct In-Text
    first_author = meta.authors[0].split(",")[0] if meta.authors else "Unknown"
    in_text = f"({first_author})"
    
    return FormattedCitation(in_text=in_text, full_reference=full, style=CitationStyle.MLA_9, metadata=meta)

def format_citation(metadata: ReferenceMetadata, style: CitationStyle) -> FormattedCitation:
    """
    Routes the metadata through the appropriate style template engine.
    """
    if style == CitationStyle.APA_7:
        return _format_apa_7(metadata)
    elif style == CitationStyle.MLA_9:
        return _format_mla_9(metadata)
    else:
        # Fallback to APA for unsupported mocked styles
        return _format_apa_7(metadata)
