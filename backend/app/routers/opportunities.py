from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from decimal import Decimal

from app.dependencies import get_db, get_current_user
from app.schemas.opportunity import OpportunityResponse
from app.services.opportunity_service import OpportunityService
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[OpportunityResponse])
def get_opportunities(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
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
    location: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get opportunities with optional filters.
    """
    return OpportunityService.get_filtered(
        db, skip=skip, limit=limit, signal_id=signal_id, domain=domain,
        min_urgency=min_urgency, max_urgency=max_urgency,
        min_impact=min_impact, max_impact=max_impact,
        trl_level=trl_level, high_priority=high_priority,
        company=company, tech=tech, location=location
    )

@router.get("/{id}", response_model=OpportunityResponse)
def get_opportunity(id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    opportunity = OpportunityService.get_opportunity(db, id)
    if not opportunity:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    return opportunity
