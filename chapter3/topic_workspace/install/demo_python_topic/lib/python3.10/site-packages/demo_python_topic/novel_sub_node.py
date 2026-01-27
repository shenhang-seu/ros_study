import rclpy
from rclpy.node import Node
import espeakng
from example_interfaces.msg import String #消息接口
from queue import Queue
import threading
import time

class NovelSubNode(Node):
    def __init__(self, node_name):
        super().__init__(node_name)
        self.novels_queue_ = Queue()
        self.get_logger().info(f'{node_name}, start')
        self.novel_subscriber_ = self.create_subscription(String, 'novel', self.novel_cb, 10)#订阅/novel话题
        self.speaker_thread_ = threading.Thread(target=self.speaker_thread_func)
        self.speaker_thread_.start()

    def novel_cb(self, msg: String): #有消息的时候就会调用该函数
        self.novels_queue_.put(msg.data)

    def speaker_thread_func(self):
        speaker = espeakng.Speaker()
        speaker.voice = 'zh'

        while rclpy.ok():#检测当前ros上下文是否ok
            if self.novels_queue_.qsize() > 0:
                text = self.novels_queue_.get()
                self.get_logger().info(f'speak: {text}')
                speaker.say(text)#说
                speaker.wait()#等他说完
            else:
                time.sleep(1)



def main():
    rclpy.init()
    node=NovelSubNode('novel_sub')
    rclpy.spin(node)
    rclpy.shutdown()