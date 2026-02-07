from sqlalchemy import Column, String, Text, Integer, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
import uuid

from app.models.base import Base

class Opportunity(Base):
    __tablename__ = "signal_analysis_opportunity"
    
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    signal_id = Column(String, ForeignKey("signals.id"), nullable=False)
    primary_domain = Column(String(50), nullable=False)
    urgency_score = Column(Integer, nullable=False)
    impact_score = Column(Integer, nullable=False)
    estimated_trl = Column(Integer)
    companies_mentioned = Column(Text)
    technologies_mentioned = Column(Text)
    locations_mentioned = Column(Text)
    
    # Relationships
    signal = relationship("Signal", back_populates="opportunity")
    feasibility_study = relationship("FeasibilityStudy", back_populates="opportunity", uselist=False)
