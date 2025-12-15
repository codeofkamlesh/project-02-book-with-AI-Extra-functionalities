# ROS2 Code Generator Subagent Specification

## Name
ROS2 Code Generator

## Purpose
Generate ROS2 code snippets, rclpy node skeletons, and launch files based on user specifications for the Physical AI & Humanoid Robotics book.

## Inputs
- `urdf_path`: Path to URDF file describing the robot
- `target_controller`: Name of the controller to implement (e.g., "joint_state_controller", "position_controllers/JointGroupPositionController")
- `robot_joints`: List of joint names and types for the robot
- `node_name`: Desired name for the ROS2 node
- `additional_requirements`: Any specific requirements or constraints

## Outputs
- `node_skeleton`: Complete rclpy node skeleton with proper structure
- `launch_file`: Launch file to start the node with required parameters
- `tests_spec`: Specification for unit tests for the generated code
- `documentation`: Inline documentation and comments for the code

## Constraints
- Must follow ROS2 Humble Hawksbill conventions
- Code must be compatible with rclpy
- Generated code must follow ROS2 best practices
- All parameters must be configurable via launch files
- Code must include proper error handling and logging

## Acceptance Criteria
- Generated node skeleton compiles without errors
- Launch file successfully starts the node
- Code follows ROS2 naming conventions and best practices
- Includes proper parameter declarations and handling
- Contains appropriate logging and error handling

## Example Input
```
{
  "urdf_path": "/path/to/my_robot.urdf",
  "target_controller": "position_controllers/JointGroupPositionController",
  "robot_joints": ["joint1", "joint2", "joint3"],
  "node_name": "my_robot_controller",
  "additional_requirements": ["publish joint states", "use PID control"]
}
```

## Example Output
```
{
  "node_skeleton": "Complete Python code for the ROS2 node...",
  "launch_file": "Launch file content...",
  "tests_spec": "Test specification...",
  "documentation": "Documentation content..."
}
```

## Implementation Notes
- Use Context7 MCP to validate ROS2 API calls
- Reference official ROS2 documentation for correct patterns
- Include proper imports and class structure
- Add comments explaining key implementation decisions