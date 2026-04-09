from gazebo_sim.launch_utils import DEFAULT_WORLD_PATH
from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    world_sdf_file_arg = DeclareLaunchArgument(
        name='world_sdf', 
        default_value=DEFAULT_WORLD_PATH, 
        description='Path to the SDF world file')
    world_sdf_path = LaunchConfiguration('world_sdf')

    gz_sim_pkg_path = get_package_share_directory('ros_gz_sim')
    gz_sim_launch_path = PathJoinSubstitution([gz_sim_pkg_path, 'launch', 'gz_sim.launch.py'])
    gz_launch_action = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(gz_sim_launch_path),
        launch_arguments={'gz_args': world_sdf_path, 'on_exit_shutdown': 'True'}.items()
    )
 
    return LaunchDescription([
       world_sdf_file_arg, 
       gz_launch_action
    ])