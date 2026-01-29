#include "rclcpp/rclcpp.hpp"
#include "chapter4_interfaces/srv/partol.hpp"
#include <chrono>
#include <ctime>
using Partol = chapter4_interfaces::srv::Partol;

using namespace std::chrono_literals; // 可以使用10s 100ms

class PartolClientNode : public rclcpp::Node
{
private:
    rclcpp::TimerBase::SharedPtr timer_;
    rclcpp::Client<Partol>::SharedPtr partol_client_;

public:
    explicit PartolClientNode(const std::string &node_name) : Node(node_name)
    {
        srand(time(NULL));
        partol_client_ = this->create_client<Partol>("partol"); // 前面创建的服务名称为partol
        timer_ = this->create_wall_timer(10s, [&]() -> void {
            //1.检测服务端是否上线
            while(!partol_client_->wait_for_service(1s))
            {
                if (!rclcpp::ok())
                {
                    return;
                }
                RCLCPP_INFO(this->get_logger(), "waiting service...");
            }
            //2.构造请求对象
            auto request = std::make_shared<Partol::Request>();
            request->target_x = rand() % 15;
            request->target_y = rand() % 15;
            RCLCPP_INFO(this->get_logger(), "prepare target_x=%f, target_y=%f", request->target_x, request->target_y);
            //3.发送请求
            partol_client_->async_send_request(request, [&](rclcpp::Client<Partol>::SharedFuture result_future)->void {
                auto response = result_future.get();
                if (response->result == Partol::Response::SUCCESS)
                {
                    RCLCPP_INFO(this->get_logger(), "success");
                }
                else
                {
                     RCLCPP_INFO(this->get_logger(), "failed");
                }
            });

        });
    }
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<PartolClientNode>("partol_client_node");
    RCLCPP_INFO(node->get_logger(), "partol_client_node");
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}