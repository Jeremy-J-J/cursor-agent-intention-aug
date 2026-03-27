"""
Scenario schema definitions
"""
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class ScenarioBase(BaseModel):
    id: str
    name: str
    category: Optional[str] = None
    road_scenario: Optional[str] = None
    scene_participants: Optional[str] = None
    initial_position: Optional[str] = None
    movement_direction: Optional[str] = None
    ego_intent: Optional[str] = None
    trigger_condition: Optional[str] = None
    test_intent: Optional[str] = None
    open_scenario_file: Optional[str] = None
    json_metadata: Optional[Dict[str, Any]] = None

class ScenarioCreate(ScenarioBase):
    pass

class ScenarioUpdate(ScenarioBase):
    pass

class ScenarioResponse(ScenarioBase):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    version: int = 1
    is_valid: bool = True
    validation_errors: Optional[Dict[str, Any]] = None

class ScenarioListResponse(BaseModel):
    scenarios: list
    total: int
    page: int
    page_size: int
    total_pages: int