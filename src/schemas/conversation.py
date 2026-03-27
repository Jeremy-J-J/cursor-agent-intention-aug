"""
Conversation schemas for API validation
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class ConversationBase(BaseModel):
    """Base conversation schema"""
    role: str = Field(..., description="Role (user, assistant, system)")
    content: str = Field(..., description="Message content")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class ConversationCreate(ConversationBase):
    """Schema for creating a new conversation entry"""
    id: str = Field(..., description="Unique conversation ID")
    scenario_id: str = Field(..., description="Associated scenario ID")
    
    class Config:
        from_attributes = True


class ConversationResponse(ConversationBase):
    """Schema for conversation response"""
    id: str
    scenario_id: str
    timestamp: datetime
    
    class Config:
        from_attributes = True


class ConversationListResponse(BaseModel):
    """Schema for paginated conversation list"""
    conversations: List[ConversationResponse]
    total: int
    page: int
    page_size: int
