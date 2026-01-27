cmake_minimum_required(VERSION 3.8)
project(demo_cpp_pkg)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)#新增, 事实上, rclcpp这个package依赖于ament_cmake, 所以就算上一句不写也没事
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)
include_directories(include)

add_executable(cpp_node_exe src/cpp_node_test.cpp)#新增
add_executable(cpp_oop_test_exe src/cpp_oop_test.cpp)
add_executable(cpp_thread_test_exe src/cpp_thread_test.cpp)

# target_include_directories(cpp_node_exe PUBLIC ${rclcpp_INCLUDE_DIRS})#新增
# target_link_libraries(cpp_node_exe PUBLIC ${rclcpp_LIBRARIES})#新增
ament_target_dependencies(cpp_node_exe rclcpp)#新增, 等价上面两句
ament_target_dependencies(cpp_oop_test_exe rclcpp)
ament_target_dependencies(cpp_thread_test_exe rclcpp)

install(TARGETS cpp_node_exe cpp_oop_test_exe cpp_thread_test_exe
  DESTINATION lib/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
