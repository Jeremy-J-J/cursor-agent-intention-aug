# Ego Cut-in Scenario DSL

This directory contains a Domain-Specific Language (DSL) implementation for ego vehicle cut-in scenarios in OpenSCENARIO format.

## Overview

The implementation consists of two main files:
- `ego_cut_in_dsl.osc`: Core DSL implementation with safety features
- `ego_cut_in_scenario.osc`: Usage examples and environment setup

## Features

### Core Features
- Configurable cruise speed and initial lane position
- Three-phase execution: setup, cut-in, and stabilization
- Realistic vehicle behavior modeling

### Safety Features
- Minimum safe distance enforcement
- Maximum speed difference limits
- Collision detection and prevention
- Safe distance maintenance between vehicles

### Environment Controls
- Weather condition variations (clear, light rain, heavy rain)
- Road friction coefficient adjustment
- Visibility requirements
- Minimum lane requirements

### Success/Failure Criteria
- Explicit success criteria verification
- Comprehensive failure condition monitoring
- Continuous safety constraint checking

## Usage

### Basic Usage
To run the basic ego cut-in scenario:
```openscenario
import ego_cut_in_dsl.osc

scenario top:
    path: Path
    path.set_map("Town04")
    path.path_min_driving_lanes(3)
    
    do serial():
        sut.ego_cut_in()  # Uses default parameters
```

### Weather Variations
Example of running with different weather conditions:
```openscenario
# Clear weather (default)
sut.ego_cut_in(
    weather_condition: "clear",
    road_friction: 1.0
)

# Light rain
sut.ego_cut_in(
    weather_condition: "light_rain",
    road_friction: 0.7,
    requested_cruise_speed: 70kph  # Reduced speed for safety
)
```

### Safety Parameters
Adjusting safety parameters:
```openscenario
sut.ego_cut_in(
    min_safe_distance: 25m,  # Increased safety distance
    max_cut_in_speed_delta: 10kph,  # More conservative speed difference
    requested_cruise_speed: 75kph
)
```

## Parameters

### Required Parameters
- `path`: Global path variable (must be defined in top-level scenario)

### Optional Parameters
- `requested_cruise_speed` (default: 80kph)
- `ego_initial_lane` (default: 1)
- `min_safe_distance` (default: 20m)
- `max_cut_in_speed_delta` (default: 15kph)
- `weather_condition` (default: "clear")
- `road_friction` (default: 1.0)

## Success Criteria
The scenario is considered successful when:
1. Ego vehicle completes lane change
2. Safe distances are maintained throughout
3. Speed differences remain within limits
4. No collisions occur
5. All safety constraints are satisfied

## Failure Conditions
The scenario fails if:
1. Any collision occurs
2. Safe distance violations
3. Speed difference violations
4. Environmental conditions become unsafe

## Examples
See `ego_cut_in_scenario.osc` for complete examples including:
- Basic scenario execution
- Weather variation handling
- Parameter customization
- Safety constraint demonstrations

## Dependencies
- `basic.osc`: Basic OpenSCENARIO definitions
- Town04 map (for multi-lane road support)

## Notes
- Ensure minimum 3 lanes are available in the selected map
- Adjust safety parameters based on weather conditions
- Monitor success/failure criteria during execution