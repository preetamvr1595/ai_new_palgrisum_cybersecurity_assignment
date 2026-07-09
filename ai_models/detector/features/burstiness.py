import math
from collections import Counter
import numpy as np

def extract_burstiness(text: str) -> dict:
    """
    Approximates burstiness (variance of sentence lengths) and perplexity heuristics.
    In a real implementation, a small language model like GPT-2 is used to score perplexity.
    """
    sentences = [s.strip() for s in text.split('.') if s.strip()]
    lengths = [len(s.split()) for s in sentences]
    
    if not lengths:
        return {"length_variance": 0, "entropy": 0}
        
    variance = np.var(lengths)
    
    # Simple word entropy
    words = text.split()
    word_counts = Counter(words)
    total_words = len(words)
    entropy = -sum((count/total_words) * math.log2(count/total_words) for count in word_counts.values())
    
    return {
        "length_variance": variance,
        "entropy": entropy
    }
