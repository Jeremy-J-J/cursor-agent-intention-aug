"""
Conversation model - stores AI agent conversation history for scenarios
"""
from sqlalchemy import Column, String, Text, DateTime, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.models.base import Base

class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(String, primary_key=True)
    scenario_id = Column(String, ForeignKey("scenarios.id"), nullable=False)
    role = Column(String, nullable=False)  # user, assistant, system
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    metadata = Column(JSON)  # Additional metadata like token usage, model used
    
    # Relationships
    scenario = relationship("Scenario", back_populates="conversations")
    
    def to_dict(self):
        """Convert conversation to dictionary"""
        return {
            "id": self.id,
            "scenario_id": self.scenario_id,
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "metadata": self.metadata
        }