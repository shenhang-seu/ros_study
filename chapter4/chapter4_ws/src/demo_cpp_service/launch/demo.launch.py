import launch
import launch_ros

def generate_launch_description(): #函数名是写死的
    """"产生launch描述"""
    #ros2 run turtlesim turtlesim_node
    action_node_turtlesim_node = launch_ros.actions.Node(
        package='turtlesim',
        executable='turtlesim_node',
        output='screen'
    )

    #ros2 run demo_cpp_service partol_client_exe
    partol_client_node = launch_ros.actions.Node(
        package='demo_cpp_service',
        executable='partol_client_exe',
        output='log'
    )

    #ros2 run demo_cpp_service turtle_control_exe
    turtle_control_node = launch_ros.actions.Node(
        package='demo_cpp_service',
        executable='turtle_control_exe',
        output='both'
    )

    return launch.LaunchDescription([
        # actions动作
        action_node_turtlesim_node,
        partol_client_node,
        turtle_control_node
    ])