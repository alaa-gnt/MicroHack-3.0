from sqlalchemy import Column, String, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
import uuid

from app.models.base import Base

class VentureBlueprint(Base):
    __tablename__ = "venture_blueprints"
    
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    opportunity_id = Column(String, ForeignKey("signal_analysis_opportunity.id"), nullable=False, unique=True)
    
    # 1. Automated "Cahier de Charge" (Specs)
    system_architecture = Column(Text)
    data_schema = Column(Text)
    security_protocols = Column(Text)
    kpi_metrics = Column(Text)
    
    # 2. The "v0.dev" MVP Accelerator
    v0_prompt = Column(Text)
    
    # 3. The GitHub "Day-Zero" Repo
    github_manifest = Column(JSON) # Stores package.json, README.md, etc.
    
    # 4. Logic Flow
    mermaid_flow = Column(Text)
    
    # Relationships
    opportunity = relationship("Opportunity", back_populates="venture_blueprint")
