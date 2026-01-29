import rclpy
from rclpy.node import Node
from chapter4_interfaces.srv import FaceDetector

import face_recognition
import cv2
from ament_index_python.packages import get_package_share_directory #获取功能包share目录绝对路径
import os

from cv_bridge import CvBridge

import time

class FaceDetectNode(Node):
    def __init__(self):
        super().__init__('face_detect_node')
        #FaceDetector是之前创建的自定义服务接口, face_detect是这里创建的服务名称
        self.service_ = self.create_service(FaceDetector, 'face_detect', self.detect_face_cb)
        self.bridge_ = CvBridge()
        self.declare_parameter('number_of_times_to_upsample',1)
        self.number_of_times_to_upsample_ = self.get_parameter('number_of_times_to_upsample').value
        self.declare_parameter('model','hog')
        self.model_ = self.get_parameter('model').value
        self.default_image_path_ = os.path.join(get_package_share_directory('demo_python_service'), 'resource/default.jpg')
        self.get_logger().info(f'服务已启动')
    
    def detect_face_cb(self, request, response):
        if request.image.data:
            cv_image = self.bridge_.imgmsg_to_cv2(request.image)
        else:
            cv_image = cv2.imread(self.default_image_path_)
        #cv_image已经是一个opencv格式的图像了
        start_time = time.time()
        self.get_logger().info(f'开始识别')
        #检测人脸
        face_locations = face_recognition.face_locations(cv_image, number_of_times_to_upsample=self.number_of_times_to_upsample_, model=self.model_)
        response.use_time = time.time() - start_time
        response.number = len(face_locations)
        for top,right,bottom,left in face_locations:
            response.top.append(top)
            response.right.append(right)
            response.bottom.append(bottom)
            response.left.append(left)
        return response #返回response给客户端

def main():
    rclpy.init()
    node = FaceDetectNode()
    rclpy.spin(node)
    rclpy.shutdown()