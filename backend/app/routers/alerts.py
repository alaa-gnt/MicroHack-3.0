from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user
from app.schemas.alert import AlertResponse, AlertUpdate
from app.services.alert_service import AlertService
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[AlertResponse])
def get_alerts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), ):
    """
    Retrieve all alerts for the admin/user.
    """
    return AlertService.get_alerts(db, skip=skip, limit=limit)

@router.patch("/{id}/read", response_model=AlertResponse)
def mark_alert_as_read(id: str, db: Session = Depends(get_db), ):
    """
    Mark a specific alert as read.
    """
    alert = AlertService.mark_as_read(db, id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_alert(id: str, db: Session = Depends(get_db), ):
    """
    Permanently dismiss an alert.
    """
    if not AlertService.delete_alert(db, id):
        raise HTTPException(status_code=404, detail="Alert not found")
    return None
