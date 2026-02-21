from pydantic import BaseModel
from typing import Optional

class FeasibilityStudyBase(BaseModel):
    opportunity_id: str
    technical_assessment: Optional[str] = None
    required_technology_stack: Optional[str] = None
    market_analysis: Optional[str] = None
    overall_feasibility: str
    final_recommendation: str

class FeasibilityStudyCreate(FeasibilityStudyBase):
    pass

class FeasibilityStudyUpdate(BaseModel):
    technical_assessment: Optional[str] = None
    required_technology_stack: Optional[str] = None
    market_analysis: Optional[str] = None
    business_recommendation: Optional[str] = None
    regulatory_compliance: Optional[str] = None
    overall_feasibility: Optional[str] = None
    final_recommendation: Optional[str] = None

class FeasibilityStudyResponse(FeasibilityStudyBase):
    id: str

    class Config:
        from_attributes = True
