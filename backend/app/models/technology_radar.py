from sqlalchemy import Column, String, Integer, Float, Date
from app.models.base import Base

class TechnologyRadar(Base):
    __tablename__ = "technology_radar"
    
    id = Column(Integer, primary_key=True, index=True)
    tech_name = Column(String(100), nullable=False)
    avg_trl_level = Column(Float, default=0.0)
    frequency_count = Column(Integer, default=0)
    snapshot_date = Column(Date, nullable=False)
