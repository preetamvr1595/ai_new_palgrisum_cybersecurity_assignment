from schemas.humanizer import HumanizationMode, HumanizationStrength

def build_system_prompt(mode: HumanizationMode, strength: HumanizationStrength) -> str:
    """
    Constructs the system prompt to guide the LLM's stylistic generation.
    """
    base_prompt = "You are an expert humanizer. Rewrite the provided text to sound more natural and less robotic. "
    
    mode_instructions = {
        HumanizationMode.NATURAL: "Use a conversational, engaging, and highly human flow.",
        HumanizationMode.ACADEMIC: "Maintain a formal tone, but eliminate predictable AI formulaic structures. Keep it scholarly.",
        HumanizationMode.PROFESSIONAL: "Write for a corporate audience. Be concise, polite, and natural.",
        HumanizationMode.TECHNICAL: "Preserve all technical jargon exactly. Focus on simplifying the sentence structures around the technical terms.",
        HumanizationMode.CREATIVE: "Use vivid, unpredictable vocabulary and varied sentence lengths to tell a story."
    }
    
    strength_instructions = {
        HumanizationStrength.CONSERVATIVE: "Make minimal changes. Focus only on removing obvious AI watermarks and repetitive phrases. Do NOT alter sentence structure drastically.",
        HumanizationStrength.BALANCED: "Re-structure paragraphs and sentences to improve flow, but ensure exact semantic parity.",
        HumanizationStrength.AGGRESSIVE: "Completely rewrite the text in a highly creative, unpredictable human style. Preserve core facts but feel free to completely change the structure."
    }
    
    prompt = base_prompt + mode_instructions[mode] + " " + strength_instructions[strength] + " CRITICAL: NEVER alter facts, dates, names, or numbers."
    return prompt
