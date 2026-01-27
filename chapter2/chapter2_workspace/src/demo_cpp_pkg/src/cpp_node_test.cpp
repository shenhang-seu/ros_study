#include "rclcpp/rclcpp.hpp"
 
 
int main(int argc,char**argv)
{
  rclcpp::init(argc, argv);
  auto node=std::make_shared<rclcpp::Node>("cpp_node");//创建node对象，智能指针对象接管
  RCLCPP_INFO(node->get_logger(),"你好c++节点！");
  rclcpp::spin(node);//运行节点
  rclcpp::shutdown();
  return 0;
}