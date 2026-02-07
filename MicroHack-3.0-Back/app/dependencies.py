from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.database.postgres import SessionLocal
from app.core.security import ALGORITHM, SECRET_KEY
from app.models.user import User
from app.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(db: Session = Depends(get_db)) -> User:
    # 🧪 TEMPORARY TEST BYPASS
    user = db.query(User).filter(User.email == "admin@apcs.com").first()
    if not user:
        # Create a transient dummy user if not in DB
        user = User(
            id="user_001",
            email="admin@apcs.com",
            username="admin",
            full_name="Test Admin",
            role="admin"
        )
    return user
