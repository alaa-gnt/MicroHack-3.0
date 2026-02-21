from sqlalchemy import Column, String, Integer, Boolean, JSON
import uuid
from app.models.base import Base

class AlertRule(Base):
    __tablename__ = "alert_rules"
    
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    categories = Column(JSON, nullable=False) # List of category names
    minimum_impact_score = Column(Integer, default=0)
    minimum_urgency_score = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(String) # Reusing standard string date for simple schema
