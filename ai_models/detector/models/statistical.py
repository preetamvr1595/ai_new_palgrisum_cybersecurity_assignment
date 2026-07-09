from sklearn.ensemble import RandomForestClassifier
import numpy as np

class StatisticalEngine:
    """
    Trains and predicts using statistical/burstiness features (entropy, variance).
    """
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, max_depth=10)
        self.is_trained = False

    def train(self, X: np.ndarray, y: np.ndarray):
        """
        X: array of burstiness feature vectors
        y: labels [0, 1, 2]
        """
        self.model.fit(X, y)
        self.is_trained = True

    def predict_proba(self, features: np.ndarray) -> np.ndarray:
        if not self.is_trained:
            return np.array([[0.6, 0.2, 0.2] for _ in range(len(features))])
        return self.model.predict_proba(features)
