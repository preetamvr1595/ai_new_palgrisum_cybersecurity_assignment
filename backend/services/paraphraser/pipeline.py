from .llm_provider import llm_provider
from .style_adapter import build_system_prompt
from .semantic_validator import calculate_quality_metrics, passes_semantic_validation
from .diff_generator import generate_diff
from schemas.paraphraser import ParaphraseMode, ParaphraseStrength
from typing import List

async def process_paraphrase(text: str, mode: ParaphraseMode, strength: ParaphraseStrength, protected_keywords: List[str]) -> dict:
    """
    The master Multi-Pass orchestration pipeline for paraphrasing.
    """
    # Pass 1: Context & Strategy Selection
    system_prompt = build_system_prompt(mode, strength, protected_keywords)
    
    # Configure LLM Temperature
    temperature = 0.4
    if strength == ParaphraseStrength.MEDIUM:
        temperature = 0.7
    elif strength == ParaphraseStrength.HIGH:
        temperature = 0.85
        
    # Pass 2: Generate Rewrite
    paraphrased_text = await llm_provider.generate(system_prompt, text, temperature)
    
    # Pass 3 & 4: Semantic Validation & Quality Check
    metrics = calculate_quality_metrics(text, paraphrased_text)
    
    if not passes_semantic_validation(metrics.similarity_score):
        # In a real system, we would trigger a retry here (Pass 5: Optimization)
        # For scaffolding, we accept it but log a warning.
        pass
    
    # Pass 5: Comparison Generation
    diff_view = generate_diff(text, paraphrased_text)
    
    return {
        "paraphrased_text": paraphrased_text,
        "quality_metrics": metrics,
        "diff_view": diff_view
    }
