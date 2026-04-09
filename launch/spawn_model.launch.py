from gazebo_sim.launch_utils import DEFAULT_MODEL_PATH
from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    urdf_file_arg = DeclareLaunchArgument(
        name='model_urdf', 
        default_value=DEFAULT_MODEL_PATH, 
        description='Path to the URDF model file')
    urdf_file = LaunchConfiguration('model_urdf')

    world_name_arg = DeclareLaunchArgument(
        name='world_name', 
        default_value='default_world', 
        description='World name to spawn the model in')
    world_name = LaunchConfiguration('world_name')
    
    model_name_arg = DeclareLaunchArgument(
        name='model_name', 
        default_value='default_robot', 
        description='Name of the spawned model')
    model_name = LaunchConfiguration('model_name')
    
    pose_z_arg = DeclareLaunchArgument(
        name='z', 
        default_value='0.1', 
        description='Z height to spawn the model at')
    pose_z = LaunchConfiguration('z')

    gz_spawn_action = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['--file', urdf_file, 
                   '--world', world_name,
                   '--name', model_name,
                   '--z', pose_z],
        output='screen'
    )

    return LaunchDescription([
        urdf_file_arg,
        world_name_arg,
        model_name_arg,
        pose_z_arg,
        gz_spawn_action,
        LogInfo(msg=[
            "Spawning model with parameters:", 
            "\nName: " , model_name, 
            "\nWorld: ", world_name, 
            "\nFile: ", urdf_file, 
            "\nHeight: ", pose_z
        ])
    ])
