from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from app.dependencies import get_db, get_current_user
from app.schemas.blueprint import VentureBlueprintResponse
from app.services.blueprint_service import BlueprintService
from app.models.user import User

router = APIRouter()

@router.get("/{opportunity_id}", response_model=VentureBlueprintResponse)
def get_blueprint(opportunity_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = BlueprintService(db)
    blueprint = service.get_blueprint(opportunity_id)
    if not blueprint:
        raise HTTPException(status_code=404, detail="Blueprint not found. Use POST /generate to create one.")
    return blueprint

@router.post("/{opportunity_id}/generate", response_model=VentureBlueprintResponse)
def generate_blueprint(opportunity_id: str, force: bool = False, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = BlueprintService(db)
    try:
        blueprint = service.generate_blueprint(opportunity_id, force=force)
        return blueprint
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
