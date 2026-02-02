import launch
import launch_ros

def generate_launch_description(): #函数名是写死的
    #1.声明一个launch参数
    action_declare_arg_background_g = launch.actions.DeclareLaunchArgument('launch_arg_bg',default_value='150')
    action_declare_arg_max_speed = launch.actions.DeclareLaunchArgument('launch_max_speed',default_value='2.0')
    #2.把launch的参数手动传递给某个节点
    """"产生launch描述"""
    #ros2 run turtlesim turtlesim_node
    action_node_turtlesim_node = launch_ros.actions.Node(
        package='turtlesim',
        executable='turtlesim_node',
        parameters=[{'background_g': launch.substitutions.LaunchConfiguration('launch_arg_bg',default='150')}],
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
        parameters=[{'max_speed': launch.substitutions.LaunchConfiguration('launch_max_speed',default='2.0')}],
        output='both'
    )

    return launch.LaunchDescription([
        # actions动作
        action_declare_arg_background_g,
        action_declare_arg_max_speed,
        action_node_turtlesim_node,
        partol_client_node,
        turtle_control_node
    ])