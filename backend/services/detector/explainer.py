import spacy
from .inference import inference_engine
from .aggregator import calculate_risk_category
from schemas.detection import ParagraphAnalysis, SentenceAnalysis

_nlp = None
def get_nlp():
    global _nlp
    if _nlp is None:
        _nlp = spacy.load("en_core_web_sm")
    return _nlp

def explain_text(document_text: str) -> list:
    """
    Splits document into paragraphs and sentences, scoring each.
    """
    nlp = get_nlp()
    # Split by double newline to approximate paragraphs
    raw_paragraphs = [p.strip() for p in document_text.split("\n\n") if len(p.strip()) > 10]
    
    paragraph_analyses = []
    
    for idx, para_text in enumerate(raw_paragraphs):
        doc = nlp(para_text)
        sentences = [s.text for s in doc.sents if len(s.text.strip()) > 5]
        
        sent_analyses = []
        para_ai_scores = []
        
        for sent in sentences:
            score = inference_engine.predict_chunk(sent)
            para_ai_scores.append(score)
            
            is_flagged = score > 0.65
            indicators = ["High burstiness", "Predictable syntax"] if is_flagged else []
            
            sent_analyses.append(SentenceAnalysis(
                sentence=sent,
                ai_probability=score,
                is_flagged=is_flagged,
                explanation_indicators=indicators
            ))
            
        para_score = sum(para_ai_scores) / len(para_ai_scores) if para_ai_scores else 0.0
        
        paragraph_analyses.append(ParagraphAnalysis(
            paragraph_index=idx,
            text=para_text,
            ai_probability=para_score,
            risk_category=calculate_risk_category(para_score),
            flagged_sentences=[s for s in sent_analyses if s.is_flagged]
        ))
        
    return paragraph_analyses
