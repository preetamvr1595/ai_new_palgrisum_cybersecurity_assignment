from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class CorrectionMode(str, Enum):
    GRAMMAR_ONLY = "grammar_only"
    GRAMMAR_STYLE = "grammar_style"
    FULL_ENHANCEMENT = "full_enhancement"

class WritingMode(str, Enum):
    ACADEMIC = "academic"
    BUSINESS = "business"
    TECHNICAL = "technical"
    CREATIVE = "creative"

class SuggestionType(str, Enum):
    GRAMMAR = "grammar"
    SPELLING = "spelling"
    PUNCTUATION = "punctuation"
    STYLE = "style"
    TONE = "tone"
    VOCABULARY = "vocabulary"

class Suggestion(BaseModel):
    issue_type: SuggestionType
    reason: str
    suggested_fix: str
    confidence_score: float
    start_char: int
    end_char: int

class WritingQualityScores(BaseModel):
    grammar_score: float
    style_score: float
    readability_score: float
    clarity_score: float
    overall_writing_score: float

class GrammarRequest(BaseModel):
    text: str
    correction_mode: CorrectionMode = CorrectionMode.FULL_ENHANCEMENT
    writing_mode: WritingMode = WritingMode.BUSINESS
    document_id: Optional[str] = None

class GrammarResponse(BaseModel):
    report_id: str
    original_text: str
    corrected_text: str
    detected_tone: str
    scores: WritingQualityScores
    suggestions: List[Suggestion]
    generation_time_ms: int
