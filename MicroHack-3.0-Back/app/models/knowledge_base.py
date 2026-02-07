from sqlalchemy import Column, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.models.base import Base

class KnowledgeBaseEntry(Base):
    __tablename__ = "knowledge_base_entries"
    
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    signal_id = Column(String, ForeignKey("signals.id"), nullable=False)
    opportunity_id = Column(String, ForeignKey("signal_analysis_opportunity.id"), nullable=False)
    feasibility_id = Column(String, ForeignKey("feasibility_studies.id"), nullable=False)
    
    source_name = Column(String(100), nullable=False)
    title = Column(String(500), nullable=False)
    domain = Column(String(50), nullable=False)
    summary = Column(Text)
    technical_stack = Column(Text)
    feasibility_score = Column(String(20))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    signal = relationship("Signal")
    opportunity = relationship("Opportunity")
    feasibility = relationship("FeasibilityStudy")
