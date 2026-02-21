from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class AlertRuleBase(BaseModel):
    name: str
    categories: List[str]
    minimum_impact_score: int = 0
    minimum_urgency_score: int = 0
    is_active: bool = True

class AlertRuleCreate(AlertRuleBase):
    pass

class AlertRuleUpdate(BaseModel):
    name: Optional[str] = None
    categories: Optional[List[str]] = None
    minimum_impact_score: Optional[int] = None
    minimum_urgency_score: Optional[int] = None
    is_active: Optional[bool] = None

class AlertRuleResponse(AlertRuleBase):
    id: str
    created_at: Optional[str] = None

    class Config:
        from_attributes = True
