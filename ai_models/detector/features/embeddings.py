import numpy as np

def generate_embeddings(text: str) -> np.ndarray:
    """
    Mocks generation of sentence/document embeddings.
    Production implementation uses `sentence-transformers` (e.g., all-MiniLM-L6-v2).
    """
    # In production:
    # from sentence_transformers import SentenceTransformer
    # model = SentenceTransformer('all-MiniLM-L6-v2')
    # return model.encode(text)
    
    # Mocking a 384-dimensional embedding
    return np.random.rand(384)
