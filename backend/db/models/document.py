import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text, Index
from sqlalchemy.types import Uuid as UUID
from sqlalchemy.orm import relationship

from backend.db.base_class import Base, SoftDeleteMixin


class Document(Base, SoftDeleteMixin):
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    title = Column(String(255), nullable=False)
    file_name = Column(String(255), nullable=True)
    file_type = Column(String(50), nullable=True)
    file_size = Column(Integer, nullable=True)
    storage_path = Column(String(1024), nullable=True)
    word_count = Column(Integer, nullable=True)
    status = Column(String(50), default="active")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    versions = relationship("DocumentVersion", back_populates="document", cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_documents_id_created_at", "id", "created_at"),
    )


class DocumentVersion(Base):
    __tablename__ = "document_versions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"), index=True, nullable=False)
    version_number = Column(Integer, nullable=False)
    content_snapshot = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    document = relationship("Document", back_populates="versions")
