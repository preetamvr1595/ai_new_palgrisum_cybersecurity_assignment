import difflib
from schemas.humanizer import DiffChunk

def generate_diff(original_text: str, humanized_text: str) -> list[DiffChunk]:
    """
    Generates a structured chunk-by-chunk difference view using Python's difflib.
    """
    matcher = difflib.SequenceMatcher(None, original_text.split(), humanized_text.split())
    
    chunks = []
    
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            chunks.append(DiffChunk(operation="equal", text=" ".join(original_text.split()[i1:i2])))
        elif tag == 'replace':
            chunks.append(DiffChunk(operation="delete", text=" ".join(original_text.split()[i1:i2])))
            chunks.append(DiffChunk(operation="insert", text=" ".join(humanized_text.split()[j1:j2])))
        elif tag == 'delete':
            chunks.append(DiffChunk(operation="delete", text=" ".join(original_text.split()[i1:i2])))
        elif tag == 'insert':
            chunks.append(DiffChunk(operation="insert", text=" ".join(humanized_text.split()[j1:j2])))
            
    return chunks
