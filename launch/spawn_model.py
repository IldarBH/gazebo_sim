# AI-assisted documentation:
# Some comments were generated with AI assistance to help explain
# functions and classes. The code and final documentation were
# reviewed by the author.
from pathlib import Path
from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    this_pkg_path = get_package_share_directory('gazebo_sim')
    default_model_sdf = Path(this_pkg_path) / 'models' / 'base_model.sdf'

    model_sdf_file_arg = DeclareLaunchArgument(name='model_sdf', default_value=str(default_model_sdf), description='Path to the SDF model file')
    spawn_world_arg = DeclareLaunchArgument(name='world', default_value='base_world', description='World name to spawn the model in')
    spawn_name_arg = DeclareLaunchArgument(name='name', default_value='default_robot', description='Name of the spawned model')
    spawn_z_arg = DeclareLaunchArgument(name='z', default_value='0.1', description='Z height to spawn the model at')

    gz_spawn_action = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['--world', LaunchConfiguration('world'),
                   '--file', LaunchConfiguration('model_sdf'),
                   '--name', LaunchConfiguration('name'),
                   '--z', LaunchConfiguration('z')],
        output='screen'
    )

    gz_bridge_lidar = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=['/sensors/lidar@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan'],
        output='screen'
    )
    
    gz_bridge_imu = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=['/sensors/imu@sensor_msgs/msg/Imu@gz.msgs.IMU'],
        output='screen'
    )

    ld = LaunchDescription()
    ld.add_action(model_sdf_file_arg)
    ld.add_action(spawn_world_arg)
    ld.add_action(spawn_name_arg)
    ld.add_action(spawn_z_arg)
    ld.add_action(gz_spawn_action)
    ld.add_action(gz_bridge_lidar)
    ld.add_action(gz_bridge_imu)
    return ld
