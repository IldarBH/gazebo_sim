from gazebo_sim.launch_utils import DEFAULT_WORLD_PATH, DEFAULT_MODEL_PATH, PACKAGE_PATH

from pathlib import Path
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, OpaqueFunction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.descriptions import ParameterValue

import xml.etree.ElementTree as ET

def get_world_name_from_sdf(sdf_path):
    tree = ET.parse(sdf_path)
    root = tree.getroot()
    # In SDF, the world tag is usually a direct child of <sdf>
    world = root.find('world')
    if world is not None:
        return world.get('name')
    else:
        raise ValueError(f"No <world> tag found in SDF file: {sdf_path}")
    
def process_world_name(context, *args, **kwargs):
    # This evaluates the 'pointer' into a real string path
    sdf_path_str = LaunchConfiguration('world_sdf').perform(context)
    
    # Use your function
    world_name = get_world_name_from_sdf(sdf_path_str)
    
    # Store it back into the launch system so other nodes can see it
    context.launch_configurations['world_name'] = world_name
    return []

def generate_launch_description():
    world_file_arg = DeclareLaunchArgument(
        name='world_sdf', 
        default_value=DEFAULT_WORLD_PATH, 
        description='Path to the SDF world file')
    world_file = LaunchConfiguration('world_sdf')

    model_file_arg = DeclareLaunchArgument(
        name='model_urdf', 
        default_value=DEFAULT_MODEL_PATH, 
        description='Path to the URDF model file')
    model_file = LaunchConfiguration('model_urdf')

    world_launch_path = Path(PACKAGE_PATH) / 'launch' / 'start_world.launch.py'
    world_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(world_launch_path),
        launch_arguments={'world_sdf': world_file}.items()
    )
    
    spawn_launch_path = Path(PACKAGE_PATH) / 'launch' / 'spawn_model.launch.py'
    resolve_world_name_action = OpaqueFunction(function=process_world_name)
    model_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(spawn_launch_path),
        launch_arguments={
            'model_urdf': model_file,
            'world_name': LaunchConfiguration('world_name'),
            'model_name': 'default_robot'  # This could also be made dynamic if needed
        }.items()
    )

    bridge_launch_path = Path(PACKAGE_PATH) / 'launch' / 'start_bridge.launch.py'
    bridge_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(bridge_launch_path),
        launch_arguments={
            'model_urdf': model_file,
            'world_name': LaunchConfiguration('world_name'),
            'model_name': 'default_robot'  # This could also be made dynamic if needed
        }.items()
    )

    return LaunchDescription([
        world_file_arg,
        model_file_arg,
        world_launch,
        resolve_world_name_action,
        model_launch,
        bridge_launch
    ])