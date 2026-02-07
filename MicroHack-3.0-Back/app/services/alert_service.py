from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.alert import Alert
from app.models.opportunity import Opportunity
from app.schemas.alert import AlertCreate, AlertUpdate

class AlertService:
    @staticmethod
    def create_alert(db: Session, alert_in: AlertCreate) -> Alert:
        db_alert = Alert(**alert_in.model_dump())
        db.add(db_alert)
        db.commit()
        db.refresh(db_alert)
        return db_alert

    @staticmethod
    def check_and_trigger_critical_alert(db: Session, opportunity: Opportunity):
        """
        Checks against all active AlertRules and triggers alerts if criteria match.
        """
        from app.models.alert_rule import AlertRule
        
        rules = db.query(AlertRule).filter(AlertRule.is_active == True).all()
        
        for rule in rules:
            # Check if domain matches (if categories is empty, assume all)
            category_match = not rule.categories or "allCategories" in rule.categories or opportunity.primary_domain in rule.categories
            
            # Check scores
            impact_match = (opportunity.impact_score or 0) >= rule.minimum_impact_score
            urgency_match = (opportunity.urgency_score or 0) >= rule.minimum_urgency_score
            
            if category_match and impact_match and urgency_match:
                alert_in = AlertCreate(
                    opportunity_id=opportunity.id,
                    title=f"Alert: {rule.name}",
                    message=f"Opportunity in {opportunity.primary_domain} matches your rule '{rule.name}'. (Impact: {opportunity.impact_score}, Urgency: {opportunity.urgency_score})",
                    severity="High" if rule.minimum_impact_score < 8 else "Critical"
                )
                AlertService.create_alert(db, alert_in)
                # We could break here or allow multiple rules to trigger multiple alerts

    @staticmethod
    def get_alerts(db: Session, skip: int = 0, limit: int = 100) -> List[Alert]:
        return db.query(Alert).offset(skip).limit(limit).all()

    @staticmethod
    def mark_as_read(db: Session, alert_id: str) -> Optional[Alert]:
        db_alert = db.query(Alert).filter(Alert.id == alert_id).first()
        if db_alert:
            db_alert.is_read = True
            db.commit()
            db.refresh(db_alert)
        return db_alert

    @staticmethod
    def delete_alert(db: Session, alert_id: str) -> bool:
        db_alert = db.query(Alert).filter(Alert.id == alert_id).first()
        if db_alert:
            db.delete(db_alert)
            db.commit()
            return True
        return False
