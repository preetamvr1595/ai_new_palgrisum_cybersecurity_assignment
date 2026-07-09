from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.sessions import SessionMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from backend.core.config import settings
from backend.core.security_headers import SecurityHeadersMiddleware
from backend.middleware.logging import RequestLoggingMiddleware
from backend.core.exceptions import add_exception_handlers
from backend.api.v1.endpoints import auth, oauth, health, documents, detect, humanize, paraphrase, grammar, plagiarism, citation, research

from backend.services.detector.inference import inference_engine

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

from backend.db.session import engine
from backend.db.base_class import Base

@app.on_event("startup")
async def startup_event():
    # Initialize SQLite database
    Base.metadata.create_all(bind=engine)
    # Warm up models on application startup
    await inference_engine.load_models()

# 1. Add Custom Exception Handlers
add_exception_handlers(app)

# 2. Add Middlewares (Order matters: outermost first)
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Authlib requires session middleware
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to the frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Initialize Prometheus Metrics
Instrumentator().instrument(app).expose(app)

# 4. Include Routers
app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(oauth.router, prefix=f"{settings.API_V1_STR}/oauth", tags=["oauth"])
app.include_router(documents.router, prefix=f"{settings.API_V1_STR}/documents", tags=["documents"])
app.include_router(detect.router, prefix=f"{settings.API_V1_STR}/detect", tags=["detect"])
app.include_router(humanize.router, prefix=f"{settings.API_V1_STR}/humanize", tags=["humanize"])
app.include_router(paraphrase.router, prefix=f"{settings.API_V1_STR}/paraphrase", tags=["paraphrase"])
app.include_router(grammar.router, prefix=f"{settings.API_V1_STR}/grammar", tags=["grammar"])
app.include_router(plagiarism.router, prefix=f"{settings.API_V1_STR}/plagiarism", tags=["plagiarism"])
app.include_router(citation.router, prefix=f"{settings.API_V1_STR}/citation", tags=["citation"])
app.include_router(research.router, prefix=f"{settings.API_V1_STR}/research", tags=["research"])

@app.get("/")
def read_root():
    return {"message": f"Welcome to the {settings.PROJECT_NAME} API"}
