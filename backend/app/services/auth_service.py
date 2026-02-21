from typing import Optional
from sqlalchemy.orm import Session
import uuid
from datetime import datetime

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password

class AuthService:
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
        user = AuthService.get_user_by_email(db, email)
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user

    @staticmethod
    def create_user(db: Session, user_in: UserCreate) -> User:
        db_user = User(
            id=str(uuid.uuid4()),
            email=user_in.email,
            username=user_in.username,
            full_name=user_in.full_name,
            password_hash=get_password_hash(user_in.password),
            role=user_in.role,
            department=user_in.department,
            job_title=user_in.job_title,
            created_at=datetime.utcnow()
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
