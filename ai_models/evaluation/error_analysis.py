import pandas as pd

def get_error_samples(df: pd.DataFrame, y_true_col: str, y_pred_col: str) -> pd.DataFrame:
    """
    Filters the dataframe to return only misclassified samples.
    """
    return df[df[y_true_col] != df[y_pred_col]].copy()

def analyze_errors(df: pd.DataFrame, y_true_col: str, y_pred_col: str):
    """
    Generates summary statistics of errors (e.g., False Positives vs False Negatives).
    """
    errors = get_error_samples(df, y_true_col, y_pred_col)
    
    # 0 = Human, 1 = AI, 2 = Mixed
    false_positives = errors[(errors[y_true_col] == 0) & (errors[y_pred_col] == 1)]
    false_negatives = errors[(errors[y_true_col] == 1) & (errors[y_pred_col] == 0)]
    
    return {
        "total_errors": len(errors),
        "human_marked_ai": len(false_positives),
        "ai_marked_human": len(false_negatives)
    }
