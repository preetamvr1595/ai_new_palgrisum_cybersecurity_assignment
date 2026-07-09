from schemas.paraphraser import ParaphraseMode, ParaphraseStrength
from typing import List

def build_system_prompt(mode: ParaphraseMode, strength: ParaphraseStrength, protected_keywords: List[str]) -> str:
    """
    Constructs the system prompt to guide the LLM's paraphrase generation.
    """
    base_prompt = "You are an expert paraphrasing engine. Rewrite the provided text while strictly preserving facts and meaning. "
    
    mode_instructions = {
        ParaphraseMode.STANDARD: "Rewrite clearly and naturally. Improve vocabulary.",
        ParaphraseMode.FLUENCY: "Focus entirely on grammatical correctness, readability, and removing awkward phrasing.",
        ParaphraseMode.ACADEMIC: "Elevate the vocabulary to a scholarly level. Use precise terminology and formal structure.",
        ParaphraseMode.FORMAL: "Rewrite for professional business communication. Be polite, concise, and direct.",
        ParaphraseMode.CREATIVE: "Use evocative language, varied sentence structures, and an engaging tone.",
        ParaphraseMode.CONCISE: "Reduce the word count as much as possible without losing the core facts.",
        ParaphraseMode.EXPANDED: "Add context, elaborations, and descriptive vocabulary to lengthen the text while remaining factual."
    }
    
    strength_instructions = {
        ParaphraseStrength.LOW: "Make only minor vocabulary swaps. Do not restructure sentences.",
        ParaphraseStrength.MEDIUM: "Restructure sentences and swap vocabulary to improve flow.",
        ParaphraseStrength.HIGH: "Completely restructure paragraphs and sentences for a drastically different read."
    }
    
    prompt = base_prompt + mode_instructions[mode] + " " + strength_instructions[strength]
    
    if protected_keywords:
        prompt += f" CRITICAL INSTRUCTION: You MUST NOT alter, translate, or replace the following protected keywords: {', '.join(protected_keywords)}."
        
    return prompt
