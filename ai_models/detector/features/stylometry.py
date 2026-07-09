import textstat
import spacy

# Load spacy model lazily
_nlp = None

def get_nlp():
    global _nlp
    if _nlp is None:
        try:
            _nlp = spacy.load("en_core_web_sm")
        except OSError:
            import spacy.cli
            spacy.cli.download("en_core_web_sm")
            _nlp = spacy.load("en_core_web_sm")
    return _nlp

def extract_stylometry(text: str) -> dict:
    """
    Extracts stylometric features from the text.
    """
    nlp = get_nlp()
    doc = nlp(text)
    
    sentences = list(doc.sents)
    num_sentences = len(sentences)
    avg_sentence_length = sum(len(s) for s in sentences) / max(num_sentences, 1)
    
    # Vocabulary diversity
    tokens = [token.text.lower() for token in doc if token.is_alpha]
    unique_tokens = set(tokens)
    lexical_richness = len(unique_tokens) / max(len(tokens), 1)
    
    # Passive voice heuristic
    passive_count = sum(1 for token in doc if token.dep_ == "auxpass")
    
    return {
        "flesch_reading_ease": textstat.flesch_reading_ease(text),
        "smog_index": textstat.smog_index(text),
        "avg_sentence_length": avg_sentence_length,
        "lexical_richness": lexical_richness,
        "passive_voice_count": passive_count
    }
