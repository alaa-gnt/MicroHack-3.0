from pydantic import BaseModel
from typing import List, Optional

class PipelineTrigger(BaseModel):
    keywords: Optional[List[str]] = None
    sources: Optional[List[str]] = None

class PipelineResponse(BaseModel):
    id: str
    status: str

    class Config:
        from_attributes = True
