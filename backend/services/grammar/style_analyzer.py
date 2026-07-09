import spacy
from schemas.grammar import Suggestion, SuggestionType

_nlp = None
def get_nlp():
    global _nlp
    if _nlp is None:
        _nlp = spacy.load("en_core_web_sm")
    return _nlp

def analyze_style(text: str) -> list[Suggestion]:
    """
    Uses SpaCy to detect passive voice and wordiness.
    """
    nlp = get_nlp()
    doc = nlp(text)
    suggestions = []
    
    # Very simple mock logic for Passive Voice detection
    for sent in doc.sents:
        # Check for passive dependency tags (e.g. nsubjpass, auxpass)
        passive_tokens = [tok for tok in sent if tok.dep_ == "auxpass" or tok.dep_ == "nsubjpass"]
        
        if passive_tokens:
            start = sent.start_char
            end = sent.end_char
            suggestions.append(Suggestion(
                issue_type=SuggestionType.STYLE,
                reason="Passive voice detected. Consider rewriting in active voice for better clarity.",
                suggested_fix="", # LLM will provide the fix
                confidence_score=0.80,
                start_char=start,
                end_char=end
            ))
            
    return suggestions
