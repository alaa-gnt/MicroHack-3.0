from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from decimal import Decimal

from app.models.opportunity import Opportunity
from app.services.alert_service import AlertService
from app.schemas.opportunity import OpportunityCreate, OpportunityUpdate

class OpportunityService:
    @staticmethod
    def get_opportunity(db: Session, opportunity_id: str) -> Optional[Opportunity]:
        return db.query(Opportunity).filter(Opportunity.id == opportunity_id).first()

    @staticmethod
    def create_opportunity(db: Session, opportunity: OpportunityCreate) -> Opportunity:
        db_opportunity = Opportunity(**opportunity.dict())
        db.add(db_opportunity)
        db.commit()
        db.refresh(db_opportunity)
        
        # Trigger alert if critical
        AlertService.check_and_trigger_critical_alert(db, db_opportunity)
        
        return db_opportunity

    @staticmethod
    def update_opportunity(db: Session, opportunity_id: str, opportunity: OpportunityUpdate) -> Optional[Opportunity]:
        db_opportunity = db.query(Opportunity).filter(Opportunity.id == opportunity_id).first()
        if db_opportunity:
            for key, value in opportunity.dict(exclude_unset=True).items():
                setattr(db_opportunity, key, value)
            db.commit()
            db.refresh(db_opportunity)
            
            # Trigger alert if critical
            AlertService.check_and_trigger_critical_alert(db, db_opportunity)
            
        return db_opportunity

    @staticmethod
    def get_filtered(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        signal_id: Optional[str] = None,
        domain: Optional[str] = None,
        min_urgency: Optional[float] = None,
        max_urgency: Optional[float] = None,
        min_impact: Optional[float] = None,
        max_impact: Optional[float] = None,
        trl_level: Optional[int] = None,
        high_priority: Optional[bool] = False,
        company: Optional[str] = None,
        tech: Optional[str] = None,
        location: Optional[str] = None
    ) -> List[Opportunity]:
        query = db.query(Opportunity)

        if signal_id:
            query = query.filter(Opportunity.signal_id == signal_id)
        if domain:
            query = query.filter(Opportunity.primary_domain == domain)
        if min_urgency is not None:
            query = query.filter(Opportunity.urgency_score >= min_urgency)
        if max_urgency is not None:
            query = query.filter(Opportunity.urgency_score <= max_urgency)
        if min_impact is not None:
            query = query.filter(Opportunity.impact_score >= min_impact)
        if max_impact is not None:
            query = query.filter(Opportunity.impact_score <= max_impact)
        if trl_level is not None:
            query = query.filter(Opportunity.estimated_trl == trl_level)
        if high_priority:
            query = query.filter((Opportunity.urgency_score + Opportunity.impact_score) >= 15.0)
        if company:
            query = query.filter(Opportunity.companies_mentioned.ilike(f"%{company}%"))
        if tech:
            query = query.filter(Opportunity.technologies_mentioned.ilike(f"%{tech}%"))
        if location:
            query = query.filter(Opportunity.locations_mentioned.ilike(f"%{location}%"))

        return query.offset(skip).limit(limit).all()
