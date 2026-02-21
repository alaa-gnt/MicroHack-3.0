from typing import List, Optional
from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user
from app.schemas.pipeline import PipelineResponse, PipelineTrigger
from app.services.pipeline_service import PipelineService
from app.models.user import User

router = APIRouter()

@router.get("/overview")
def get_pipeline_overview(db: Session = Depends(get_db)):
    """
    Returns pipeline stage counts and recent projects.
    """
    return PipelineService.get_pipeline_overview(db)

@router.get("/stages/{stage_id}/projects")
def get_stage_projects(stage_id: str, db: Session = Depends(get_db)):
    """
    Returns normalized projects for a specific stage.
    """
    return PipelineService.get_stage_projects(db, stage_id)

@router.get("/status", response_model=List[PipelineResponse])
def get_pipeline_status(db: Session = Depends(get_db)):
    """
    Placeholder for pipeline status logic.
    """
    return []

@router.post("/trigger", response_model=dict)
def trigger_scraping(
    trigger_data: PipelineTrigger,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Triggers the scraping agent in the background.
    """
    background_tasks.add_task(
        PipelineService.run_scraping_pipeline,
        db=db,
        keywords=trigger_data.keywords,
        sources=trigger_data.sources
    )
    return {"message": "Scraping pipeline triggered successfully", "status": "running"}
