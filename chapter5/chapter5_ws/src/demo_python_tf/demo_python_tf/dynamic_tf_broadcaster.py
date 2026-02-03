import rclpy
from rclpy.node import Node
from tf2_ros import TransformBroadcaster #坐标发布器类
from geometry_msgs.msg import TransformStamped #消息接口geometry_msgs/TransformStamped对应的类
"""
ros2 interface show tf2_msgs/msg/TFMessage
geometry_msgs/TransformStamped[] transforms
        #
        #
        std_msgs/Header header
                builtin_interfaces/Time stamp
                        int32 sec
                        uint32 nanosec
                string frame_id
        string child_frame_id
        Transform transform
                Vector3 translation
                        float64 x
                        float64 y
                        float64 z
                Quaternion rotation
                        float64 x 0
                        float64 y 0
                        float64 z 0
                        float64 w 1
"""
from tf_transformations import quaternion_from_euler #欧拉角转四元数
import math #角度转弧度函数

class TFBroadcaster(Node):
    def __init__(self):
        super().__init__('dynamic_tf_broadcaster')
        self.dynamic_broadcaster_ = TransformBroadcaster(self)
        self.timer_ = self.create_timer(0.01,self.publish_tf)

    def publish_tf(self):
        """
        发布静态TF, 从camera_link到bottle_link之间的坐标关系
        """
        transform = TransformStamped()
        transform.header.frame_id = 'camera_link'
        transform.child_frame_id = 'bottle_link'
        transform.header.stamp = self.get_clock().now().to_msg()

        transform.transform.translation.x = 0.2
        transform.transform.translation.y = 0.3
        transform.transform.translation.z = 0.5
        #q=x,y,z,w
        q = quaternion_from_euler(0,0,0)
        transform.transform.rotation.x = q[0]
        transform.transform.rotation.y = q[1]
        transform.transform.rotation.z = q[2]
        transform.transform.rotation.w = q[3]

        #发布坐标关系
        self.dynamic_broadcaster_.sendTransform(transform)
        self.get_logger().info(f'发布动态TF:{transform}')

def main():
    rclpy.init()
    node = TFBroadcaster()
    rclpy.spin(node)
    rclpy.shutdown()