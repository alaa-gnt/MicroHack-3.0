from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date

# POC Schemas
class POCBase(BaseModel):
    feasibility_study_id: str
    poc_name: str = Field(..., max_length=200)
    objectives: Optional[str] = None
    methodology: Optional[str] = None
    resources_required: Optional[str] = None
    timeline: Optional[str] = None
    success_criteria: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    results: Optional[str] = None
    lessons_learned: Optional[str] = None
    final_status: Optional[str] = Field(None, max_length=20, description="Success, Partial, Failed")

class POCCreate(POCBase):
    pass

class POCUpdate(BaseModel):
    poc_name: Optional[str] = Field(None, max_length=200)
    objectives: Optional[str] = None
    methodology: Optional[str] = None
    resources_required: Optional[str] = None
    timeline: Optional[str] = None
    success_criteria: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    results: Optional[str] = None
    lessons_learned: Optional[str] = None
    final_status: Optional[str] = Field(None, max_length=20)

class POCResponse(POCBase):
    id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class POCListResponse(BaseModel):
    pocs: list[POCResponse]
    total: int
    page: int
    page_size: int
