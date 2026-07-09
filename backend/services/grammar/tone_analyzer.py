def analyze_tone(text: str) -> str:
    """
    Detects the overarching tone of the text.
    In a full implementation, this uses sentence embeddings or keyword density.
    """
    text_lower = text.lower()
    
    formal_markers = ["therefore", "furthermore", "thus", "moreover", "consequently"]
    conversational_markers = ["like", "you know", "super", "pretty much", "basically"]
    
    formal_score = sum(1 for w in formal_markers if w in text_lower)
    casual_score = sum(1 for w in conversational_markers if w in text_lower)
    
    if formal_score > casual_score:
        return "Formal"
    elif casual_score > formal_score:
        return "Conversational"
    else:
        return "Neutral"
