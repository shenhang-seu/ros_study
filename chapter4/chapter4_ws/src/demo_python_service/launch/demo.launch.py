import launch
import launch_ros

def generate_launch_description(): #函数名是写死的
    """"产生launch描述"""
    #ros2 run demo_python_service face_detect_node_exe
    face_detect_node = launch_ros.actions.Node(
        package='demo_python_service',
        executable='face_detect_node_exe',
        output='screen'
    )

    #ros2 run demo_python_service face_detect_client_node_exe
    face_detect_client_node = launch_ros.actions.Node(
        package='demo_python_service',
        executable='face_detect_client_node_exe',
        output='screen'
    )

    return launch.LaunchDescription([
        # actions动作
        face_detect_node,
        face_detect_client_node,
    ])