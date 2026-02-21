from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user
from app.schemas.feasibility import FeasibilityStudyResponse
from app.services.feasibility_service import FeasibilityService
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[FeasibilityStudyResponse])
def get_feasibility_studies(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    opportunity_id: Optional[str] = None,
    feasibility_level: Optional[str] = None,
    recommendation: Optional[str] = None,
    status: Optional[str] = Query(None, description="One of: approved, rejected, pending, high-feasibility"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get feasibility studies with optional filters.
    """
    return FeasibilityService.get_filtered(
        db, skip=skip, limit=limit,
        opportunity_id=opportunity_id,
        feasibility_level=feasibility_level,
        recommendation=recommendation,
        status=status
    )

@router.get("/{id}", response_model=FeasibilityStudyResponse)
def get_feasibility_study(id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    study = FeasibilityService.get_by_id(db, id)
    if not study:
        raise HTTPException(status_code=404, detail="Feasibility Study not found")
    return study
