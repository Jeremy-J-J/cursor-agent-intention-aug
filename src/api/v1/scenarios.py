"""
API routes for scenario management
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from src.database import get_db
from src.services.scenario_service import ScenarioService
from src.schemas.scenario import ScenarioCreate, ScenarioUpdate, ScenarioResponse, ScenarioListResponse

router = APIRouter(prefix="/api/v1/scenarios", tags=["scenarios"])


@router.post("/", response_model=ScenarioResponse, status_code=201)
async def create_scenario(
    scenario: ScenarioCreate,
    db: Session = Depends(get_db)
):
    """Create a new scenario"""
    # Check if scenario already exists
    existing = ScenarioService.get_scenario(db, scenario.id)
    if existing:
        raise HTTPException(status_code=400, detail="Scenario with this ID already exists")
    
    db_scenario = ScenarioService.create_scenario(db, scenario)
    return db_scenario


@router.get("/{scenario_id}", response_model=ScenarioResponse)
async def get_scenario(
    scenario_id: str,
    db: Session = Depends(get_db)
):
    """Get a scenario by ID"""
    db_scenario = ScenarioService.get_scenario(db, scenario_id)
    if not db_scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return db_scenario


@router.get("/", response_model=ScenarioListResponse)
async def list_scenarios(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    category: Optional[str] = Query(None, description="Filter by category"),
    search: Optional[str] = Query(None, description="Search in name and description"),
    db: Session = Depends(get_db)
):
    """Get list of scenarios with filtering and pagination"""
    scenarios, total = ScenarioService.get_scenarios(db, skip, limit, category, search)
    
    total_pages = (total + limit - 1) // limit
    
    return ScenarioListResponse(
        scenarios=scenarios,
        total=total,
        page=skip // limit + 1,
        page_size=limit,
        total_pages=total_pages
    )


@router.put("/{scenario_id}", response_model=ScenarioResponse)
async def update_scenario(
    scenario_id: str,
    scenario_update: ScenarioUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing scenario"""
    db_scenario = ScenarioService.update_scenario(db, scenario_id, scenario_update)
    if not db_scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return db_scenario


@router.delete("/{scenario_id}", status_code=204)
async def delete_scenario(
    scenario_id: str,
    db: Session = Depends(get_db)
):
    """Delete a scenario"""
    success = ScenarioService.delete_scenario(db, scenario_id)
    if not success:
        raise HTTPException(status_code=404, detail="Scenario not found")


@router.post("/import", response_model=dict)
async def import_scenarios(
    scenarios_data: List[dict],
    db: Session = Depends(get_db)
):
    """Import multiple scenarios from JSON data"""
    count = ScenarioService.import_scenarios_from_json(db, scenarios_data)
    return {"imported": count, "message": f"Successfully imported {count} scenarios"}
