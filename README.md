# ROS 2 Introduction to Robotics – Lab 1

## Repository Information

- **Repository:** `intro_robotics_intelligent_systems_labs`
- **Exercise:** `lab1_exercise`
- **ROS 2 Distribution:** Humble
- **Operating System:** Ubuntu 22.04
- **Simulation:** Gazebo
- **Contributor:** Eyerusalem Gebrat
- **Student ID:** UGR/9470/16

## Project Overview

This project implements a differential-drive robot using ROS 2 and Gazebo. It demonstrates robot control, sensor data processing, obstacle detection, ROS 2 topics, custom messages, services, and actions.

The robot can detect nearby obstacles, move forward, turn when an obstacle is detected, change its turning speed through a service, rotate by a requested angle, and drive a specified distance.

The final exercise combines the movement actions to make the robot complete a square path in Gazebo.

## Packages

The exercise contains four ROS 2 packages:

- **`diffdrive_bot`** – Robot model, Gazebo simulation, and control setup.
- **`lab_interfaces`** – Custom obstacle information message and drive-distance action.
- **`my_robot_interfaces`** – Robot status message, turn-speed service, and rotate action.
- **`my_robot_nodes`** – Python nodes for obstacle avoidance, rotation, and square movement.

## Requirements

- Ubuntu 22.04
- ROS 2 Humble
- Gazebo and RViz2
- `colcon` and `rosdep`

## Build Instructions

Place `lab1_exercise` inside the `src` directory of a ROS 2 workspace.

```bash
mkdir -p ~/ros2_ws/src
```

Source ROS 2 and build:

```bash
source /opt/ros/humble/setup.bash
cd ~/ros2_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
```

For every new terminal, source the environments:

```bash
source /opt/ros/humble/setup.bash
source ~/ros2_ws/install/setup.bash
```

## Running the Project

Launch the complete square movement exercise:

```bash
ros2 launch my_robot_nodes square.launch.py
```

The robot spawns in Gazebo, waits for the required action servers, and then drives four sides, rotating approximately 90 degrees after each side.

The default side length is **0.5 meters**.

To change it:

```bash
ros2 launch my_robot_nodes square.launch.py side_length:=1.0
```

## Testing

**Check active nodes and topics:**

```bash
ros2 node list
ros2 topic list
```

**Monitor robot status:**

```bash
ros2 topic echo /robot_status
```

**Change turning speed:**

```bash
ros2 service call /set_turn_speed my_robot_interfaces/srv/SetTurnSpeed "{turn_speed: 0.8}"
```

**Enable obstacle avoidance:**

```bash
ros2 service call /turn_away_enable std_srvs/srv/SetBool "{data: true}"
```

**Test rotation action:**

```bash
ros2 action send_goal /rotate my_robot_interfaces/action/Rotate "{angle: 1.57}" --feedback
```

**Test drive-distance action:**

```bash
ros2 action send_goal /drive_distance lab_interfaces/action/DriveDistance "{distance: 0.5}" --feedback
```

## Screenshots

The `screenshots` folder should contain:

- RViz2 depth image
- RViz2 point cloud
- rqt_graph while the square launch is running
- Gazebo showing the robot's square movement

## Issues Encountered

The drive-distance action initially rejected goals when odometry was not yet available. The server was adjusted to wait for odometry during execution. Robot control interference was also resolved so the square movement could run correctly.

Gazebo displayed some non-fatal sensor configuration warnings, but these did not prevent the simulation from working.

## Expected Result

The robot successfully drives four sides and rotates approximately 90 degrees after each side, completing a square path in Gazebo.

**Contributor:** Eyerusalem Gebrat  
**Student ID:** UGR/9470/16
