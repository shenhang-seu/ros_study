import rclpy
from rclpy.node import Node
import requests
from example_interfaces.msg import String #消息接口
from queue import Queue

class NovelPubNode(Node):
    def __init__(self, node_name):
        super().__init__(node_name)
        self.novels_queue_ = Queue()
        self.get_logger().info(f'{node_name}, start')
        self.novel_publisher_ = self.create_publisher(String, 'novel', 10)#创建话题发布者
        self.create_timer(5 ,self.timer_cb)#ros node提供的定时器
    
    def timer_cb(self):
        if self.novels_queue_.qsize() > 0:
            line = self.novels_queue_.get()
            msg = String()
            msg.data = line
            self.novel_publisher_.publish(msg)
            self.get_logger().info(f'publish: {msg}')

    
    def download(self, url):
        response = requests.get(url)
        response.encoding = 'utf-8'
        text = response.text
        self.get_logger().info(f'download {url}, len {len(text)}')
        for line in text.splitlines():
            self.novels_queue_.put(line)

def main():
    rclpy.init()
    node=NovelPubNode('novel_pub')
    node.download('http://0.0.0.0:8000/novel1.txt')
    rclpy.spin(node)
    rclpy.shutdown()