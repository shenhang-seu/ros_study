#include <memory>
#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/transform_stamped.hpp" //消息接口geometry_msgs/TransformStamped对应的类
/*
ros2 interface show tf2_msgs/msg/TFMessage
geometry_msgs/TransformStamped[] transforms
        #
        #
        std_msgs/Header header
                builtin_interfaces/Time stamp
                        int32 sec
                        uint32 nanosec
                string frame_id
        string child_frame_id
        Transform transform
                Vector3 translation
                        float64 x
                        float64 y
                        float64 z
                Quaternion rotation
                        float64 x 0
                        float64 y 0
                        float64 z 0
                        float64 w 1
*/
#include "tf2/LinearMath/Quaternion.hpp"
#include "tf2_geometry_msgs/tf2_geometry_msgs.hpp" //消息类型转换函数 tf2::toMsg()
#include "tf2_ros/transform_listener.hpp"          //静态坐标监听类
#include "tf2_ros/buffer.hpp"
#include "tf2/utils.hpp" //提供了四元数转欧拉角的函数

#include <chrono>
using namespace std::chrono_literals;

class TFListener : public rclcpp::Node
{
private:
    std::shared_ptr<tf2_ros::TransformListener> listener_;
    rclcpp::TimerBase::SharedPtr timer_;
    std::shared_ptr<tf2_ros::Buffer> buffer_;

public:
    TFListener() : Node("tf_listener")
    {
        this->timer_ = this->create_wall_timer(1s, std::bind(&TFListener::get_transform, this));
        this->buffer_ = std::make_shared<tf2_ros::Buffer>(this->get_clock());
        this->listener_ = std::make_shared<tf2_ros::TransformListener>(*this->buffer_, this); // 一旦创建了监听器, 它就开始通过网络接收tf2变换
        /*
        tf2_ros::TransformListener的构造函数中的参数spin_thread
        spin_thread = true时‌: 构造函数会内部启动一个独立的ros回调线程
        这个线程会持续监听并处理来自 /tf 和 /tf_static 主题的变换消息, 无需用户在主程序中调用 ros::spin() 或 ros::spinOnce() 来驱动 TF 消息的接收
        这种方式简化了代码，避免了多线程竞争，是推荐的使用方式，尤其适用于需要稳定、实时监听变换的场景
        */
    }

    void get_transform()
    {
        // 到buffer_里查询坐标变换关系
        try
        {
            // 查询坐标关系
            const auto transform = buffer_->lookupTransform("base_link", "target_point", this->get_clock()->now(),
                                                            rclcpp::Duration::from_seconds(1.0f));
            auto translation = transform.transform.translation;
            auto rotation = transform.transform.rotation;
            double y, p, r;
            tf2::getEulerYPR(rotation, y, p, r);
            RCLCPP_INFO(this->get_logger(), "平移: %f,%f,%f", translation.x, translation.y, translation.z);
            RCLCPP_INFO(this->get_logger(), "旋转: %f,%f,%f", y, p, r);
        }
        catch (const std::exception &e)
        {
            RCLCPP_WARN(this->get_logger(), "%s", e.what());
        }
    }
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<TFListener>();
    RCLCPP_INFO(node->get_logger(), "tf_listener");
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}