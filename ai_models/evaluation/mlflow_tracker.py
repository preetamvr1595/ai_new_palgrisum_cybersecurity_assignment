import mlflow
import os

def setup_mlflow():
    """
    Sets up the MLflow tracking URI and experiment.
    """
    mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "file:./mlruns"))
    mlflow.set_experiment("ai_detector_research")

def log_experiment(params: dict, metrics: dict, model=None, artifact_path: str = None):
    """
    Logs an experiment run to MLflow.
    """
    with mlflow.start_run():
        mlflow.log_params(params)
        mlflow.log_metrics(metrics)
        
        if artifact_path and os.path.exists(artifact_path):
            mlflow.log_artifact(artifact_path)
            
        if model:
            # Mocking sklearn log
            import mlflow.sklearn
            mlflow.sklearn.log_model(model, "model")
