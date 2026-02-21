from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

class OpportunityBase(BaseModel):
    signal_id: str
    primary_domain: str
    urgency_score: int
    impact_score: int
    estimated_trl: Optional[int] = None
    companies_mentioned: Optional[str] = None
    technologies_mentioned: Optional[str] = None
    locations_mentioned: Optional[str] = None

class OpportunityCreate(OpportunityBase):
    pass

class OpportunityUpdate(BaseModel):
    primary_domain: Optional[str] = None
    urgency_score: Optional[int] = None
    impact_score: Optional[int] = None
    estimated_trl: Optional[int] = None
    companies_mentioned: Optional[str] = None
    technologies_mentioned: Optional[str] = None
    locations_mentioned: Optional[str] = None

class OpportunityResponse(OpportunityBase):
    id: str

    class Config:
        from_attributes = True
