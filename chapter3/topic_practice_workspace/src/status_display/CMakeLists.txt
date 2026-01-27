cmake_minimum_required(VERSION 3.8)
project(status_display)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(status_interfaces REQUIRED)

find_package(Qt5 REQUIRED COMPONENTS Widgets)#新增
add_executable(hello_qt_exe src/hello_qt.cpp)#新增
add_executable(sys_status_display_exe src/sys_status_display.cpp)#新增
target_link_libraries(hello_qt_exe Qt5::Widgets)#新增
target_link_libraries(sys_status_display_exe Qt5::Widgets)#新增
ament_target_dependencies(sys_status_display_exe rclcpp status_interfaces)#新增

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

install(TARGETS hello_qt_exe sys_status_display_exe#新增
DESTINATION lib/${PROJECT_NAME}
)

ament_package()
