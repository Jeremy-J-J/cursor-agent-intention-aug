"""
Repository for scenario data access
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from src.models.scenario import Scenario

class ScenarioRepository:
    """Repository class for scenario operations"""
    
    @staticmethod
    def get_scenario(db: Session, scenario_id: str) -> Optional[Scenario]:
        """Get a scenario by ID"""
        return db.query(Scenario).filter(Scenario.id == scenario_id).first()
    
    @staticmethod
    def get_scenarios(db: Session, skip: int = 0, limit: int = 100) -> List[Scenario]:
        """Get list of scenarios with pagination"""
        return db.query(Scenario).offset(skip).limit(limit).all()
    
    @staticmethod
    def create_scenario(db: Session, scenario: Scenario) -> Scenario:
        """Create a new scenario"""
        db.add(scenario)
        db.commit()
        db.refresh(scenario)
        return scenario
    
    @staticmethod
    def update_scenario(db: Session, scenario_id: str, updates: dict) -> Optional[Scenario]:
        """Update an existing scenario"""
        db_scenario = ScenarioRepository.get_scenario(db, scenario_id)
        if not db_scenario:
            return None
        
        for key, value in updates.items():
            setattr(db_scenario, key, value)
        
        db.commit()
        db.refresh(db_scenario)
        return db_scenario
    
    @staticmethod
    def delete_scenario(db: Session, scenario_id: str) -> bool:
        """Delete a scenario"""
        db_scenario = ScenarioRepository.get_scenario(db, scenario_id)
        if not db_scenario:
            return False
        
        db.delete(db_scenario)
        db.commit()
        return True