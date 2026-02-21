from sqlalchemy import Column, String, Float, Integer
from app.models.base import Base

class StrategicBenchmark(Base):
    __tablename__ = "strategic_benchmarks"
    
    id = Column(Integer, primary_key=True, index=True)
    sector = Column(String(50), nullable=False)
    metric_name = Column(String(100), nullable=False) # e.g., 'Avg ROI Period'
    benchmark_value = Column(Float, nullable=False)
    unit = Column(String(20))
