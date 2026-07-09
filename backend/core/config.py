from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Schoolarshild"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    # Database (Using SQLite for local dev)
    POSTGRES_USER: str = "user"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "schoolarshild"
    
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return "sqlite:///./schoolarshild.db"
    
    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    
    # Security & JWT
    SECRET_KEY: str = "SUPER_SECRET_KEY_PLEASE_CHANGE_IN_PRODUCTION"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    
    # OAuth (Google)
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    
    # OAuth (GitHub)
    GITHUB_CLIENT_ID: str = ""
    GITHUB_CLIENT_SECRET: str = ""
    
    # MFA
    ENABLE_MFA: bool = False
    
    class Config:
        case_sensitive = True

settings = Settings()
