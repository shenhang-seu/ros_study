import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/shenhang/ros_study/chapter3/topic_practice_workspace/install/status_publisher'
