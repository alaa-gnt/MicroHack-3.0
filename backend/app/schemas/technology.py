from pydantic import BaseModel
from typing import Optional

class TechnologyBase(BaseModel):
    name: str
    category: Optional[str] = None

class TechnologyCreate(TechnologyBase):
    pass

class TechnologyUpdate(TechnologyBase):
    name: Optional[str] = None

class TechnologyResponse(TechnologyBase):
    id: str

    class Config:
        from_attributes = True
