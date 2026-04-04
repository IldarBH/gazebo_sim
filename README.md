# Gazebo Simulation Package

## Building the Package

```
colcon build --packages-select gazebo_sim
```

## Running the Simulation

Start the Gazebo world:
```
ros2 launch gazebo_sim start_world.py
```

Spawn a model into the world:
```
ros2 launch gazebo_sim spawn_model.py
```
