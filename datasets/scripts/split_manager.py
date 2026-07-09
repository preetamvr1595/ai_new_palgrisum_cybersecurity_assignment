import pandas as pd
from sklearn.model_selection import train_test_split

def split_dataset(df: pd.DataFrame, test_size: float = 0.15, val_size: float = 0.15, blind_size: float = 0.05):
    """
    Splits the dataset into Training, Validation, Testing, and Blind Benchmark sets.
    """
    # 1. Separate Blind Benchmark
    main_df, blind_df = train_test_split(df, test_size=blind_size, stratify=df['label'], random_state=42)
    
    # 2. Separate Test Set
    main_df, test_df = train_test_split(main_df, test_size=test_size/(1-blind_size), stratify=main_df['label'], random_state=42)
    
    # 3. Separate Validation Set
    train_df, val_df = train_test_split(main_df, test_size=val_size/(1-blind_size-test_size), stratify=main_df['label'], random_state=42)
    
    return {
        "train": train_df,
        "val": val_df,
        "test": test_df,
        "blind": blind_df
    }
