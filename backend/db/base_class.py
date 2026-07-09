from datetime import datetime, timezone
import uuid
from sqlalchemy import Column, DateTime
from sqlalchemy.orm import declarative_base

# Define the base class for all models
Base = declarative_base()

class TimestampMixin:
    """Mixin to add created_at and updated_at columns."""
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=True)

class SoftDeleteMixin:
    """Mixin to add deleted_at column for soft deletes."""
    deleted_at = Column(DateTime(timezone=True), nullable=True)
