from sqlalchemy import Column, String, Integer, Float, Date
from app.models.base import Base

class FunnelMetric(Base):
    __tablename__ = "funnel_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    stage = Column(String(20), nullable=False) # 'Signal', 'Opportunity', 'Feasibility'
    entry_count = Column(Integer, default=0)
    conversion_rate = Column(Float, default=0.0)
    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)
