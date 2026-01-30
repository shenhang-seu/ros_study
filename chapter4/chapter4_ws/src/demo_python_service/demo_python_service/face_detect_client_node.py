import rclpy
from rclpy.node import Node
from chapter4_interfaces.srv import FaceDetector

import face_recognition
import cv2
from ament_index_python.packages import get_package_share_directory #获取功能包share目录绝对路径
import os
from typing import List

from cv_bridge import CvBridge

import time

from rcl_interfaces.srv import SetParameters
from rcl_interfaces.msg import Parameter, ParameterValue, ParameterType

class FaceDetectClientNode(Node):
    def __init__(self):
        super().__init__('face_detect_client_node')
        #FaceDetector是之前创建的自定义服务接口, face_detect是服务端创建的服务名称
        self.client_ = self.create_client(FaceDetector, 'face_detect')#'/face_detect'也行
        self.bridge_ = CvBridge()
        self.image_path_ = os.path.join(get_package_share_directory('demo_python_service'), 'resource/test1.jpg')
        self.image_ = cv2.imread(self.image_path_)
        self.get_logger().info(f'客户端已启动')

    def call_set_parameters(self,parameters: List[Parameter]):
        """
        调用服务, 修改参数值
        """

        """
        SetParameters是服务接口, /face_detect_node/set_parameters是服务名称
        ros2 service list -t
        /face_detect_node/set_parameters [rcl_interfaces/srv/SetParameters]
        """
        #1.创建一个客户端,等待服务上线
        client = self.create_client(SetParameters, 'face_detect_node/set_parameters')
        while client.wait_for_service(timeout_sec=1.0) is False:
            self.get_logger().info(f'等待服务端启动')
        #2.创建request
        request = SetParameters.Request()
        request.parameters = parameters
        #3.调用服务端更新参数
        future = client.call_async(request)
        rclpy.spin_until_future_complete(self,future)#阻塞等待response返回
        response = future.result()
        return response
    
    def update_detect_model(self,model='hog'):
        """根据传入的model, 构造参数parameters, 然后调用call_set_parameters"""

        #1.创建参数对象
        """
        ros2 interface show rcl_interfaces/srv/SetParameters
        # A list of parameters to set.
        Parameter[] parameters
                string name
                ParameterValue value
                        uint8 type
                        bool bool_value
                        int64 integer_value
                        float64 double_value
                        string string_value
                        byte[] byte_array_value
                        bool[] bool_array_value
                        int64[] integer_array_value
                        float64[] double_array_value
                        string[] string_array_value
        ---
        # Indicates whether setting each parameter succeeded or not and why.
        SetParametersResult[] results
                bool successful
                string reason
        """
        param = Parameter()
        param.name = "model"
        #2.创建ParameterValue对象
        param_value = ParameterValue()
        param_value.string_value = model
        param_value.type = ParameterType.PARAMETER_STRING
        param.value = param_value

        #3.调用服务, 修改参数值
        response = self.call_set_parameters([param])
        for result in response.results:
            self.get_logger().info(f'结果: {result.successful} {result.reason}')


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
    node.update_detect_model('hog')
    node.send_request()
    node.update_detect_model('cnn')
    node.send_request()
    rclpy.spin(node)
    rclpy.shutdown()