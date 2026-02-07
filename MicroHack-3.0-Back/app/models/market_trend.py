from sqlalchemy import Column, String, Integer, Float, Date
from app.models.base import Base

class MarketTrend(Base):
    __tablename__ = "market_trends"
    
    id = Column(Integer, primary_key=True, index=True)
    domain_name = Column(String(50), nullable=False)
    signal_count = Column(Integer, default=0)
    avg_urgency_score = Column(Float, default=0.0)
    snapshot_date = Column(Date, nullable=False)
