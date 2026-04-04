# AI-assisted documentation:
# Some comments were generated with AI assistance to help explain
# functions and classes. The code and final documentation were
# reviewed by the author.
from pathlib import Path
from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    this_pkg_path = get_package_share_directory('gazebo_sim')
    default_world_sdf = Path(this_pkg_path) / 'worlds' / 'base_world.sdf'

    world_sdf_file_arg = DeclareLaunchArgument(name='world_sdf', default_value=str(default_world_sdf), description='Path to the SDF world file')
    world_sdf_path = PathJoinSubstitution([this_pkg_path, 'worlds', LaunchConfiguration('world_sdf')])

    gz_sim_pkg_path = get_package_share_directory('ros_gz_sim')
    gz_sim_launch_path = PathJoinSubstitution([gz_sim_pkg_path, 'launch', 'gz_sim.launch.py'])
    gz_launch_action = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(gz_sim_launch_path),
        launch_arguments={'gz_args': world_sdf_path, 'on_exit_shutdown': 'True'}.items()
    )
 
    ld = LaunchDescription()
    ld.add_action(world_sdf_file_arg)
    ld.add_action(gz_launch_action)
    return ld