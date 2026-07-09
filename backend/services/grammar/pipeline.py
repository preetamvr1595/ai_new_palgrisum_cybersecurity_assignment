from .grammar_analyzer import analyze_grammar
from .style_analyzer import analyze_style
from .tone_analyzer import analyze_tone
from .llm_corrector import generate_llm_suggestions
from schemas.grammar import CorrectionMode, WritingMode, WritingQualityScores
import textstat

async def process_grammar(text: str, c_mode: CorrectionMode, w_mode: WritingMode) -> dict:
    """
    Orchestrates the entire Grammar and Enhancement Pipeline.
    """
    suggestions = []
    
    # 1. Grammar Pass (Always Run)
    suggestions.extend(analyze_grammar(text))
    
    # 2. Style Pass
    if c_mode in [CorrectionMode.GRAMMAR_STYLE, CorrectionMode.FULL_ENHANCEMENT]:
        suggestions.extend(analyze_style(text))
        
    # 3. Full LLM Enhancement Pass
    if c_mode == CorrectionMode.FULL_ENHANCEMENT:
        llm_suggs = await generate_llm_suggestions(text, w_mode)
        suggestions.extend(llm_suggs)
        
    # 4. Tone Analysis
    tone = analyze_tone(text)
    
    # 5. Quality Metrics
    readability = textstat.flesch_reading_ease(text) / 100.0
    
    # Deduct points based on error count
    error_penalty = len(suggestions) * 0.05
    grammar_score = max(0.0, 1.0 - error_penalty)
    
    scores = WritingQualityScores(
        grammar_score=round(grammar_score, 2),
        style_score=0.85, # Mock
        readability_score=round(readability, 2),
        clarity_score=0.90, # Mock
        overall_writing_score=round((grammar_score + readability) / 2.0, 2)
    )
    
    # Generate mock corrected text (In reality, we apply the suggestions sequentially)
    corrected_text = text.replace("Helo", "Hello")
    
    return {
        "corrected_text": corrected_text,
        "detected_tone": tone,
        "scores": scores,
        "suggestions": suggestions
    }
