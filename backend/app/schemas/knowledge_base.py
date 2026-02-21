from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
import uuid

class KnowledgeBaseBase(BaseModel):
    source_name: str
    title: str
    domain: str
    summary: Optional[str] = None
    technical_stack: Optional[str] = None
    feasibility_score: Optional[str] = None

class KnowledgeBaseCreate(KnowledgeBaseBase):
    signal_id: str
    opportunity_id: str
    feasibility_id: str

class KnowledgeBase(KnowledgeBaseBase):
    id: str
    signal_id: str
    opportunity_id: str
    feasibility_id: str
    created_at: datetime

    class Config:
        from_attributes = True
