from typing import Optional
from sqlalchemy.orm import Session
from backend.db.models.user import User
from backend.repository.base import CRUDBase
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password_hash: str
    full_name: Optional[str] = None

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password_hash: Optional[str] = None
    full_name: Optional[str] = None

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()

    def is_active(self, user: User) -> bool:
        return user.is_active

user_repo = CRUDUser(User)
