from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config

from backend.db.session import get_db
from backend.repository.user_repo import user_repo, UserCreate
from backend.core.config import settings
from backend.services.auth_service import create_user_session
from backend.services.audit_service import log_audit_event
from backend.core.security import get_password_hash
import uuid

router = APIRouter()

# Setup Authlib OAuth
# In a real app, you might use a .env file. We map our settings directly.
starlette_config = Config(environ={
    "GOOGLE_CLIENT_ID": settings.GOOGLE_CLIENT_ID,
    "GOOGLE_CLIENT_SECRET": settings.GOOGLE_CLIENT_SECRET,
    "GITHUB_CLIENT_ID": settings.GITHUB_CLIENT_ID,
    "GITHUB_CLIENT_SECRET": settings.GITHUB_CLIENT_SECRET,
})

oauth = OAuth(starlette_config)

# Register Google
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

# Register GitHub
oauth.register(
    name='github',
    api_base_url='https://api.github.com/',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
    client_kwargs={'scope': 'user:email'},
)


@router.get("/login/{provider}")
async def login_oauth(provider: str, request: Request):
    client = oauth.create_client(provider)
    if not client:
        raise HTTPException(status_code=404, detail=f"Provider {provider} not supported")
        
    redirect_uri = request.url_for('auth_callback', provider=provider)
    return await client.authorize_redirect(request, redirect_uri)


@router.get("/callback/{provider}")
async def auth_callback(provider: str, request: Request, response: Response, db: Session = Depends(get_db)):
    client = oauth.create_client(provider)
    if not client:
        raise HTTPException(status_code=404, detail="Provider not found")
        
    try:
        token = await client.authorize_access_token(request)
        if provider == 'google':
            user_info = token.get('userinfo')
            email = user_info.get('email')
            name = user_info.get('name')
        elif provider == 'github':
            resp = await client.get('user', token=token)
            profile = resp.json()
            # Fetch emails because primary email might not be in profile
            emails_resp = await client.get('user/emails', token=token)
            emails = emails_resp.json()
            primary_email = next(e['email'] for e in emails if e['primary'])
            email = primary_email
            name = profile.get('name') or profile.get('login')
    except Exception as e:
        raise HTTPException(status_code=400, detail="OAuth Authentication Failed")

    # Sync User
    user = user_repo.get_by_email(db, email=email)
    if not user:
        # Create a new user automatically
        new_user_data = UserCreate(
            email=email,
            username=email.split('@')[0] + "_" + str(uuid.uuid4())[:4],
            full_name=name,
            password=get_password_hash(str(uuid.uuid4())) # Random password, they use OAuth
        )
        user = user_repo.create(db, obj_in=new_user_data)
        log_audit_event(db, action_type=f"register_oauth_{provider}", user_id=str(user.id), ip_address=request.client.host)

    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    # Issue Tokens
    session_data = create_user_session(
        db=db, 
        user_id=str(user.id), 
        device_info=request.headers.get("User-Agent"), 
        ip_address=request.client.host
    )
    
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
    
    log_audit_event(db, action_type=f"login_oauth_{provider}", user_id=str(user.id), ip_address=request.client.host)
    return {"message": f"Successfully logged in via {provider}"}
