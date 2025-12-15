# Gazebo Scene Creator Subagent Specification

## Name
Gazebo Scene Creator

## Purpose
Generate Gazebo world files and SDF models for humanoid robotics simulation scenes based on user specifications for the Physical AI & Humanoid Robotics book.

## Inputs
- `robot_model_path`: Path to the robot URDF/SDF model
- `environment_type`: Type of environment (e.g., "indoor", "outdoor", "warehouse", "home")
- `objects`: List of additional objects to include in the scene
- `lighting_conditions`: Lighting setup (e.g., "bright", "dim", "natural", "artificial")
- `physics_properties`: Physics parameters for the simulation
- `scene_name`: Desired name for the scene

## Outputs
- `world_file`: Complete Gazebo world file with robot and environment
- `sdf_models`: SDF model definitions for custom objects
- `config_file`: Configuration file for the world
- `documentation`: Explanation of the scene setup and parameters

## Constraints
- Must follow Gazebo Harmonic conventions
- Models must be compatible with ROS2 Gazebo integration
- Physics parameters must be realistic for humanoid robotics
- Scene must be suitable for the specified environment type
- All models must be properly referenced and positioned

## Acceptance Criteria
- Generated world file loads successfully in Gazebo
- Robot model appears correctly in the scene
- Physics simulation behaves as expected
- Scene matches the specified environment type
- All objects are properly positioned and configured

## Example Input
```
{
  "robot_model_path": "/models/my_robot.urdf",
  "environment_type": "indoor",
  "objects": ["table", "chair", "shelf"],
  "lighting_conditions": "bright",
  "physics_properties": {"gravity": -9.81, "real_time_factor": 1.0},
  "scene_name": "indoor_robotics_lab"
}
```

## Example Output
```
{
  "world_file": "Complete SDF world file content...",
  "sdf_models": "SDF model definitions...",
  "config_file": "Configuration file content...",
  "documentation": "Documentation content..."
}
```

## Implementation Notes
- Use proper SDF format version compatible with Gazebo Harmonic
- Include appropriate lighting and camera configurations
- Set realistic physics parameters for humanoid robots
- Ensure collision and visual properties are properly defined
- Include appropriate materials and textures for the environment