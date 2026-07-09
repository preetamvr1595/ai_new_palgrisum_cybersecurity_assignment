# Import all the models, so that Base has them before being
# imported by Alembic
from backend.db.base_class import Base

from backend.db.models.user import User, UserSession, UserPreference, APIKey
from backend.db.models.subscription import Plan, Subscription, Payment
from backend.db.models.document import Document, DocumentVersion
from backend.db.models.ai import (
    AIDetectionReport, AISentenceAnalysis, HumanizerJob, ParaphraseJob,
    GrammarReport, CitationReport, ResearchSession, PlagiarismReport
)
from backend.db.models.system import UsageMetric, AuditLog, Notification, SupportTicket
