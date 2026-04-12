# Gazebo Simulation Package

## Building the Package

```
colcon build --packages-select gazebo_sim
```

## Running the Simulation

Start all components:
```
ros2 launch gazebo_sim start_sim.launch.py
```

Following are the individual steps to run the simulation:

1. Start the Gazebo world (with GUI):
    ```
    ros2 launch gazebo_sim start_world.launch.py \
      world_sdf:=<path_to_sdf_file>
    ```

2. Spawn a model into the world:
    ```
    ros2 launch gazebo_sim spawn_model.launch.py \
      model_urdf:=<path_to_urdf> \
      world_name:=<world_name> \
      model_name:=<model_name> \
      z:=<z_height>
    ```

3. Start the ROS-Gazebo bridge:
    ```
    ros2 launch gazebo_sim start_bridge.launch.py \
      model_urdf:=<path_to_urdf>
    ```