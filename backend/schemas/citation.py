from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from enum import Enum

class CitationStyle(str, Enum):
    APA_7 = "apa_7"
    MLA_9 = "mla_9"
    IEEE = "ieee"
    CHICAGO = "chicago"
    HARVARD = "harvard"

class SourceType(str, Enum):
    BOOK = "book"
    JOURNAL_ARTICLE = "journal_article"
    WEBSITE = "website"
    CONFERENCE_PAPER = "conference_paper"

class ExportFormat(str, Enum):
    BIBTEX = "bibtex"
    RIS = "ris"
    JSON = "json"

class ReferenceMetadata(BaseModel):
    source_type: SourceType
    title: str
    authors: List[str]
    publication_year: Optional[int] = None
    publisher: Optional[str] = None
    journal_name: Optional[str] = None
    volume: Optional[str] = None
    issue: Optional[str] = None
    pages: Optional[str] = None
    doi: Optional[str] = None
    url: Optional[str] = None
    access_date: Optional[str] = None

class CitationRequest(BaseModel):
    doi: Optional[str] = None
    url: Optional[str] = None
    manual_metadata: Optional[ReferenceMetadata] = None
    style: CitationStyle = CitationStyle.APA_7

class FormattedCitation(BaseModel):
    in_text: str
    full_reference: str
    style: CitationStyle
    metadata: ReferenceMetadata

class CitationResponse(BaseModel):
    citation_id: str
    formatted: FormattedCitation
    generation_time_ms: int
