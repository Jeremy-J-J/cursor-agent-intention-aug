"""
Scenario service - business logic for scenario management
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from src.models.scenario import Scenario
from src.schemas.scenario import ScenarioCreate, ScenarioUpdate
from src.repositories.scenario_repository import ScenarioRepository

class ScenarioService:
    """Service class for scenario operations"""
    
    @staticmethod
    def create_scenario(db: Session, scenario: ScenarioCreate) -> Scenario:
        """Create a new scenario"""
        db_scenario = Scenario(
            id=scenario.id,
            name=scenario.name,
            category=scenario.category,
            road_scenario=scenario.road_scenario,
            scene_participants=scenario.scene_participants,
            initial_position=scenario.initial_position,
            movement_direction=scenario.movement_direction,
            ego_intent=scenario.ego_intent,
            trigger_condition=scenario.trigger_condition,
            test_intent=scenario.test_intent,
            open_scenario_file=scenario.open_scenario_file,
            json_metadata=scenario.json_metadata
        )
        return ScenarioRepository.create_scenario(db, db_scenario)
    
    @staticmethod
    def get_scenario(db: Session, scenario_id: str) -> Optional[Scenario]:
        """Get a scenario by ID"""
        return ScenarioRepository.get_scenario(db, scenario_id)
    
    @staticmethod
    def get_scenarios(db: Session, skip: int = 0, limit: int = 100) -> List[Scenario]:
        """Get list of scenarios with pagination"""
        return ScenarioRepository.get_scenarios(db, skip, limit)
    
    @staticmethod
    def update_scenario(db: Session, scenario_id: str, scenario: ScenarioUpdate) -> Optional[Scenario]:
        """Update an existing scenario"""
        update_data = scenario.dict(exclude_unset=True)
        return ScenarioRepository.update_scenario(db, scenario_id, update_data)
    
    @staticmethod
    def delete_scenario(db: Session, scenario_id: str) -> bool:
        """Delete a scenario"""
        return ScenarioRepository.delete_scenario(db, scenario_id)