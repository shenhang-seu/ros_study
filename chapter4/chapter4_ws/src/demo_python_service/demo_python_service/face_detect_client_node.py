import rclpy
from rclpy.node import Node
from chapter4_interfaces.srv import FaceDetector

import face_recognition
import cv2
from ament_index_python.packages import get_package_share_directory #获取功能包share目录绝对路径
import os

from cv_bridge import CvBridge

import time

class FaceDetectClientNode(Node):
    def __init__(self):
        super().__init__('face_detect_client_node')
        #FaceDetector是之前创建的自定义服务接口, face_detect是服务端创建的服务名称
        self.client_ = self.create_client(FaceDetector, 'face_detect')
        self.bridge_ = CvBridge()
        self.image_path_ = os.path.join(get_package_share_directory('demo_python_service'), 'resource/test1.jpg')
        self.image_ = cv2.imread(self.image_path_)
        self.get_logger().info(f'客户端已启动')
    
    def send_request(self):
        #1.判断服务端是否在线
        while self.client_.wait_for_service(timeout_sec=1.0) is False:
            self.get_logger().info(f'等待服务端启动')
        #2.构造Request
        request = FaceDetector.Request()
        request.image = self.bridge_.cv2_to_imgmsg(self.image_)
        #3.发送请求并等待处理完成
        future = self.client_.call_async(request)
        rclpy.spin_until_future_complete(self, future)#等待服务端返回response
        response = future.result()#获取response
        self.get_logger().info(f'收到response, 并检测到有{response.number}张人脸, 耗时{response.use_time}s')
        self.show_response(response)

    def show_response(self, response):
        for i in range(response.number):
            top = response.top[i]
            right = response.right[i]
            bottom = response.bottom[i]
            left = response.left[i]
            cv2.rectangle(self.image_,(left,top),(right,bottom),(255,0,0),4)
        cv2.imshow('Face Detect Result',self.image_)
        cv2.waitKey(0)

def main():
    rclpy.init()
    node = FaceDetectClientNode()
    node.send_request()
    rclpy.spin(node)
    rclpy.shutdown()