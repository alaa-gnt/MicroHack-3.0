from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime

class SignalBase(BaseModel):
    title: str
    full_content: Optional[str] = None
    source_url: Optional[str] = None
    source_name: str

class SignalCreate(SignalBase):
    pass

class SignalUpdate(BaseModel):
    title: Optional[str] = None
    full_content: Optional[str] = None
    source_url: Optional[str] = None
    source_name: Optional[str] = None
    is_processed: Optional[bool] = None

class OpportunityShort(BaseModel):
    id: str
    primary_domain: str
    urgency_score: int
    impact_score: int

    class Config:
        from_attributes = True

class SignalResponse(SignalBase):
    id: str
    date: datetime
    is_processed: bool
    opportunity: Optional[OpportunityShort] = None

    class Config:
        from_attributes = True
