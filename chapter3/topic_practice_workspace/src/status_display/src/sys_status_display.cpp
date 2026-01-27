#include <QApplication>
#include <QLabel>
#include <QString>
#include <rclcpp/rclcpp.hpp>
#include <status_interfaces/msg/system_status.hpp>

using SystemStatus = status_interfaces::msg::SystemStatus; // 自定义的消息接口类

class SysStatusDisplay : public rclcpp::Node
{
private:
    rclcpp::Subscription<SystemStatus>::SharedPtr subscriber_;
    std::shared_ptr<QLabel> label_;

    QString get_qstr_from_msg(const SystemStatus::SharedPtr msg)
    {
        std::stringstream show_str;
        show_str << "==================系统状态显示======================\n"
                 << "数据时间: " << msg->stamp.sec << " s\n"
                 << "主机名字: " << msg->hostname << " \n"
                 << "CPU使用率: " << msg->cpu_percent << " %\n"
                 << "内存使用率: " << msg->memory_percent << " %\n"
                 << "内存总大小: " << msg->memory_total << " MB\n"
                 << "剩余有效内存: " << msg->memory_available << " MB\n"
                 << "网络发送量: " << msg->net_send << " MB\n"
                 << "网络接收量: " << msg->net_recv << " MB\n"
                 << "==================================================";
        return QString::fromStdString(show_str.str());
    }

public:
    SysStatusDisplay(const std::string &node_name) : Node(node_name)
    {
        label_ = std::make_shared<QLabel>();
        subscriber_ = this->create_subscription<SystemStatus>("sys_status", 10, [&](const SystemStatus::SharedPtr msg) -> void
                                                              { label_->setText(get_qstr_from_msg(msg)); }); // 订阅sys_status话题
        label_->setText(get_qstr_from_msg(std::make_shared<SystemStatus>()));
        label_->show();
    }
};

int main(int argc, char *argv[])
{
    rclcpp::init(argc, argv);
    QApplication app(argc, argv);
    auto node = std::make_shared<SysStatusDisplay>("sys_status_display");
    std::thread spin_thread([&]() -> void
                            { rclcpp::spin(node); });

    spin_thread.detach();
    app.exec(); // 执行应用, 阻塞代码
    return 0;
}