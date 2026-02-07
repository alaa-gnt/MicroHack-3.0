from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from app.dependencies import get_db
from app.schemas.alert_rule import AlertRuleCreate, AlertRuleResponse, AlertRuleUpdate
from app.models.alert_rule import AlertRule

router = APIRouter()

@router.post("/", response_model=AlertRuleResponse)
def create_alert_rule(rule_in: AlertRuleCreate, db: Session = Depends(get_db)):
    """
    Create a new dynamic alert rule.
    """
    db_rule = AlertRule(
        **rule_in.model_dump(),
        created_at=datetime.utcnow().isoformat()
    )
    db.add(db_rule)
    db.commit()
    db.refresh(db_rule)
    return db_rule

@router.get("/", response_model=List[AlertRuleResponse])
def get_alert_rules(db: Session = Depends(get_db)):
    """
    List all active alert rules.
    """
    return db.query(AlertRule).all()

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_alert_rule(id: str, db: Session = Depends(get_db)):
    """
    Delete an alert rule.
    """
    db_rule = db.query(AlertRule).filter(AlertRule.id == id).first()
    if not db_rule:
        raise HTTPException(status_code=404, detail="Alert rule not found")
    db.delete(db_rule)
    db.commit()
    return None
