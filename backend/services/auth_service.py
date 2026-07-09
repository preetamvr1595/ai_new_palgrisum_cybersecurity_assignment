from sqlalchemy.orm import Session
from datetime import datetime, timezone
import uuid
from backend.db.models.user import UserSession
from backend.core.security import create_access_token, create_refresh_token
from backend.services.audit_service import log_audit_event

def create_user_session(
    db: Session, 
    user_id: str, 
    device_info: str = None, 
    ip_address: str = None
) -> dict:
    """Create a new session, generate tokens, and log the event."""
    # Generate tokens
    access_token = create_access_token(subject=user_id)
    refresh_token = create_refresh_token(subject=user_id)
    
    # Store session in DB
    session_record = UserSession(
        user_id=uuid.UUID(user_id) if isinstance(user_id, str) else user_id,
        device_info=device_info,
        ip_address=ip_address,
        refresh_token=refresh_token
    )
    db.add(session_record)
    db.commit()
    
    # Log successful login
    log_audit_event(
        db=db,
        action_type="login_success",
        user_id=user_id,
        ip_address=ip_address,
        user_agent=device_info
    )
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }

def terminate_session(db: Session, refresh_token: str) -> bool:
    """Terminates a specific session by refresh token."""
    session_record = db.query(UserSession).filter(UserSession.refresh_token == refresh_token).first()
    if session_record:
        db.delete(session_record)
        db.commit()
        return True
    return False

def terminate_all_user_sessions(db: Session, user_id: str) -> None:
    """Terminates all sessions for a user."""
    db.query(UserSession).filter(UserSession.user_id == (uuid.UUID(user_id) if isinstance(user_id, str) else user_id)).delete()
    db.commit()
