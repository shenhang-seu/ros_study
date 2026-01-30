#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/twist.hpp"
#include "turtlesim/msg/pose.hpp"
#include <chrono>

#include "chapter4_interfaces/srv/partol.hpp"
using Partol = chapter4_interfaces::srv::Partol;

using namespace std;
using namespace std::chrono_literals;

class TurtleControlNode : public rclcpp::Node
{
private:
    // 订阅/turtle1/pose话题(消息接口为turtlesim/msg/Pose), 进行处理后发布/turtle1/cmd_vel话题(消息接口为geometry_msgs/msg/Twist)
    rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr publisher_; // 发布者, 消息类型为geometry_msgs/msg/Twist
    rclcpp::Subscription<turtlesim::msg::Pose>::SharedPtr subscriber_;  // 订阅者, 消息类型为turtlesim/msg/Pose
    rclcpp::Service<Partol>::SharedPtr partol_service_;                 // 巡检服务

    double target_x_{1.0};
    double target_y_{1.0};
    double k_{1.0};         // 比例系数
    double max_speed_{3.0}; // 最大速度

public:
    explicit TurtleControlNode(const std::string &node_name) : Node(node_name)
    {
        this->declare_parameter("k", 1.0);
        this->declare_parameter("max_speed", 1.0);
        this->get_parameter("k", k_);
        this->get_parameter("max_speed", max_speed_);

        publisher_ = this->create_publisher<geometry_msgs::msg::Twist>("/turtle1/cmd_vel", 10); // 因为小海龟订阅了这个话题, 所以这里发布该话题
        subscriber_ = this->create_subscription<turtlesim::msg::Pose>("/turtle1/pose", 10, bind(&TurtleControlNode::on_pose_received, this, placeholders::_1));

        // 创建的服务名称为partol
        partol_service_ = this->create_service<Partol>("partol", [&](const std::shared_ptr<Partol::Request> request, std::shared_ptr<Partol::Response> response) -> void {
            //std::shared_ptr<Partol::Request> request等价于Partol::Request::SharedPtr
            if ((0 < request->target_x && request->target_x < 12.0f) &&
                (0 < request->target_y && request->target_y < 12.0f))
            {
                this->target_x_ = request->target_x;
                this->target_y_ = request->target_y;
                response->result = Partol::Response::SUCCESS;
            }
            else
            {
                response->result = Partol::Response::FAIL;
            } });
    }

    void on_pose_received(const turtlesim::msg::Pose::SharedPtr pose)
    {
        // 1.获取当前位置
        auto current_x = pose->x;
        auto current_y = pose->y;
        RCLCPP_INFO(this->get_logger(), "cur x=%f, cur y=%f", current_x, current_y);

        // 2.计算当前海龟位置跟目标位置之间的距离差和角度差
        auto distance = sqrt((target_x_ - current_x) * (target_x_ - current_x) + (target_y_ - current_y) * (target_y_ - current_y));
        auto angle = atan2(target_y_ - current_y, target_x_ - current_x) - pose->theta;

        // 3.控制策略
        auto msg = geometry_msgs::msg::Twist();
        if (distance > 0.1)
        {
            if (fabs(angle) > 0.2)
            {
                msg.angular.z = fabs(angle); // 角速度
            }
            else
            {
                msg.linear.x = k_ * distance; // 线速度
            }
        }

        // 4.限制线速度最大值
        if (msg.linear.x > msg.linear.x)
        {
            msg.linear.x = max_speed_;
        }

        // 发布turtle1/cmd_vel话题, 由于小海龟订阅了该话题, 就会收到
        publisher_->publish(msg);
    }
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = make_shared<TurtleControlNode>("turtle_control");
    RCLCPP_INFO(node->get_logger(), "turtle_control");
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}