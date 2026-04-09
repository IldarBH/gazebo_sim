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

    world_name_arg = DeclareLaunchArgument(
        name='world_name', 
        default_value='', 
        description='Name of the Gazebo world to spawn the model in')
    world_name = LaunchConfiguration('world_name')

    model_name_arg = DeclareLaunchArgument(
        name='model_name', 
        default_value='default_robot', 
        description='Name of the spawned model')
    model_name = LaunchConfiguration('model_name')

    robot_description_content = ParameterValue(
        Command(['cat ', LaunchConfiguration('model_urdf')]),
        value_type=str
    )
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': robot_description_content,
            'use_sim_time': True
        }]
    )
    ros_gz_bridge_node = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            ['/world/', world_name, '/model/', model_name, '/joint_state@sensor_msgs/msg/JointState[gz.msgs.Model'],
            ['/model/', model_name, '/odometry@nav_msgs/msg/Odometry[gz.msgs.Odometry'],
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
        ],
        remappings=[
            # This must be a tuple: ( [list_of_parts_for_old_topic], 'new_topic_name' )
            (
                ['/world/', world_name, '/model/', model_name, '/joint_state'], 
                '/joint_states'
            ),
            # If you want to remap odometry too:
            # (['/model/', model_name, '/odometry'], '/odom')
        ],
        output='screen'
    )


    # # TODO: Hardcoded sensor topics. Consider making these configurable via launch arguments or SDF parameters.
    # gz_bridge_lidar = Node(
    #     package='ros_gz_bridge',
    #     executable='parameter_bridge',
    #     arguments=['/sensors/lidar@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan'],
    #     output='screen'
    # )
    # gz_bridge_imu = Node(
    #     package='ros_gz_bridge',
    #     executable='parameter_bridge',
    #     arguments=['/sensors/imu@sensor_msgs/msg/Imu@gz.msgs.IMU'],
    #     output='screen'
    # )
    # gz_bridge_local = Node(
    #     package='ros_gz_bridge',
    #     executable='parameter_bridge',
    #     arguments=['/ground_truth/local@nav_msgs/msg/Odometry@gz.msgs.Odometry'],
    #     output='screen'
    # )
    # gz_bridge_global = Node(
    #     package='ros_gz_bridge',
    #     executable='parameter_bridge',
    #     arguments=['/ground_truth/global@nav_msgs/msg/Odometry@gz.msgs.Odometry'],
    #     output='screen'
    # )
    # gz_bridge_cmd_vel = Node(
    #     package='ros_gz_bridge',
    #     executable='parameter_bridge',
    #     arguments=['/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist'],
    #     output='screen'
    # )
    # gz_bridge_tf = Node(
    #     package='ros_gz_bridge',
    #     executable='parameter_bridge',
    #     arguments=['/tf@tf2_msgs/msg/TFMessage@gz.msgs.Pose_V'],
    #     output='screen'
    # )
    # gz_bridge_odom = Node(
    #     package='ros_gz_bridge',
    #     executable='parameter_bridge',
    #     arguments=['/odom@nav_msgs/msg/Odometry@gz.msgs.Odometry'],
    #     output='screen'
    # )

    return LaunchDescription([
        urdf_file_arg,
        world_name_arg,
        model_name_arg,
        robot_state_publisher_node,
        ros_gz_bridge_node
    ])
    
