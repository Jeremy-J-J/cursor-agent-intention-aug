"""
Scenario model - represents an OpenSCENARIO test scenario
"""
from sqlalchemy import Column, String, Text, DateTime, Integer, JSON, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.models.base import Base

class Scenario(Base):
    __tablename__ = "scenarios"
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    category = Column(String)  # CDA, CQU, CUSTOM, DEMO
    road_scenario = Column(Text)
    scene_participants = Column(Text)
    initial_position = Column(Text)
    movement_direction = Column(Text)
    ego_intent = Column(Text)
    trigger_condition = Column(Text)
    test_intent = Column(Text)
    open_scenario_file = Column(String)
    json_metadata = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    version = Column(Integer, default=1)
    is_valid = Column(Boolean, default=True)
    validation_errors = Column(JSON)
    
    # Relationships
    participants = relationship("Participant", back_populates="scenario", cascade="all, delete-orphan")
    conversations = relationship("Conversation", back_populates="scenario", cascade="all, delete-orphan")
    
    def to_dict(self):
        """Convert scenario to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "road_scenario": self.road_scenario,
            "scene_participants": self.scene_participants,
            "initial_position": self.initial_position,
            "movement_direction": self.movement_direction,
            "ego_intent": self.ego_intent,
            "trigger_condition": self.trigger_condition,
            "test_intent": self.test_intent,
            "open_scenario_file": self.open_scenario_file,
            "json_metadata": self.json_metadata,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "version": self.version,
            "is_valid": self.is_valid,
            "validation_errors": self.validation_errors
        }