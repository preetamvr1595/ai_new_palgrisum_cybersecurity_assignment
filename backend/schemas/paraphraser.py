from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class ParaphraseMode(str, Enum):
    STANDARD = "standard"
    FLUENCY = "fluency"
    ACADEMIC = "academic"
    FORMAL = "formal"
    CREATIVE = "creative"
    CONCISE = "concise"
    EXPANDED = "expanded"

class ParaphraseStrength(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class QualityMetrics(BaseModel):
    similarity_score: float
    readability_score: float
    fluency_score: float
    preservation_score: float
    quality_score: float

class ParaphraseDiffChunk(BaseModel):
    operation: str # "equal", "insert", "delete"
    text: str

class ParaphraseRequest(BaseModel):
    text: str
    mode: ParaphraseMode = ParaphraseMode.STANDARD
    strength: ParaphraseStrength = ParaphraseStrength.MEDIUM
    protected_keywords: List[str] = []
    document_id: Optional[str] = None

class ParaphraseResponse(BaseModel):
    report_id: str
    original_text: str
    paraphrased_text: str
    mode: ParaphraseMode
    strength: ParaphraseStrength
    protected_keywords: List[str]
    quality_metrics: QualityMetrics
    diff_view: List[ParaphraseDiffChunk]
    generation_time_ms: int
