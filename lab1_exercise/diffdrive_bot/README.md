# Diffdrive_bot

This package contains the differential-drive robot model and simulation resources used in the ROS 2 Lab 1 exercise.

## Package contents

- `urdf/` — Robot description, including the differential-drive base and attached sensors.
- `launch/` — Launch files for displaying the robot, starting the Gazebo simulation, and configuring robot control.
- `config/` — Configuration files for ROS-Gazebo communication.
- `worlds/` — Gazebo world files.
- `scripts/` — Supporting scripts used by the robot simulation.

## Launch files

The package provides these launch files:

- `display.launch.py` — Displays the robot model.
- `gazebo.launch.py` — Starts the Gazebo simulation.
- `control.launch.py` — Starts the robot control setup.

## Setup and usage

Follow the complete installation, build, and execution instructions in the [Lab 1 exercise README](../README.md).

Run commands from the ROS 2 workspace root:

```bash
cd ~/ros2_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
```

Refer to the exercise README for the correct launch sequence and testing instructions.