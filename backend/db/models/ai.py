import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Numeric, DateTime, ForeignKey, Integer, Text, Float
from sqlalchemy.types import Uuid as UUID
from sqlalchemy.types import JSON as JSONB
from sqlalchemy.orm import relationship

from backend.db.base_class import Base


class AIDetectionReport(Base):
    __tablename__ = "ai_detection_reports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"), index=True, nullable=False)
    ai_score = Column(Float, nullable=False)
    human_score = Column(Float, nullable=False)
    confidence_score = Column(Float, nullable=False)
    analysis_summary = Column(Text, nullable=True)
    processing_time = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    sentences = relationship("AISentenceAnalysis", back_populates="report", cascade="all, delete-orphan")


class AISentenceAnalysis(Base):
    __tablename__ = "ai_sentence_analysis"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    report_id = Column(UUID(as_uuid=True), ForeignKey("ai_detection_reports.id", ondelete="CASCADE"), index=True, nullable=False)
    sentence_text = Column(Text, nullable=False)
    ai_probability = Column(Float, nullable=False)
    classification = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    report = relationship("AIDetectionReport", back_populates="sentences")


class HumanizerJob(Base):
    __tablename__ = "humanizer_jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id", ondelete="SET NULL"), nullable=True)
    mode = Column(String(50), nullable=False)
    original_text = Column(Text, nullable=False)
    humanized_text = Column(Text, nullable=True)
    processing_time = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ParaphraseJob(Base):
    __tablename__ = "paraphrase_jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id", ondelete="SET NULL"), nullable=True)
    mode = Column(String(50), nullable=False)
    original_text = Column(Text, nullable=False)
    paraphrased_text = Column(Text, nullable=True)
    processing_time = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class GrammarReport(Base):
    __tablename__ = "grammar_reports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False)
    grammar_score = Column(Float, nullable=False)
    readability_score = Column(Float, nullable=False)
    style_score = Column(Float, nullable=False)
    issues_json = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class CitationReport(Base):
    __tablename__ = "citation_reports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    citation_style = Column(String(50), nullable=False)
    source_data = Column(JSONB, nullable=False)
    generated_citation = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ResearchSession(Base):
    __tablename__ = "research_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    topic = Column(String(255), nullable=False)
    summary = Column(Text, nullable=True)
    suggestions = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class PlagiarismReport(Base):
    __tablename__ = "plagiarism_reports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"), index=True, nullable=False)
    similarity_score = Column(Float, nullable=False)
    matched_sources_count = Column(Integer, default=0)
    report_data = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
