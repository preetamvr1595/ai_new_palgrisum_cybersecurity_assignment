import pandas as pd
import re

def remove_duplicates(df: pd.DataFrame, text_column: str = 'text') -> pd.DataFrame:
    """
    Removes exact duplicates and standardizes spacing to catch near-duplicates.
    """
    df_cleaned = df.drop_duplicates(subset=[text_column]).copy()
    return df_cleaned

def normalize_text(text: str) -> str:
    """
    Cleans OCR noise and normalizes spaces.
    """
    text = re.sub(r'\s+', ' ', text)
    text = text.replace('\x00', '')
    return text.strip()

def clean_dataset(df: pd.DataFrame, text_column: str = 'text', min_words: int = 50) -> pd.DataFrame:
    """
    Applies normalization, removes duplicates, and filters out short texts.
    """
    df[text_column] = df[text_column].apply(normalize_text)
    df = remove_duplicates(df, text_column)
    
    # Filter by word count
    df = df[df[text_column].apply(lambda x: len(x.split()) >= min_words)]
    return df
