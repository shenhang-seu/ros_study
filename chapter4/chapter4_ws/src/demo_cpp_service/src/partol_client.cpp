#include "rclcpp/rclcpp.hpp"
#include "chapter4_interfaces/srv/partol.hpp"
#include <chrono>
#include <ctime>
#include "rcl_interfaces/msg/parameter.hpp"
#include "rcl_interfaces/msg/parameter_value.hpp"
#include "rcl_interfaces/msg/parameter_type.hpp"
#include "rcl_interfaces/srv/set_parameters.hpp"
using SetParameters = rcl_interfaces::srv::SetParameters;

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

    // 创建客户端发送修改参数的resquest, 等待response
    SetParameters::Response::SharedPtr call_set_parameter(const rcl_interfaces::msg::Parameter &param)
    {
        auto client = this->create_client<SetParameters>("/turtle_control/set_parameters"); // 服务名称为/turtle_control/set_parameters, 对应类为SetParameters
        //1.检测服务端是否上线
        while(!client->wait_for_service(1s))
        {
            if (!rclcpp::ok())
            {
                return nullptr;
            }
            RCLCPP_INFO(this->get_logger(), "waiting service...");
        }
        //2.构造请求对象
        auto request = std::make_shared<SetParameters::Request>();
        request->parameters.push_back(param);
        //3.同步发送请求
        auto future = client->async_send_request(request);
        rclcpp::spin_until_future_complete(this->get_node_base_interface(), future);
        auto response = future.get();
        return response;
    }

    //更新服务端的参数k
    /*
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
    */
    void update_server_param_k(double k)
    {
        //1.创建参数对象
        auto param = rcl_interfaces::msg::Parameter();
        param.name = "k";
        //2.创建参数值
        auto param_value = rcl_interfaces::msg::ParameterValue();
        param_value.type = rcl_interfaces::msg::ParameterType::PARAMETER_DOUBLE;
        param_value.double_value = k;
        param.value = param_value;
        //3.发送request并处理response
        auto response = call_set_parameter(param);
        if (!response)
        {
            RCLCPP_INFO(this->get_logger(), "update param k failed");
            return;
        }

        for (auto result:response->results)
        {
            if (result.successful == false)
            {
                RCLCPP_INFO(this->get_logger(), "update param k failed, reason: %s", result.reason.c_str());
            }
            else
            {
                RCLCPP_INFO(this->get_logger(), "update param k success");
            }
        }
    }

};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<PartolClientNode>("partol_client_node");
    RCLCPP_INFO(node->get_logger(), "partol_client_node");
    node->update_server_param_k(3.0);
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}