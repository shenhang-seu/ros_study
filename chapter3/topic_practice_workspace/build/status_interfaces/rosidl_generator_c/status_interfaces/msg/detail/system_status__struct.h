// NOLINT: This file starts with a BOM since it contain non-ASCII characters
// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from status_interfaces:msg/SystemStatus.idl
// generated code does not contain a copyright notice

#ifndef STATUS_INTERFACES__MSG__DETAIL__SYSTEM_STATUS__STRUCT_H_
#define STATUS_INTERFACES__MSG__DETAIL__SYSTEM_STATUS__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.h"
// Member 'hostname'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/SystemStatus in the package status_interfaces.
typedef struct status_interfaces__msg__SystemStatus
{
  /// 记录时间戳, 来自builtin_interfaces/msg/Time功能包
  builtin_interfaces__msg__Time stamp;
  /// ros2内置默认消息类型
  rosidl_runtime_c__String hostname;
  /// ros2内置默认消息类型
  float cpu_percent;
  /// ros2内置默认消息类型
  float memory_percent;
  /// ros2内置默认消息类型
  float memory_total;
  /// ros2内置默认消息类型
  float memory_available;
  /// ros2内置默认消息类型 网络发送数据总量
  double net_send;
  /// ros2内置默认消息类型 网络接收数据总量 MB
  double net_recv;
} status_interfaces__msg__SystemStatus;

// Struct for a sequence of status_interfaces__msg__SystemStatus.
typedef struct status_interfaces__msg__SystemStatus__Sequence
{
  status_interfaces__msg__SystemStatus * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} status_interfaces__msg__SystemStatus__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // STATUS_INTERFACES__MSG__DETAIL__SYSTEM_STATUS__STRUCT_H_
