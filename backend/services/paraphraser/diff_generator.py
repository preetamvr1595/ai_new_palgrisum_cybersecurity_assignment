import difflib
from schemas.paraphraser import ParaphraseDiffChunk

def generate_diff(original_text: str, paraphrased_text: str) -> list[ParaphraseDiffChunk]:
    """
    Generates a structured chunk-by-chunk difference view using Python's difflib.
    """
    matcher = difflib.SequenceMatcher(None, original_text.split(), paraphrased_text.split())
    
    chunks = []
    
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            chunks.append(ParaphraseDiffChunk(operation="equal", text=" ".join(original_text.split()[i1:i2])))
        elif tag == 'replace':
            chunks.append(ParaphraseDiffChunk(operation="delete", text=" ".join(original_text.split()[i1:i2])))
            chunks.append(ParaphraseDiffChunk(operation="insert", text=" ".join(paraphrased_text.split()[j1:j2])))
        elif tag == 'delete':
            chunks.append(ParaphraseDiffChunk(operation="delete", text=" ".join(original_text.split()[i1:i2])))
        elif tag == 'insert':
            chunks.append(ParaphraseDiffChunk(operation="insert", text=" ".join(paraphrased_text.split()[j1:j2])))
            
    return chunks
