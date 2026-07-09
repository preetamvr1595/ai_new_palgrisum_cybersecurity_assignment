import hashlib
import logging

logger = logging.getLogger(__name__)

def generate_ngrams(text: str, n: int = 5) -> list[str]:
    """
    Generates N-grams from the text for shingling.
    """
    words = text.lower().split()
    return [" ".join(words[i:i+n]) for i in range(len(words)-n+1)]

def get_fingerprint(text: str) -> str:
    """
    Creates a simple MD5 hash fingerprint of the text.
    In prod, MinHash/SimHash is used for near-duplicate detection.
    """
    return hashlib.md5(text.lower().encode()).hexdigest()

def find_exact_matches(text: str) -> list[dict]:
    """
    Scans the text against the 'Internal Document Index'.
    MOCK implementation for scaffolding.
    """
    logger.info("Scanning for exact N-Gram matches...")
    
    matches = []
    # Mocking a hit on an internal database document
    if "global warming" in text.lower():
        matches.append({
            "source_id": "doc_internal_8472",
            "source_name": "Climate_Report_2024.pdf",
            "matched_text": "global warming is a critical issue",
            "similarity": 1.0,
            "type": "exact_match"
        })
        
    return matches
