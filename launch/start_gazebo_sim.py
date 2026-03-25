# AI-assisted documentation:
# Some comments were generated with AI assistance to help explain
# functions and classes. The code and final documentation were
# reviewed by the author.
import os
from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, SetEnvironmentVariable
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    this_pkg_path = get_package_share_directory('gazebo_sim')
    set_env_action = SetEnvironmentVariable('GZ_SIM_RESOURCE_PATH', this_pkg_path)
    
    world_sdf_file_arg = DeclareLaunchArgument(name='world_sdf', default_value='base_world.sdf', description='Path to the SDF world file')
    world_sdf_path = PathJoinSubstitution([this_pkg_path, 'worlds', LaunchConfiguration('world_sdf')])
    
    model_sdf_file_arg = DeclareLaunchArgument(name='model_sdf', default_value='base_model.sdf', description='Path to the SDF model file')
    model_sdf_path = PathJoinSubstitution([this_pkg_path, 'models', LaunchConfiguration('model_sdf')])

    gz_sim_pkg_path = get_package_share_directory('ros_gz_sim')
    gz_sim_launch_path = PathJoinSubstitution([gz_sim_pkg_path, 'launch', 'gz_sim.launch.py'])
    gz_launch_action = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(gz_sim_launch_path),
        launch_arguments={'gz_args': world_sdf_path, 'on_exit_shutdown': 'True'}.items()
    )

    gz_spawn_launch_path = PathJoinSubstitution([gz_sim_pkg_path, 'launch', 'gz_spawn_model.launch.py'])
    gz_spawn_action = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(gz_spawn_launch_path),
        launch_arguments={'world': 'base_world',
                          'file': model_sdf_path, 
                          'entity_name': 'default_robot',
                          'z': '0.1'}.items(),
    )

    ld = LaunchDescription()
    ld.add_action(set_env_action)
    ld.add_action(world_sdf_file_arg)
    ld.add_action(model_sdf_file_arg)
    ld.add_action(gz_launch_action)
    ld.add_action(gz_spawn_action)
    return ld
