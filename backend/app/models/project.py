from sqlalchemy import Column, String, Text, Integer, ForeignKey, Float
from app.models.base import BaseModel

class Project(BaseModel):
    __tablename__ = "projects"
    
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    poc_id = Column(Integer, nullable=True) # Integer link for pocs
    budget = Column(Float, nullable=True)
    status = Column(String(50), default="Active")
