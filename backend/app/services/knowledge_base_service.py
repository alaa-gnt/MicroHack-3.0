from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.knowledge_base import KnowledgeBaseEntry
from app.models.signal import Signal
from app.models.opportunity import Opportunity
from app.models.feasibility import FeasibilityStudy
from app.schemas.knowledge_base import KnowledgeBaseCreate

class KnowledgeBaseService:
    @staticmethod
    def get_entries(db: Session, skip: int = 0, limit: int = 100) -> List[KnowledgeBaseEntry]:
        return db.query(KnowledgeBaseEntry).offset(skip).limit(limit).all()

    @staticmethod
    def consolidate_to_kb(db: Session, feasibility_id: str) -> Optional[KnowledgeBaseEntry]:
        # Check if already exists
        existing = db.query(KnowledgeBaseEntry).filter(KnowledgeBaseEntry.feasibility_id == feasibility_id).first()
        if existing:
            return existing

        # Fetch all related data
        feasibility = db.query(FeasibilityStudy).filter(FeasibilityStudy.id == feasibility_id).first()
        if not feasibility:
            return None
        
        opportunity = db.query(Opportunity).filter(Opportunity.id == feasibility.opportunity_id).first()
        if not opportunity:
            return None
            
        signal = db.query(Signal).filter(Signal.id == opportunity.signal_id).first()
        if not signal:
            return None

        # Create KB entry
        kb_entry = KnowledgeBaseEntry(
            signal_id=signal.id,
            opportunity_id=opportunity.id,
            feasibility_id=feasibility.id,
            source_name=signal.source_name,
            title=signal.title,
            domain=opportunity.primary_domain,
            summary=signal.full_content[:500] if signal.full_content else None, # Simplified summary
            technical_stack=feasibility.required_technology_stack or opportunity.technologies_mentioned,
            feasibility_score=feasibility.overall_feasibility
        )

        db.add(kb_entry)
        db.commit()
        db.refresh(kb_entry)
        return kb_entry
