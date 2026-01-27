import rclpy #导入库
from rclpy.node import Node #导入rclpy.node下的类Node

def main():
    rclpy.init()#初始化工作，分配资源
    node=Node('python_node')#创建节点
    node.get_logger().info('你好 python 节点！')#get——logger（获取日至管理模块）；info（日志提示等级，它表示信息提示）
    rclpy.spin(node)#运行节点（阻塞，不能主动退出）,会不停检测执行节点是否会有变化
    rclpy.shutdown()#主动退出节点，进行清理
