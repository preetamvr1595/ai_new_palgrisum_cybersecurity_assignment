import asyncio
from schemas.grammar import Suggestion, SuggestionType, WritingMode
import logging

logger = logging.getLogger(__name__)

async def generate_llm_suggestions(text: str, mode: WritingMode) -> list[Suggestion]:
    """
    Hits an LLM to generate deep contextual and structural rewrites that rule-based systems miss.
    """
    logger.info(f"Generating LLM Suggestions for mode: {mode}")
    await asyncio.sleep(0.5) # Simulate latency
    
    # Mock LLM Suggestion
    if len(text) > 50:
        return [Suggestion(
            issue_type=SuggestionType.VOCABULARY,
            reason="This paragraph is a bit wordy. Try tightening the prose.",
            suggested_fix="[Mock concise rewrite from LLM]",
            confidence_score=0.88,
            start_char=0,
            end_char=len(text)
        )]
    return []
