from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class MatchType(str, Enum):
    EXACT_MATCH = "exact_match"
    NEAR_MATCH = "near_match"
    SEMANTIC_SIMILARITY = "semantic_similarity"
    PARAPHRASED_SIMILARITY = "paraphrased_similarity"

class RiskLevel(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    VERY_HIGH = "very_high"

class MatchedSource(BaseModel):
    source_url_or_id: str
    source_name: str
    matched_text: str
    similarity_percentage: float
    match_type: MatchType

class HighlightedSegment(BaseModel):
    text: str
    start_char: int
    end_char: int
    similarity_score: float
    risk_level: RiskLevel
    matched_source_id: str

class PlagiarismRequest(BaseModel):
    text: str
    threshold: float = 0.50 # Conservative
    document_id: Optional[str] = None

class PlagiarismReport(BaseModel):
    report_id: str
    overall_similarity_percentage: float
    risk_level: RiskLevel
    matched_sources: List[MatchedSource]
    highlighted_segments: List[HighlightedSegment]
    generation_time_ms: int
