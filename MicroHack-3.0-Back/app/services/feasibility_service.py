from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.feasibility import FeasibilityStudy
from app.schemas.feasibility import FeasibilityStudyCreate, FeasibilityStudyUpdate

class FeasibilityService:
    @staticmethod
    def get_by_id(db: Session, study_id: str) -> Optional[FeasibilityStudy]:
        return db.query(FeasibilityStudy).filter(FeasibilityStudy.id == study_id).first()

    @staticmethod
    def get_filtered(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        opportunity_id: Optional[str] = None,
        feasibility_level: Optional[str] = None,
        recommendation: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[FeasibilityStudy]:
        query = db.query(FeasibilityStudy)

        if opportunity_id:
            query = query.filter(FeasibilityStudy.opportunity_id == opportunity_id)
        if feasibility_level:
            query = query.filter(FeasibilityStudy.overall_feasibility == feasibility_level)
        if recommendation:
            query = query.filter(FeasibilityStudy.final_recommendation == recommendation)
        
        if status:
            if status == 'approved':
                query = query.filter(FeasibilityStudy.final_recommendation == 'approved')
            elif status == 'rejected':
                query = query.filter(FeasibilityStudy.final_recommendation == 'rejected')
            elif status == 'pending':
                query = query.filter(FeasibilityStudy.final_recommendation == 'needs_revision')
            elif status == 'high-feasibility':
                query = query.filter(FeasibilityStudy.overall_feasibility == 'high')

        return query.offset(skip).limit(limit).all()
