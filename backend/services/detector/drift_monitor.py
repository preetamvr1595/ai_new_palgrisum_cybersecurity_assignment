import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class DriftMonitor:
    """
    Monitors inference scores over time to detect dataset shift.
    """
    def __init__(self):
        self.recent_scores = []
        
    def log_prediction(self, ai_score: float):
        self.recent_scores.append({
            "score": ai_score,
            "timestamp": datetime.utcnow()
        })
        
        # Simple logging for scaffolding. In prod, push to Prometheus/Grafana.
        if len(self.recent_scores) % 100 == 0:
            avg_score = sum(s["score"] for s in self.recent_scores[-100:]) / 100
            logger.info(f"Drift Monitor - Average AI Score over last 100 requests: {avg_score:.4f}")

drift_monitor = DriftMonitor()
