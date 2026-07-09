from schemas.citation import ReferenceMetadata, ExportFormat

def _generate_bibtex(meta: ReferenceMetadata) -> str:
    """
    Converts Pydantic metadata into a standard BibTeX string.
    """
    cite_key = f"{meta.authors[0].split(',')[0].lower()}{meta.publication_year}" if meta.authors else "unknown"
    
    entry_type = "article" if meta.source_type == "journal_article" else "misc"
    
    bib = f"@{entry_type}{{{cite_key},\n"
    bib += f"  title = {{{meta.title}}},\n"
    if meta.authors:
        bib += f"  author = {{{' and '.join(meta.authors)}}},\n"
    if meta.publication_year:
        bib += f"  year = {{{meta.publication_year}}},\n"
    if meta.journal_name:
        bib += f"  journal = {{{meta.journal_name}}},\n"
    if meta.doi:
        bib += f"  doi = {{{meta.doi}}},\n"
    if meta.url:
        bib += f"  url = {{{meta.url}}},\n"
    bib += "}"
    
    return bib

def export_references(metadata_list: list[ReferenceMetadata], format_type: ExportFormat) -> str:
    """
    Generates a downloadable export file string.
    """
    if format_type == ExportFormat.BIBTEX:
        return "\n\n".join([_generate_bibtex(m) for m in metadata_list])
    elif format_type == ExportFormat.JSON:
        return "[" + ",\n".join([m.json() for m in metadata_list]) + "]"
    else:
        raise ValueError(f"Export format {format_type} is not yet implemented.")
