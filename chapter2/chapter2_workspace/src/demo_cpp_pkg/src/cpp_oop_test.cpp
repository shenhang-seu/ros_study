#include "rclcpp/rclcpp.hpp"
#include <iostream>
#include <string>
using namespace std;

class PersonNode : public rclcpp::Node
{
public:
    PersonNode(const string &name, int age) : Node(name)
    {
        this->name_ = name;
        this->age_ = age;
    }

    void eat(const string &food_name)
    {
        RCLCPP_INFO(this->get_logger(), "name:%s, age:%d, eat: %s", this->name_.c_str(), this->age_, food_name.c_str());
    }

private:
    string name_;
    int age_;
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<PersonNode>("cpp_node", 30); // 创建node对象，智能指针对象接管
    RCLCPP_INFO(node->get_logger(), "你好c++节点！");
    rclcpp::spin(node); // 运行节点
    rclcpp::shutdown();
    return 0;
}