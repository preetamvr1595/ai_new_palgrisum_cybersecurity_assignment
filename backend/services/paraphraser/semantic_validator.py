import textstat
from schemas.paraphraser import QualityMetrics
import random

def calculate_quality_metrics(original_text: str, paraphrased_text: str) -> QualityMetrics:
    """
    Computes objective scores comparing the original and paraphrased text.
    Uses mock cosine similarity for Semantic Similarity.
    """
    # 1. Similarity Score (Mocked: In prod, use sentence-transformers cosine similarity)
    similarity = random.uniform(0.85, 0.98)
    
    # 2. Readability
    readability = textstat.flesch_reading_ease(paraphrased_text) / 100.0
    
    # 3. Fluency Score (Mocked: Grammar check integration)
    fluency = random.uniform(0.80, 0.99)
    
    # 4. Preservation Score (Mocked: Fact-checking integration)
    preservation = random.uniform(0.95, 1.0)
    
    overall = (similarity + readability + fluency + preservation) / 4.0
    
    return QualityMetrics(
        similarity_score=round(similarity, 2),
        readability_score=round(readability, 2),
        fluency_score=round(fluency, 2),
        preservation_score=round(preservation, 2),
        quality_score=round(overall, 2)
    )

def passes_semantic_validation(similarity_score: float) -> bool:
    """
    Returns True if the similarity score meets the threshold to prevent hallucination.
    """
    return similarity_score >= 0.75
