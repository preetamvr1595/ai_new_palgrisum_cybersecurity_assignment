from celery import Celery
from backend.core.config import settings
import time
from backend.core.logger import logger

# Initialize Celery app
celery_app = Celery(
    "lexiforge_worker",
    broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/1",
    backend=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/2"
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

@celery_app.task(name="test_background_job")
def test_background_job(word: str) -> str:
    """Dummy task to verify Celery workers are picking up tasks."""
    logger.info(f"Worker received job to process word: {word}")
    time.sleep(2)
    logger.info(f"Worker finished processing word: {word}")
    return f"Processed: {word}"
