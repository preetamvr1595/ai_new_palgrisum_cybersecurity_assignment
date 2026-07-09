from .llm_provider import llm_provider
from .style_adapter import build_system_prompt
from .validator import calculate_quality_scores
from .diff_generator import generate_diff
from schemas.humanizer import HumanizationMode, HumanizationStrength

async def process_humanization(text: str, mode: HumanizationMode, strength: HumanizationStrength) -> dict:
    """
    The master Multi-Pass orchestration pipeline.
    """
    # Pass 1: Strategy Selection
    system_prompt = build_system_prompt(mode, strength)
    
    # Configure LLM Temperature based on strength
    temperature = 0.5
    if strength == HumanizationStrength.BALANCED:
        temperature = 0.7
    elif strength == HumanizationStrength.AGGRESSIVE:
        temperature = 0.9
        
    # Pass 2: Generation
    humanized_text = await llm_provider.generate(system_prompt, text, temperature)
    
    # Pass 3: Quality Validation
    scores = calculate_quality_scores(text, humanized_text)
    
    # Pass 4: Diff Generation
    diff_view = generate_diff(text, humanized_text)
    
    return {
        "humanized_text": humanized_text,
        "quality_scores": scores,
        "diff_view": diff_view
    }
