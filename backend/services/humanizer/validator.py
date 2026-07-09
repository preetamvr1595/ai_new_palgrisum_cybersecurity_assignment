import textstat
from schemas.humanizer import QualityScores
import random

def calculate_quality_scores(original_text: str, humanized_text: str) -> QualityScores:
    """
    Computes objective scores comparing the original and humanized text.
    Uses textstat for readability. Other metrics are mocked heuristics for now.
    """
    # 1. Readability
    readability = textstat.flesch_reading_ease(humanized_text)
    
    # 2. Naturalness (Mocked: based on sentence length variance in a real implementation)
    naturalness = random.uniform(0.75, 0.95)
    
    # 3. Consistency/Meaning Preservation (Mocked: based on embedding similarity in prod)
    preservation = random.uniform(0.90, 0.99)
    
    # 4. Consistency (Mocked: factual checks)
    consistency = random.uniform(0.85, 0.95)
    
    overall = (readability/100 + naturalness + preservation + consistency) / 4.0
    
    return QualityScores(
        readability_score=round(readability, 2),
        naturalness_score=round(naturalness, 2),
        consistency_score=round(consistency, 2),
        preservation_score=round(preservation, 2),
        overall_quality_score=round(overall, 2)
    )
