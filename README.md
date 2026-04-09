# Gazebo Simulation Package

## Building the Package

```
colcon build --packages-select gazebo_sim
```

## Running the Simulation

Start the Gazebo world:
```
ros2 launch gazebo_sim start_world.launch.py
```

Spawn a model into the world:
```
ros2 launch gazebo_sim spawn_model.launch.py
```

Start the ROS-Gazebo bridge:
```
ros2 launch gazebo_sim start_bridge.launch.py
```