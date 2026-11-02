# ROS 2 Lab 1 — Differential-Drive Robot Simulation

**Course:** Introduction to Robotics and Intelligent Systems  
**University:** Addis Ababa University, College of Technology and Built-In Environment

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
- Obstacle avoidance using a turn-away node.
- Robot status publishing.
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

## Fresh clone and workspace setup

Run these commands in order. They create a workspace, clone the repository, and enter the lab folder.

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src

git clone https://github.com/Eyerusalem-Gebrat/intro_robotics_intelligent_systems_labs.git

cd intro_robotics_intelligent_systems_labs/lab1_exercise
```

### Make the Python scripts executable

A fresh Git clone can check out Python scripts without executable permission. If this happens, ROS 2 may report:

```text
No executable found
```

or:

```text
executable 'obstacle_detector.py' not found
```

Fix the permissions before building:

```bash
chmod +x diffdrive_bot/scripts/*.py
```

This is safe to run even if the scripts already have executable permission.

### Install dependencies

```bash
source /opt/ros/humble/setup.bash

cd ~/ros2_ws

rosdep update
rosdep install --from-paths src --ignore-src -r -y
```

### Build the workspace

Build all four packages and their dependencies:

```bash
cd ~/ros2_ws

source /opt/ros/humble/setup.bash

colcon build --symlink-install
```

If the workspace has previously been built from a different folder or the build reports stale source paths, clean the generated build folders and build again:

```bash
cd ~/ros2_ws

rm -rf build install log

source /opt/ros/humble/setup.bash

colcon build --symlink-install
```

After a successful build, source the workspace:

```bash
source ~/ros2_ws/install/setup.bash
```

**Important:** Every new terminal used for testing must source both ROS 2 and the workspace:

```bash
source /opt/ros/humble/setup.bash
source ~/ros2_ws/install/setup.bash
```

## Start the robot and simulation

For tests that use the robot, sensors, and obstacle detector, use `control.launch.py`:

```bash
cd ~/ros2_ws
source /opt/ros/humble/setup.bash
source ~/ros2_ws/install/setup.bash

ros2 launch diffdrive_bot control.launch.py
```

Keep this terminal running.

This launch starts the robot control setup, including the obstacle detector that publishes `/obstacle`. Starting Gazebo alone is not sufficient for the obstacle-avoidance test if the obstacle detector is not running.

## Test obstacle avoidance (turn_away)

Follow the terminal order below.

### Terminal 1 – start the robot

```bash
cd ~/ros2_ws
source /opt/ros/humble/setup.bash
source ~/ros2_ws/install/setup.bash

ros2 launch diffdrive_bot control.launch.py
```

Keep it running.

### Terminal 2 – start the turn-away node

Open a second terminal:

```bash
cd ~/ros2_ws
source /opt/ros/humble/setup.bash
source ~/ros2_ws/install/setup.bash

ros2 run my_robot_nodes turn_away
```

Expected startup message:

```text
Turn away node started (disabled)
```

**This is expected. The node is intentionally disabled when it starts.** It must be enabled using the `/turn_away_enable` service before it controls the robot.

### Terminal 3 – enable obstacle avoidance

Open a third terminal:

```bash
cd ~/ros2_ws
source /opt/ros/humble/setup.bash
source ~/ros2_ws/install/setup.bash

ros2 service call /turn_away_enable std_srvs/srv/SetBool "{data: true}"
```

The node is now enabled.

Expected behavior:

- The robot moves forward when no obstacle is detected.
- When an obstacle is detected as too close, the robot stops moving forward and turns away from it.
- Once it is clear of the obstacle, it continues moving forward.

### Check that obstacle messages are being published

In another sourced terminal:

```bash
ros2 topic echo /obstacle
```

You should see messages of type `lab_interfaces/msg/ObstacleInfo`, including the obstacle distance, angle, and `too_close` value.

To check the node and topic connections:

```bash
ros2 topic list
ros2 node list
ros2 topic info /obstacle
ros2 topic info /cmd_vel
```

### Disable obstacle avoidance

```bash
ros2 service call /turn_away_enable std_srvs/srv/SetBool "{data: false}"
```

The node should stop controlling the robot. Disabling it publishes a zero velocity command as specified in the exercise.

## Test turn-away parameters and service

The turn-away node uses these parameters:

- `forward_speed` – forward linear speed.
- `turn_speed` – turning angular speed.
- `max_turn_speed` – maximum permitted turning speed.

With `turn_away` running, inspect its parameters:

```bash
ros2 param list /turn_away
ros2 param get /turn_away forward_speed
ros2 param get /turn_away turn_speed
ros2 param get /turn_away max_turn_speed
```

Change the forward speed:

```bash
ros2 param set /turn_away forward_speed 0.3
```

Change the maximum permitted turn speed:

```bash
ros2 param set /turn_away max_turn_speed 1.5
```

### Test the custom turn-speed service

Enable the node first if necessary:

```bash
ros2 service call /turn_away_enable std_srvs/srv/SetBool "{data: true}"
```

Set a valid turning speed:

```bash
ros2 service call /set_turn_speed my_robot_interfaces/srv/SetTurnSpeed "{turn_speed: 1.0}"
```

The service should accept the value because it is positive and does not exceed the maximum.

Try an invalid value:

```bash
ros2 service call /set_turn_speed my_robot_interfaces/srv/SetTurnSpeed "{turn_speed: 3.0}"
```

The service should reject the value because it exceeds `max_turn_speed`.

Disable the node after testing:

```bash
ros2 service call /turn_away_enable std_srvs/srv/SetBool "{data: false}"
```

## Test robot status

With the relevant nodes running, inspect the robot status topic:

```bash
ros2 topic list
ros2 topic info /robot_status
ros2 topic echo /robot_status
```

The topic uses the custom message:

```text
my_robot_interfaces/msg/RobotStatus
```

It reports the robot's state and obstacle distance.

## Test the drive-distance action

With the robot control setup running, check that the action is available:

```bash
ros2 action list
ros2 action info /drive_distance
```

The action type is:

```text
lab_interfaces/action/DriveDistance
```

If the action server is available, send a short test goal:

```bash
ros2 action send_goal /drive_distance lab_interfaces/action/DriveDistance "{distance: 0.5}" --feedback
```

The command should show the goal response, feedback, and final result.

## Test the rotate action

Start the rotate action server if it is not already running. Use a separate sourced terminal:

```bash
cd ~/ros2_ws
source /opt/ros/humble/setup.bash
source ~/ros2_ws/install/setup.bash

ros2 run my_robot_nodes rotate_server
```

In another sourced terminal, check the action:

```bash
ros2 action list
ros2 action info /rotate
```

Send a rotation goal of approximately 90 degrees (1.57 radians):

```bash
ros2 action send_goal /rotate my_robot_interfaces/action/Rotate "{angle: 1.57}" --feedback
```

The action should provide feedback while rotating and a final result when it finishes.

## Test autonomous square movement

The square test uses the robot's control launch, the rotate action server, and the square driver. The `square.launch.py` launch file starts the required components together.

**Before starting:** Stop other simulation or robot-control launch processes from earlier tests. Do not run a second copy of the simulation at the same time.

### Run the square test

Open a fresh terminal:

```bash
cd ~/ros2_ws
source /opt/ros/humble/setup.bash
source ~/ros2_ws/install/setup.bash

ros2 launch my_robot_nodes square.launch.py
```

Keep this terminal running and watch the output.

Expected behavior:

- The robot and Gazebo simulation start.
- The rotate action server and square driver start.
- The square driver sends drive-distance and rotation goals.
- The robot drives four sides and rotates between sides.
- The robot completes a square and stops.

The default side length is `0.5` metres.

**Important:** Do not start `control.launch.py` separately before running `square.launch.py`. The square launch file already includes the required control launch. Starting both can create duplicate simulation or control nodes.

## Troubleshooting

Run these commands from a terminal where ROS 2 and the workspace have been sourced.

### Check whether the required nodes are running

```bash
ros2 node list
```

### Check whether the required topics exist

```bash
ros2 topic list
```

### Check whether obstacle messages are arriving

```bash
ros2 topic echo /obstacle
```

If no messages arrive, confirm that `control.launch.py` is running and that the obstacle detector started successfully.

### Check whether the services are available

```bash
ros2 service list
```

The turn-away test requires:

```text
/turn_away_enable
/set_turn_speed
```

### Check whether the actions are available

```bash
ros2 action list
```

The square test requires the drive-distance and rotate actions:

```text
/drive_distance
/rotate
```

### Fix a missing Python executable after cloning

If ROS 2 reports that `obstacle_detector.py` cannot be found or is not executable, run:

```bash
cd ~/ros2_ws/src/intro_robotics_intelligent_systems_labs/lab1_exercise/diffdrive_bot

chmod +x scripts/*.py

cd ~/ros2_ws

colcon build --symlink-install --packages-select diffdrive_bot

source /opt/ros/humble/setup.bash
source ~/ros2_ws/install/setup.bash
```

Then retry the launch or `ros2 run` command.

### Fix stale build paths

If the build refers to an old workspace location, clean and rebuild:

```bash
cd ~/ros2_ws

rm -rf build install log

source /opt/ros/humble/setup.bash

colcon build --symlink-install

source install/setup.bash
```
## Screenshots

The `screenshots/` directory contains:

- `rviz_depth_pointcloud.png` — RViz2 view of the depth camera and point cloud.
- `rqt_graph.png` — ROS 2 node communication graph.

## Expected Result

When launched successfully, the robot spawns in Gazebo, detects obstacles, publishes robot status, responds to movement and rotation actions, and executes an autonomous square path.

## Reflection: What Did Not Work

- **Gazebo sensor warnings:** Gazebo showed `gz_frame_id` compatibility warnings, but all sensors still published data correctly.
- **Rotate action:** The rotate action was unavailable in `control.launch.py` because its server was not included. Starting `rotate_server` separately fixed this.
- **Automated tests:** No automated test cases were registered, so functionality was verified manually using ROS 2 commands and Gazebo.
