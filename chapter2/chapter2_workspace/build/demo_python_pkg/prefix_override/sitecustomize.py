import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/shenhang/ros_study/chapter2/chapter2_workspace/install/demo_python_pkg'
