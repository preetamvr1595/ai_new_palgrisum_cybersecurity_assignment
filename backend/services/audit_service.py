from sqlalchemy.orm import Session
from typing import Optional, Dict, Any
from backend.db.models.system import AuditLog

import uuid

def log_audit_event(
    db: Session,
    action_type: str,
    user_id: Optional[str] = None,
    entity_type: Optional[str] = None,
    entity_id: Optional[str] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
    metadata_json: Optional[Dict[str, Any]] = None
) -> AuditLog:
    """Helper to log security and system events to the database."""
    # SQLite requires UUID objects, not strings
    if user_id and isinstance(user_id, str):
        user_id = uuid.UUID(user_id)
        
    log_entry = AuditLog(
        user_id=user_id,
        action_type=action_type,
        entity_type=entity_type,
        entity_id=entity_id,
        ip_address=ip_address,
        user_agent=user_agent,
        metadata_json=metadata_json
    )
    db.add(log_entry)
    db.commit()
    db.refresh(log_entry)
    return log_entry
