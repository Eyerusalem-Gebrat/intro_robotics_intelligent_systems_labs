# ROS 2 Lab 1 — Differential-Drive Robot Simulation

**Course:** Introduction to Robotics and Intelligent Systems  
**Program:** BSc in Software Engineering  
**University:** Addis Ababa University  
**Academic Year:** 2026

## Contributor

**Eyerusalem Gebrat**  
**Student ID:** UGR/9470/16

## Project Overview

This project implements a differential-drive robot simulation using ROS 2 Humble and Gazebo. It demonstrates ROS 2 topics, services, custom messages, and actions through robot control, obstacle detection, obstacle avoidance, and autonomous square movement.

## Package Structure

| Package | Description |
|---|---|
| `diffdrive_bot` | Robot description, Gazebo simulation world, and sensor configuration. |
| `lab_interfaces` | Custom messages, services, and actions for robot control. |
| `my_robot_interfaces` | Additional robot-specific messages, services, and actions. |
| `my_robot_nodes` | ROS 2 nodes for obstacle detection, robot control, rotation, and square navigation. |

## Implemented Features

- Differential-drive robot simulation in Gazebo.
- Depth camera and IMU sensor integration.
- Obstacle detection and distance monitoring.
- Obstacle avoidance and robot status publishing.
- Turn-speed configuration through a ROS 2 service.
- Distance-based movement using an action server.
- Robot rotation using an action server.
- Autonomous square movement using four driving and rotation sequences.

## Requirements

- Ubuntu 22.04
- ROS 2 Humble
- Gazebo and ROS-Gazebo integration packages
- RViz2
- `colcon`
- `rosdep`

## Setup and Build

Create a ROS 2 workspace if you do not already have one:

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
```

Clone the repository:

```bash
git clone https://github.com/Eyerusalem-Gebrat/intro_robotics_intelligent_systems_labs.git
```

Install dependencies and build the workspace:

```bash
cd ~/ros2_ws
source /opt/ros/humble/setup.bash
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
```

## Running the Simulation

Launch the robot simulation and square navigation:

```bash
ros2 launch my_robot_nodes square.launch.py
```

To change the square side length:

```bash
ros2 launch my_robot_nodes square.launch.py side_length:=1.0
```

The default side length is `0.5` meters.

## Testing

Useful commands for inspecting the running ROS 2 system:

```bash
ros2 node list
ros2 topic list
ros2 topic echo /robot_status
ros2 topic echo /obstacle
```

The robot's movement can also be tested through the `/drive_distance` and `/rotate` action servers, and the `/set_turn_speed` service.

## Screenshots

The `screenshots/` directory contains:

- `rviz_depth_pointcloud.png` — RViz2 view of the depth camera and point cloud.
- `rqt_graph.png` — ROS 2 node communication graph.

## Expected Result

When launched successfully, the robot spawns in Gazebo, detects obstacles, and executes an autonomous square path using the distance and rotation action servers.
