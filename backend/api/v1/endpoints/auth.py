from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from sqlalchemy.orm import Session
from datetime import timedelta

from backend.db.session import get_db
from backend.repository.user_repo import user_repo, UserCreate
from backend.core.security import get_password_hash, verify_password, decode_token
from backend.core.config import settings
from backend.schemas.auth import UserRegister, UserLogin, TokenResponse, PasswordResetRequest
from backend.services.auth_service import create_user_session, terminate_session
from backend.services.audit_service import log_audit_event
from backend.api.dependencies import get_current_user
from backend.db.models.user import User

router = APIRouter()

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(user_in: UserRegister, request: Request, db: Session = Depends(get_db)):
    if user_repo.get_by_email(db, email=user_in.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    if user_repo.get_by_username(db, username=user_in.username):
        raise HTTPException(status_code=400, detail="Username already taken")
        
    # Create user
    new_user_data = UserCreate(
        email=user_in.email,
        username=user_in.username,
        full_name=user_in.full_name,
        password_hash=get_password_hash(user_in.password)
    )
    user = user_repo.create(db, obj_in=new_user_data)
    
    # Mock Email Verification Sending
    print(f"MOCK: Sending verification email to {user.email}")
    
    log_audit_event(db, action_type="register", user_id=str(user.id), ip_address=request.client.host)
    return {"message": "User registered successfully. Please verify your email."}


@router.post("/login")
def login(user_in: UserLogin, request: Request, response: Response, db: Session = Depends(get_db)):
    user = user_repo.get_by_email(db, email=user_in.email)
    
    if not user or not verify_password(user_in.password, user.password_hash):
        log_audit_event(db, action_type="login_failed", ip_address=request.client.host)
        raise HTTPException(status_code=401, detail="Incorrect email or password")
        
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    # Generate session tokens
    session_data = create_user_session(
        db=db, 
        user_id=str(user.id), 
        device_info=request.headers.get("User-Agent"), 
        ip_address=request.client.host
    )
    
    # Set HttpOnly cookies
    response.set_cookie(
        key="access_token",
        value=session_data["access_token"],
        httponly=True,
        secure=True, # Ensure HTTPS in production
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    
    response.set_cookie(
        key="refresh_token",
        value=session_data["refresh_token"],
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
    )
    
    return {"message": "Login successful"}


@router.post("/logout")
def logout(request: Request, response: Response, db: Session = Depends(get_db)):
    refresh_token = request.cookies.get("refresh_token")
    if refresh_token:
        terminate_session(db, refresh_token)
        
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"message": "Logged out successfully"}


@router.post("/refresh")
def refresh_token(request: Request, response: Response, db: Session = Depends(get_db)):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")
        
    payload = decode_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")
        
    user_id = payload.get("sub")
    
    # Generate new tokens
    session_data = create_user_session(
        db=db, 
        user_id=user_id, 
        device_info=request.headers.get("User-Agent"), 
        ip_address=request.client.host
    )
    
    # Invalidate old session
    terminate_session(db, refresh_token)
    
    # Set new cookies
    response.set_cookie(
        key="access_token",
        value=session_data["access_token"],
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    
    response.set_cookie(
        key="refresh_token",
        value=session_data["refresh_token"],
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
    )
    
    return {"message": "Token refreshed"}

@router.post("/password-reset")
def password_reset_request(reset_req: PasswordResetRequest, request: Request, db: Session = Depends(get_db)):
    user = user_repo.get_by_email(db, email=reset_req.email)
    if user:
        # Mock Email Sending
        print(f"MOCK: Sending password reset link to {user.email}")
        log_audit_event(db, action_type="password_reset_requested", user_id=str(user.id), ip_address=request.client.host)
        
    # Always return 200 to prevent email enumeration
    return {"message": "If that email exists, a reset link has been sent."}
