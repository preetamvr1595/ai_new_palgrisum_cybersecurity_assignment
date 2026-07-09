from enum import Enum

class ThresholdMode(Enum):
    CONSERVATIVE = "conservative"
    BALANCED = "balanced"
    AGGRESSIVE = "aggressive"

class ThresholdManager:
    """
    Manages decision boundaries to minimize False Positives.
    """
    def __init__(self):
        # AI probability thresholds required to classify as AI (1)
        self.thresholds = {
            ThresholdMode.CONSERVATIVE: 0.90, # Extremely confident, favors humans
            ThresholdMode.BALANCED: 0.70,     # Balanced approach
            ThresholdMode.AGGRESSIVE: 0.50    # Favors catching all AI, risks false positives
        }

    def apply_threshold(self, ai_probability: float, mode: ThresholdMode = ThresholdMode.BALANCED) -> int:
        """
        Returns 1 (AI) if probability exceeds threshold, else 0 (Human)
        """
        threshold = self.thresholds.get(mode, 0.70)
        return 1 if ai_probability >= threshold else 0
