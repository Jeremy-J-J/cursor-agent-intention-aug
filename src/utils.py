"""
Utility functions for scenario processing
"""
import json
import uuid
from typing import Dict, Any, List
from datetime import datetime


def generate_id(prefix: str = "SCN") -> str:
    """Generate a unique scenario ID"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    unique_id = uuid.uuid4().hex[:8]
    return f"{prefix}_{timestamp}_{unique_id}"


def load_json_file(file_path: str) -> Dict[str, Any]:
    """Load JSON file and return as dictionary"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json_file(file_path: str, data: Dict[str, Any]) -> None:
    """Save dictionary to JSON file"""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def parse_osc_file(file_path: str) -> Dict[str, Any]:
    """Parse OpenSCENARIO file and extract metadata"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Basic parsing - extract key information
        metadata = {
            "file_path": file_path,
            "file_size": len(content),
            "parsed_at": datetime.now().isoformat()
        }
        
        # Try to extract scenario information
        if "Scenario" in content:
            metadata["has_scenario"] = True
        
        return metadata
    except Exception as e:
        return {
            "error": str(e),
            "file_path": file_path
        }


def validate_scenario_data(data: Dict[str, Any]) -> List[str]:
    """Validate scenario data and return list of errors"""
    errors = []
    
    required_fields = ["id", "name"]
    for field in required_fields:
        if field not in data or not data[field]:
            errors.append(f"Missing required field: {field}")
    
    if "category" in data and data["category"] not in ["CDA", "CQU", "CUSTOM", "DEMO"]:
        errors.append(f"Invalid category: {data['category']}")
    
    return errors


def format_scenario_summary(scenario: Dict[str, Any]) -> str:
    """Format scenario data into a human-readable summary"""
    summary = f"""
Scenario: {scenario.get('name', 'Unknown')}
ID: {scenario.get('id', 'Unknown')}
Category: {scenario.get('category', 'Unknown')}
Test Intent: {scenario.get('test_intent', 'Not specified')}
"""
    return summary.strip()
