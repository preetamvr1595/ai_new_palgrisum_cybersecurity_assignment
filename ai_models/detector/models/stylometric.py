import xgboost as xgb
import numpy as np

class StylometricEngine:
    """
    Trains and predicts using stylometric features (sentence length, readability, etc).
    """
    def __init__(self):
        self.model = xgb.XGBClassifier(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            objective="multi:softprob",
            num_class=3
        )
        self.is_trained = False

    def train(self, X: np.ndarray, y: np.ndarray):
        """
        X: array of stylometric feature vectors
        y: labels [0, 1, 2]
        """
        self.model.fit(X, y)
        self.is_trained = True

    def predict_proba(self, features: np.ndarray) -> np.ndarray:
        if not self.is_trained:
            # Return mock probabilities if untrained
            return np.array([[0.5, 0.3, 0.2] for _ in range(len(features))])
        return self.model.predict_proba(features)
