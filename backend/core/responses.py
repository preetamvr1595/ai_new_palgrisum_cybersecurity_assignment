from pydantic import BaseModel, Field
from typing import Any, Optional, Generic, TypeVar
from datetime import datetime, timezone
import uuid

T = TypeVar('T')

class SuccessResponse(BaseModel, Generic[T]):
    status: str = "success"
    message: str = "Operation completed successfully"
    data: Optional[T] = None
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))

class ErrorResponse(BaseModel):
    status: str = "error"
    error_code: str
    message: str
    details: Optional[Any] = None
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
