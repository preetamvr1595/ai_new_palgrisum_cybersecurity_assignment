from fastapi import Depends, HTTPException, status, Request
from fastapi.security import APIKeyCookie
from sqlalchemy.orm import Session
from jose import JWTError
from typing import List

from backend.db.session import get_db
from backend.db.models.user import User
from backend.repository.user_repo import user_repo
from backend.core.security import decode_token

# We expect the token to be in an HttpOnly cookie named 'access_token'
cookie_sec = APIKeyCookie(name="access_token", auto_error=False)

def get_current_user(
    request: Request,
    token: str = Depends(cookie_sec),
    db: Session = Depends(get_db)
) -> User:
    """Dependency to get the current authenticated user."""
    if not token:
        # Fallback to Authorization header if not in cookie (e.g. API clients)
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    payload = decode_token(token)
    if not payload or payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token subject")
        
    user = user_repo.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
        
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")
        
    return user


def require_role(allowed_roles: List[str]):
    """Dependency factory for RBAC."""
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in allowed_roles and current_user.role != "super_admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have enough privileges"
            )
        return current_user
    return role_checker
