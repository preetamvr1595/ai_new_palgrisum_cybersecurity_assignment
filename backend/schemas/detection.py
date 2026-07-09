from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class RiskCategory(str, Enum):
    VERY_LIKELY_HUMAN = "VERY_LIKELY_HUMAN"
    LIKELY_HUMAN = "LIKELY_HUMAN"
    MIXED_CONTENT = "MIXED_CONTENT"
    LIKELY_AI = "LIKELY_AI"
    VERY_LIKELY_AI = "VERY_LIKELY_AI"

class SentenceAnalysis(BaseModel):
    sentence: str
    ai_probability: float
    is_flagged: bool
    explanation_indicators: List[str] = []

class ParagraphAnalysis(BaseModel):
    paragraph_index: int
    text: str
    ai_probability: float
    risk_category: RiskCategory
    flagged_sentences: List[SentenceAnalysis]

class DetectionReport(BaseModel):
    report_id: str
    document_id: Optional[str] = None
    overall_human_score: float
    overall_ai_score: float
    overall_confidence: float
    risk_classification: RiskCategory
    paragraph_breakdown: List[ParagraphAnalysis]
    generation_time_ms: int
