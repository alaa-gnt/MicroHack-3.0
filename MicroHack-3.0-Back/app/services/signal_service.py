from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
import uuid
from datetime import datetime

from app.models.signal import Signal
from app.models.opportunity import Opportunity
from app.schemas.signal import SignalCreate, SignalUpdate

class SignalService:
    @staticmethod
    def get_signal(db: Session, signal_id: str) -> Optional[Signal]:
        return db.query(Signal).filter(Signal.id == signal_id).first()

    @staticmethod
    def get_signals(db: Session, category: Optional[str] = None, skip: int = 0, limit: int = 100) -> List[Signal]:
        query = db.query(Signal)
        
        if category:
            # Join with Opportunity and filter by primary_domain (case-insensitive)
            query = query.join(Opportunity).filter(
                func.lower(Opportunity.primary_domain) == func.lower(category)
            )
            
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def create_signal(db: Session, signal_in: SignalCreate) -> Signal:
        db_signal = Signal(
            id=str(uuid.uuid4()),
            **signal_in.model_dump()
        )
        db.add(db_signal)
        db.commit()
        db.refresh(db_signal)
        return db_signal
