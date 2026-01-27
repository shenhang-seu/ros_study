cmake_minimum_required(VERSION 3.8)
project(cpp_node_test)

#找到ROS2的rclcpp包
find_package(rclcpp REQUIRED)

add_executable(cpp_node cpp_node_test.cpp)

# 链接rclcpp库
# target_link_libraries(cpp_node rclcpp::rclcpp)

MESSAGE(STATUS ${rclcpp_INCLUDE_DIRS}) #头文件以及rclcpp依赖的头文件
MESSAGE(STATUS ${rclcpp_LIBRARIES}) #库文件以及rclcpp依赖的库文件
target_include_directories(cpp_node PUBLIC ${rclcpp_INCLUDE_DIRS})
target_link_libraries(cpp_node PUBLIC ${rclcpp_LIBRARIES})