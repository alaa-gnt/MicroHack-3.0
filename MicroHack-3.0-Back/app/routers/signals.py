from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user
from app.schemas.signal import SignalCreate, SignalUpdate, SignalResponse
from app.services.signal_service import SignalService
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[SignalResponse])
def get_signals(
    category: Optional[str] = None,
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    return SignalService.get_signals(db, category=category, skip=skip, limit=limit)

@router.get("/{signal_id}", response_model=SignalResponse)
def get_signal(signal_id: str, db: Session = Depends(get_db)):
    signal = SignalService.get_signal(db, signal_id)
    if not signal:
        raise HTTPException(status_code=404, detail="Signal not found")
    return signal
