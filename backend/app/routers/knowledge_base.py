from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.dependencies import get_db
from app.schemas.knowledge_base import KnowledgeBase
from app.services.knowledge_base_service import KnowledgeBaseService

router = APIRouter(prefix="/knowledge-base", tags=["Knowledge Base"])

@router.get("/", response_model=List[KnowledgeBase])
def read_kb_entries(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return KnowledgeBaseService.get_entries(db, skip=skip, limit=limit)

@router.post("/consolidate/{feasibility_id}", response_model=KnowledgeBase)
def consolidate_to_kb(
    feasibility_id: str,
    db: Session = Depends(get_db)
):
    entry = KnowledgeBaseService.consolidate_to_kb(db, feasibility_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Feasibility study not found or incomplete chain")
    return entry
