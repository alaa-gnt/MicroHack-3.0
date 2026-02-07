from pydantic import BaseModel
from typing import Optional, Dict, Any

class VentureBlueprintBase(BaseModel):
    opportunity_id: str
    system_architecture: Optional[str] = None
    data_schema: Optional[str] = None
    security_protocols: Optional[str] = None
    kpi_metrics: Optional[str] = None
    v0_prompt: Optional[str] = None
    mermaid_flow: Optional[str] = None
    github_manifest: Optional[Dict[str, Any]] = None

class VentureBlueprintCreate(VentureBlueprintBase):
    pass

class VentureBlueprintUpdate(BaseModel):
    system_architecture: Optional[str] = None
    data_schema: Optional[str] = None
    security_protocols: Optional[str] = None
    kpi_metrics: Optional[str] = None
    v0_prompt: Optional[str] = None
    mermaid_flow: Optional[str] = None
    github_manifest: Optional[Dict[str, Any]] = None

class VentureBlueprintResponse(VentureBlueprintBase):
    id: str

    class Config:
        from_attributes = True
