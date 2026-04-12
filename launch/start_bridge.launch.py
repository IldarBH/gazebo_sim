from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node
from launch_ros.descriptions import ParameterValue

def generate_launch_description():
    urdf_file_arg = DeclareLaunchArgument(
        name='model_urdf', 
        default_value='', 
        description='Path to the URDF model file')
    urdf_file = LaunchConfiguration('model_urdf')

    robot_description_content = ParameterValue(Command(['cat ', urdf_file]), value_type=str)
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': robot_description_content,
            'use_sim_time': True
        }]
    )
    
    # TODO: Hardcoded. Consider making these configurable via yaml file.
    ros_gz_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/left_wheel_cmd@std_msgs/msg/Float64@gz.msgs.Double',
            '/right_wheel_cmd@std_msgs/msg/Float64@gz.msgs.Double',
            '/joint_states@sensor_msgs/msg/JointState[gz.msgs.Model',
            '/sensors/lidar@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan',
            '/sensors/imu@sensor_msgs/msg/Imu@gz.msgs.IMU',
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
        ],
        output='screen'
    )

    return LaunchDescription([
        urdf_file_arg,
        robot_state_publisher_node,
        ros_gz_bridge
    ])
    
