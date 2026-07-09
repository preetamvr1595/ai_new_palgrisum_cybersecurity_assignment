from schemas.detection import RiskCategory
import numpy as np

def calculate_risk_category(ai_score: float) -> RiskCategory:
    """
    Maps an AI probability score to a Risk Category.
    """
    if ai_score >= 0.85:
        return RiskCategory.VERY_LIKELY_AI
    elif ai_score >= 0.65:
        return RiskCategory.LIKELY_AI
    elif ai_score >= 0.40:
        return RiskCategory.MIXED_CONTENT
    elif ai_score >= 0.20:
        return RiskCategory.LIKELY_HUMAN
    else:
        return RiskCategory.VERY_LIKELY_HUMAN

def aggregate_scores(paragraph_scores: list) -> dict:
    """
    Aggregates paragraph-level scores into a final document score.
    """
    if not paragraph_scores:
        return {"overall_ai_score": 0.0, "overall_human_score": 1.0, "overall_confidence": 0.0}

    # Weight paragraphs by length or just average them. We'll use simple average for now.
    avg_ai_score = float(np.mean(paragraph_scores))
    human_score = 1.0 - avg_ai_score
    
    # Mock confidence: higher if variance is low or if score is near extremes
    variance = float(np.var(paragraph_scores))
    confidence = max(0.5, 1.0 - variance)

    return {
        "overall_ai_score": avg_ai_score,
        "overall_human_score": human_score,
        "overall_confidence": confidence
    }
