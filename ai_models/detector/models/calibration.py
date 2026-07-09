from sklearn.calibration import CalibratedClassifierCV
import numpy as np

class CalibrationLayer:
    """
    Calibrates outputs from the meta-ensemble using Isotonic Regression.
    """
    def __init__(self, base_estimator):
        # CalibratedClassifierCV requires a fitted or un-fitted base estimator
        self.calibrator = CalibratedClassifierCV(base_estimator, method='isotonic', cv='prefit')
        self.is_calibrated = False

    def calibrate(self, X_val: np.ndarray, y_val: np.ndarray):
        """
        Calibrates the raw scores to actual confidence probabilities.
        """
        self.calibrator.fit(X_val, y_val)
        self.is_calibrated = True

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        if not self.is_calibrated:
            raise RuntimeError("Model must be calibrated before prediction.")
        return self.calibrator.predict_proba(X)
