from sqlalchemy import Column, String, Text, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.models.base import Base

class Signal(Base):
    __tablename__ = "signals"
    
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(500), nullable=False)
    full_content = Column(Text)
    source_url = Column(String(1000))
    source_name = Column(String(100), nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    is_processed = Column(Boolean, default=False)
    
    # Relationships
    opportunity = relationship("Opportunity", back_populates="signal", uselist=False)
