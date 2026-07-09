import xgboost as xgb
import numpy as np
from .calibration import CalibrationLayer

class DetectorEnsemble:
    """
    The Meta-classifier that combines outputs from:
    1. Transformer (DeBERTa)
    2. Stylometric Engine
    3. Statistical Engine
    """
    def __init__(self):
        self.meta_model = xgb.XGBClassifier(
            n_estimators=50,
            learning_rate=0.05,
            max_depth=3,
            objective="multi:softprob",
            num_class=3
        )
        self.calibrator = None

    def _stack_features(self, transformer_probs, stylo_probs, stat_probs) -> np.ndarray:
        """
        Stacks the probabilities from base models into a meta-feature vector.
        """
        return np.column_stack((transformer_probs, stylo_probs, stat_probs))

    def train_meta(self, transformer_probs, stylo_probs, stat_probs, y_true):
        X_meta = self._stack_features(transformer_probs, stylo_probs, stat_probs)
        self.meta_model.fit(X_meta, y_true)
        
        # Initialize calibration layer
        self.calibrator = CalibrationLayer(self.meta_model)

    def calibrate(self, transformer_probs_val, stylo_probs_val, stat_probs_val, y_val):
        """
        Calibrates the trained meta-model on a validation set.
        """
        X_meta_val = self._stack_features(transformer_probs_val, stylo_probs_val, stat_probs_val)
        self.calibrator.calibrate(X_meta_val, y_val)

    def predict(self, transformer_probs, stylo_probs, stat_probs) -> dict:
        """
        Returns final probabilities, calibrated confidence, and raw score breakdown.
        """
        X_meta = self._stack_features(transformer_probs, stylo_probs, stat_probs)
        
        if self.calibrator and self.calibrator.is_calibrated:
            final_probs = self.calibrator.predict_proba(X_meta)
        else:
            final_probs = self.meta_model.predict_proba(X_meta)
            
        # 0=HUMAN, 1=AI, 2=MIXED
        class_idx = np.argmax(final_probs[0])
        confidence = final_probs[0][class_idx]
        
        return {
            "prediction": class_idx,
            "confidence": float(confidence),
            "probabilities": final_probs[0].tolist(),
            "explanation_data": {
                "transformer_score": transformer_probs[0].tolist(),
                "stylometric_score": stylo_probs[0].tolist(),
                "statistical_score": stat_probs[0].tolist()
            }
        }
