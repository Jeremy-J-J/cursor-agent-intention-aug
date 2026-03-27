"""
Participant schemas for API validation
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class ParticipantBase(BaseModel):
    """Base participant schema"""
    name: str = Field(..., description="Participant name")
    type: Optional[str] = Field(None, description="Participant type (EGO_VEHICLE, OTHER_VEHICLE, etc.)")
    sub_type: Optional[str] = Field(None, description="Participant sub-type")
    color: Optional[str] = Field(None, description="Color")
    initial_position: Optional[str] = Field(None, description="Initial position")
    velocity: Optional[float] = Field(None, description="Initial velocity")
    acceleration: Optional[float] = Field(None, description="Initial acceleration")
    dimensions: Optional[str] = Field(None, description="Dimensions as JSON string")
    properties: Optional[Dict[str, Any]] = Field(None, description="Additional properties")


class ParticipantCreate(ParticipantBase):
    """Schema for creating a new participant"""
    id: str = Field(..., description="Unique participant ID")
    scenario_id: str = Field(..., description="Associated scenario ID")
    
    class Config:
        from_attributes = True


class ParticipantResponse(ParticipantBase):
    """Schema for participant response"""
    id: str
    scenario_id: str
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
