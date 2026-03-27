"""
Participant model - represents vehicles, pedestrians, etc. in a scenario
"""
from sqlalchemy import Column, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from src.models.base import Base

class Participant(Base):
    __tablename__ = "participants"
    
    id = Column(String, primary_key=True)
    scenario_id = Column(String, ForeignKey("scenarios.id"), nullable=False)
    name = Column(String, nullable=False)
    type = Column(String)  # EGO_VEHICLE, OTHER_VEHICLE, PEDESTRIAN, CYCLIST, etc.
    sub_type = Column(String)
    color = Column(String)
    initial_position = Column(Text)
    velocity = Column(Float)
    acceleration = Column(Float)
    dimensions = Column(Text)  # JSON string with length, width, height
    properties = Column(JSON)
    
    # Relationships
    scenario = relationship("Scenario", back_populates="participants")
    
    def to_dict(self):
        """Convert participant to dictionary"""
        return {
            "id": self.id,
            "scenario_id": self.scenario_id,
            "name": self.name,
            "type": self.type,
            "sub_type": self.sub_type,
            "color": self.color,
            "initial_position": self.initial_position,
            "velocity": self.velocity,
            "acceleration": self.acceleration,
            "dimensions": self.dimensions,
            "properties": self.properties
        }