from pydantic import BaseModel
from datetime import date
from typing import List, Dict, Any, Optional

class MarketTrendBase(BaseModel):
    domain_name: str
    signal_count: int
    avg_urgency_score: float
    snapshot_date: date

class MarketTrendResponse(MarketTrendBase):
    id: int

    class Config:
        from_attributes = True

class TechRadarBase(BaseModel):
    tech_name: str
    avg_trl_level: float
    frequency_count: int
    snapshot_date: date

class TechRadarResponse(TechRadarBase):
    id: int

    class Config:
        from_attributes = True

class EntityTrackerBase(BaseModel):
    entity_name: str
    entity_type: str
    mention_count: int
    hotspot_score: float

class EntityTrackerResponse(EntityTrackerBase):
    id: int

    class Config:
        from_attributes = True

class FunnelMetricBase(BaseModel):
    stage: str
    entry_count: int
    conversion_rate: float
    period_start: date
    period_end: date

class FunnelMetricResponse(FunnelMetricBase):
    id: int

    class Config:
        from_attributes = True

class StrategicBenchmarkBase(BaseModel):
    sector: str
    metric_name: str
    benchmark_value: float
    unit: Optional[str] = None

class StrategicBenchmarkResponse(StrategicBenchmarkBase):
    id: int

    class Config:
        from_attributes = True

class DashboardResponse(BaseModel):
    status: str
    trends: List[MarketTrendResponse]
    tech_radar: List[TechRadarResponse]
    entities: List[EntityTrackerResponse]
    funnel: List[FunnelMetricResponse]
    benchmarks: List[StrategicBenchmarkResponse]
    metrics: Dict[str, Any]
