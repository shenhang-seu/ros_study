import launch
import launch_ros
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    #获取默认的urdf路径
    #/home/shenhang/my_github/ros_study/chapter6/chapter6_ws/install/fishbot_description/share/fishbot_description/urdf/first_robot.urdf
    urdf_package_path = get_package_share_directory('fishbot_description')
    default_urdf_path = os.path.join(urdf_package_path,'urdf','first_robot.urdf')
    #/home/shenhang/my_github/ros_study/chapter6/chapter6_ws/src/fishbot_description/config/display_robot_model.rviz
    default_rviz_config_path = os.path.join(urdf_package_path,'config','display_robot_model.rviz')

    #声明一个urdf目录的参数, 方便修改
    action_declare_arg_mode_path = launch.actions.DeclareLaunchArgument(
        name='model',default_value=str(default_urdf_path),description='加载的模型文件路径'
    )

    #通过模型文件路径, 获取内容, 并转换成参数值对象, 以供传入robot_state_publisher节点的启动
    substitutions_command_result = launch.substitutions.Command(['cat ',launch.substitutions.LaunchConfiguration('model')])
    robot_description_value = launch_ros.parameter_descriptions.ParameterValue(substitutions_command_result,value_type=str)

    #ros2 run robot_state_publisher robot_state_publisher robot_description xxx
    action_robot_state_publisher = launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description':robot_description_value}]
    )

    #ros2 run joint_state_publisher joint_state_publisher
    action_joint_state_publisher = launch_ros.actions.Node(
        package='joint_state_publisher',
        executable='joint_state_publisher'
    )

    #ros2 run rviz2 rviz2 -d /home/shenhang/my_github/ros_study/chapter6/chapter6_ws/src/fishbot_description/config/display_robot_model.rviz
    action_rviz_node = launch_ros.actions.Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d',default_rviz_config_path]
    )

    return launch.LaunchDescription([
        action_declare_arg_mode_path,
        action_robot_state_publisher,
        action_joint_state_publisher,
        action_rviz_node
    ])