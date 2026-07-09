import csv
from typing import Dict, Any, Tuple
import os

def extract_csv(file_path: str) -> Tuple[str, Dict[str, Any]]:
    """
    Extracts text from a CSV file.
    Returns string representation and row/column counts.
    """
    text_content = []
    row_count = 0
    col_count = 0
    
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                if row_count == 0:
                    col_count = len(row)
                text_content.append(" | ".join(row))
                row_count += 1

    metadata = {
        "file_size": os.path.getsize(file_path),
        "row_count": row_count,
        "column_count": col_count
    }

    return "\n".join(text_content), metadata
