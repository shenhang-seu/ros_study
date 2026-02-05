import launch
import launch_ros
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    #获取默认的路径
    #/home/shenhang/my_github/ros_study/chapter6/chapter6_ws/src/fishbot_description/urdf/fishbot/fishbot.urdf.xacro
    urdf_package_path = get_package_share_directory('fishbot_description')
    default_xacro_path = os.path.join(urdf_package_path,'urdf/fishbot/','fishbot.urdf.xacro')
    #/home/shenhang/my_github/ros_study/chapter6/chapter6_ws/src/fishbot_description/world/custom_room.world
    default_gazebo_world_path = os.path.join(urdf_package_path,'world','custom_room.world')

    #声明一个urdf目录的参数, 方便修改
    action_declare_arg_mode_path = launch.actions.DeclareLaunchArgument(
        name='model',default_value=str(default_xacro_path),description='加载的模型文件路径'
    )

    #通过模型文件路径, 获取内容, 并转换成参数值对象, 以供传入robot_state_publisher节点的启动
    substitutions_command_result = launch.substitutions.Command(['xacro ',launch.substitutions.LaunchConfiguration('model')])
    robot_description_value = launch_ros.parameter_descriptions.ParameterValue(substitutions_command_result,value_type=str)

    #ros2 run robot_state_publisher robot_state_publisher robot_description xxx
    action_robot_state_publisher = launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description':robot_description_value}]#/robot_description是robot_state_publisher节点会创建发布的话题(话题名是固定的)
    )

    #ros2 launch gazebo_ros gazebo.launch.py world:=xxx.world
    action_launch_gazebo = launch.actions.IncludeLaunchDescription(
        launch.launch_description_sources.PythonLaunchDescriptionSource(
            [get_package_share_directory('gazebo_ros'),'/launch','/gazebo.launch.py']
        ),
        launch_arguments=[('world',default_gazebo_world_path),('verbose','true')]
    )
   
    #把机器人加载到gazebo中
    #ros2 run gazebo_ros spawn_entity.py
    action_spawn_entity = launch_ros.actions.Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic','/robot_description','-entity','fishbot']
    )

    return launch.LaunchDescription([
        action_declare_arg_mode_path,
        action_robot_state_publisher,
        action_launch_gazebo,
        action_spawn_entity
    ])