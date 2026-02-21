from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AlertBase(BaseModel):
    opportunity_id: str
    title: str
    message: str
    severity: str
    is_read: bool = False

class AlertCreate(AlertBase):
    pass

class AlertUpdate(BaseModel):
    is_read: Optional[bool] = None

class AlertResponse(AlertBase):
    id: str

    class Config:
        from_attributes = True
