from sqlalchemy import Column, String, Text, Integer, ForeignKey
from app.models.base import BaseModel

class POC(BaseModel):
    __tablename__ = "pocs"
    
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    opportunity_id = Column(String(36), nullable=True) # Just a string link for now
    status = Column(String(50), default="Planned")
