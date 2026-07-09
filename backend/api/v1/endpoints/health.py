from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from backend.db.session import get_db
from backend.core.redis import redis_client
from backend.worker import celery_app
from backend.core.responses import SuccessResponse, ErrorResponse
from typing import Union

router = APIRouter()

@router.get("", response_model=SuccessResponse[dict])
def health_check():
    """Basic health check for load balancers."""
    return SuccessResponse(data={"status": "ok"})

@router.get("/db", response_model=Union[SuccessResponse[dict], ErrorResponse])
def health_check_db(db: Session = Depends(get_db)):
    """Check database connectivity."""
    try:
        db.execute(text("SELECT 1"))
        return SuccessResponse(data={"database": "healthy"})
    except Exception as e:
        return ErrorResponse(
            error_code="DB_CONNECTION_FAILED",
            message="Database connection failed",
            details=str(e)
        )

@router.get("/cache", response_model=Union[SuccessResponse[dict], ErrorResponse])
def health_check_cache():
    """Check Redis cache connectivity."""
    if redis_client.ping():
        return SuccessResponse(data={"redis": "healthy"})
    return ErrorResponse(
        error_code="REDIS_CONNECTION_FAILED",
        message="Redis connection failed"
    )

@router.get("/queue", response_model=Union[SuccessResponse[dict], ErrorResponse])
def health_check_queue():
    """Check Celery worker status."""
    try:
        # Check if any workers are listening
        i = celery_app.control.inspect()
        active_workers = i.active()
        
        if not active_workers:
            return ErrorResponse(
                error_code="CELERY_WORKERS_UNAVAILABLE",
                message="No Celery workers are currently active"
            )
            
        return SuccessResponse(data={"celery_workers_active": len(active_workers)})
    except Exception as e:
        return ErrorResponse(
            error_code="CELERY_CONNECTION_FAILED",
            message="Failed to connect to Celery broker",
            details=str(e)
        )
