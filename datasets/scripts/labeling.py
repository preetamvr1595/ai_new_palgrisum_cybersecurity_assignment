import pandas as pd
from enum import Enum

class Label(int, Enum):
    HUMAN = 0
    AI = 1
    MIXED = 2

def assign_labels(df: pd.DataFrame, source_type: str) -> pd.DataFrame:
    """
    Assigns labels based on the source type.
    """
    if source_type == 'human':
        df['label'] = Label.HUMAN.value
    elif source_type == 'ai':
        df['label'] = Label.AI.value
    elif source_type == 'mixed':
        df['label'] = Label.MIXED.value
    else:
        raise ValueError("Unknown source_type")
        
    return df

def generate_metadata(df: pd.DataFrame, domain: str, language: str = 'en') -> pd.DataFrame:
    """
    Appends metadata columns required by the PRD.
    """
    df['domain'] = domain
    df['language'] = language
    df['word_count'] = df['text'].apply(lambda x: len(x.split()))
    return df
