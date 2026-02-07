from sqlalchemy import Column, String, Integer, Float
from app.models.base import Base

class EntityTracker(Base):
    __tablename__ = "entity_tracker"
    
    id = Column(Integer, primary_key=True, index=True)
    entity_name = Column(String(100), nullable=False)
    entity_type = Column(String(20), nullable=False) # 'Company' or 'Location'
    mention_count = Column(Integer, default=0)
    hotspot_score = Column(Float, default=0.0)
