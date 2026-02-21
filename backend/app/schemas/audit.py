from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Audit Schemas
class AuditBase(BaseModel):
    user_id: str
    action: str = Field(..., max_length=100, description="Created, Updated, Approved, Rejected, etc.")
    entity_type: str = Field(..., max_length=50, description="Signal, Opportunity, Feasibility, POC, Project")
    entity_id: str
    old_value: Optional[str] = None
    new_value: Optional[str] = None
    reason: Optional[str] = None

class AuditCreate(AuditBase):
    pass

class AuditResponse(AuditBase):
    id: str
    timestamp: datetime
    
    class Config:
        from_attributes = True

class AuditListResponse(BaseModel):
    audits: list[AuditResponse]
    total: int
    page: int
    page_size: int
