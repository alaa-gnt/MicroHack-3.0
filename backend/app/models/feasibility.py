from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.orm import relationship
import uuid

from app.models.base import Base

class FeasibilityStudy(Base):
    __tablename__ = "feasibility_studies"
    
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    opportunity_id = Column(String, ForeignKey("signal_analysis_opportunity.id"), nullable=False)
    technical_assessment = Column(Text)
    required_technology_stack = Column(Text)
    market_analysis = Column(Text)
    overall_feasibility = Column(String(20), nullable=False)
    final_recommendation = Column(String(20), nullable=False)
    
    # Relationships
    opportunity = relationship("Opportunity", back_populates="feasibility_study")
