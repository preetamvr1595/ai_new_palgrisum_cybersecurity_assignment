import spacy

_nlp = None
def get_nlp():
    global _nlp
    if _nlp is None:
        _nlp = spacy.load("en_core_web_sm")
    return _nlp

class ExplainabilityEngine:
    """
    Splits documents into sentences and scores each sentence to generate a localized 'Risk Map'.
    """
    def __init__(self, ensemble_model):
        self.ensemble = ensemble_model
        
    def generate_risk_map(self, document_text: str) -> dict:
        nlp = get_nlp()
        doc = nlp(document_text)
        
        sentences = [s.text for s in doc.sents if len(s.text.strip()) > 10]
        
        risk_map = []
        for sent in sentences:
            # Mock scoring for each sentence
            # In reality, the ensemble would be run on each sentence or a sliding window.
            mock_score = 0.85 if "AI" in sent else 0.1
            
            risk_map.append({
                "sentence": sent,
                "ai_probability": mock_score,
                "is_flagged": mock_score > 0.7
            })
            
        return {
            "total_sentences": len(sentences),
            "flagged_sentences": sum(1 for s in risk_map if s["is_flagged"]),
            "risk_map": risk_map
        }
