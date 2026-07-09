from pydantic import BaseModel
from typing import List, Optional, Any
from enum import Enum

class HumanizationMode(str, Enum):
    NATURAL = "natural"
    ACADEMIC = "academic"
    PROFESSIONAL = "professional"
    TECHNICAL = "technical"
    CREATIVE = "creative"

class HumanizationStrength(str, Enum):
    CONSERVATIVE = "conservative"
    BALANCED = "balanced"
    AGGRESSIVE = "aggressive"

class QualityScores(BaseModel):
    readability_score: float
    naturalness_score: float
    consistency_score: float
    preservation_score: float
    overall_quality_score: float

class DiffChunk(BaseModel):
    operation: str # "equal", "insert", "delete"
    text: str

class HumanizerRequest(BaseModel):
    text: str
    mode: HumanizationMode = HumanizationMode.NATURAL
    strength: HumanizationStrength = HumanizationStrength.BALANCED
    document_id: Optional[str] = None

class HumanizerResponse(BaseModel):
    report_id: str
    original_text: str
    humanized_text: str
    mode: HumanizationMode
    strength: HumanizationStrength
    quality_scores: QualityScores
    diff_view: List[DiffChunk]
    generation_time_ms: int
