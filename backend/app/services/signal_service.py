from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, case
import uuid
from datetime import datetime

from app.models.signal import Signal
from app.models.opportunity import Opportunity
from app.models.feasibility import FeasibilityStudy
from app.schemas.signal import SignalCreate, SignalUpdate

class SignalService:
    @staticmethod
    def get_signal(db: Session, signal_id: str) -> Optional[Signal]:
        return db.query(Signal).filter(Signal.id == signal_id).first()

    @staticmethod
    def get_signals(db: Session, category: Optional[str] = None, skip: int = 0, limit: int = 100) -> List[Signal]:
        # outerjoin to FeasibilityStudy through Opportunity to check for existence
        query = db.query(Signal).outerjoin(Opportunity).outerjoin(FeasibilityStudy).options(
            joinedload(Signal.opportunity).joinedload(Opportunity.feasibility_study)
        )
        
        if category:
            # Filter by primary_domain (case-insensitive)
            query = query.filter(
                func.lower(Opportunity.primary_domain) == func.lower(category)
            )
        
        # Priority: 
        # 1. Opportunities with a feasibility plan first
        # 2. Most recent date second
        query = query.order_by(
            case((FeasibilityStudy.id != None, 0), else_=1),
            Signal.date.desc()
        )
            
        signals = query.offset(skip).limit(limit).all()
        
        # Populate the has_feasibility_study flag for the Pydantic schema
        for s in signals:
            s.has_feasibility_study = bool(s.opportunity and s.opportunity.feasibility_study)
            
        return signals

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
