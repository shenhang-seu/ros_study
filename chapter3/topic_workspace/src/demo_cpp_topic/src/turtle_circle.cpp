#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/twist.hpp"
#include <chrono>
using namespace std;
using namespace std::chrono_literals;

class TurtleCircleNode : public rclcpp::Node
{
private:
    rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr publisher_; // 发布者
    rclcpp::TimerBase::SharedPtr timer_;

public:
    explicit TurtleCircleNode(const std::string &node_name) : Node(node_name)
    {
        publisher_ = this->create_publisher<geometry_msgs::msg::Twist>("/turtle1/cmd_vel", 10); // 因为小海龟订阅了这个话题
        timer_ = this->create_wall_timer(1000ms, bind(&TurtleCircleNode::timer_cb, this));
    }

    void timer_cb()
    {
        auto msg = geometry_msgs::msg::Twist();
        msg.linear.x = 1.0;
        msg.angular.z = 0.5;
        publisher_->publish(msg);
    }
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = make_shared<TurtleCircleNode>("turtle_circle");
    RCLCPP_INFO(node->get_logger(), "turtle_circle");
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}