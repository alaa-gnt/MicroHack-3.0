from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

# Project Schemas
class ProjectBase(BaseModel):
    poc_id: str
    project_name: str = Field(..., max_length=200)
    description: Optional[str] = None
    scope: Optional[str] = None
    budget: Optional[Decimal] = None
    allocated_budget: Optional[Decimal] = None
    team_members: Optional[str] = None
    start_date: Optional[date] = None
    expected_end_date: Optional[date] = None
    actual_end_date: Optional[date] = None
    milestones: Optional[str] = None
    current_status: Optional[str] = Field(None, max_length=50, 
                                          description="Planning, In Progress, On Hold, Completed, Cancelled")
    progress_percentage: Optional[Decimal] = Field(None, ge=0, le=100)
    risks: Optional[str] = None
    issues: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    project_name: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    scope: Optional[str] = None
    budget: Optional[Decimal] = None
    allocated_budget: Optional[Decimal] = None
    team_members: Optional[str] = None
    start_date: Optional[date] = None
    expected_end_date: Optional[date] = None
    actual_end_date: Optional[date] = None
    milestones: Optional[str] = None
    current_status: Optional[str] = Field(None, max_length=50)
    progress_percentage: Optional[Decimal] = Field(None, ge=0, le=100)
    risks: Optional[str] = None
    issues: Optional[str] = None

class ProjectResponse(ProjectBase):
    id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ProjectListResponse(BaseModel):
    projects: list[ProjectResponse]
    total: int
    page: int
    page_size: int
