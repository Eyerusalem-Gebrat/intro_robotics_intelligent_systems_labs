from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    side_length = LaunchConfiguration('side_length')

    return LaunchDescription([

        DeclareLaunchArgument(
            'side_length',
            default_value='0.5',
            description='Length of each side of the square in meters'
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                PathJoinSubstitution([
                    FindPackageShare('diffdrive_bot'),
                    'launch',
                    'control.launch.py'
                ])
            )
        ),

        Node(
            package='my_robot_nodes',
            executable='rotate_server',
            name='rotate_server',
            output='screen'
        ),

        Node(
            package='my_robot_nodes',
            executable='square_driver',
            name='square_driver',
            output='screen',
            parameters=[{'side_length': side_length}]
        ),
    ])