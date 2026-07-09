import pytest
from datetime import timedelta
from backend.core.security import create_access_token, decode_token
from backend.core.config import settings

def test_create_and_decode_access_token():
    subject = "user_123"
    token = create_access_token(subject=subject)
    
    assert token is not None
    
    payload = decode_token(token)
    assert payload is not None
    assert payload.get("sub") == subject
    assert payload.get("type") == "access"
    assert "exp" in payload

def test_decode_expired_token():
    subject = "user_123"
    # Create an expired token by setting delta to negative
    token = create_access_token(subject=subject, expires_delta=timedelta(minutes=-10))
    
    payload = decode_token(token)
    assert payload is None # The decode_token function catches JWTError and returns None
