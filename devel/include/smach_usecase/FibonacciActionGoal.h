// Generated by gencpp from file smach_usecase/FibonacciActionGoal.msg
// DO NOT EDIT!


#ifndef SMACH_USECASE_MESSAGE_FIBONACCIACTIONGOAL_H
#define SMACH_USECASE_MESSAGE_FIBONACCIACTIONGOAL_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>

#include <std_msgs/Header.h>
#include <actionlib_msgs/GoalID.h>
#include <smach_usecase/FibonacciGoal.h>

namespace smach_usecase
{
template <class ContainerAllocator>
struct FibonacciActionGoal_
{
  typedef FibonacciActionGoal_<ContainerAllocator> Type;

  FibonacciActionGoal_()
    : header()
    , goal_id()
    , goal()  {
    }
  FibonacciActionGoal_(const ContainerAllocator& _alloc)
    : header(_alloc)
    , goal_id(_alloc)
    , goal(_alloc)  {
  (void)_alloc;
    }



   typedef  ::std_msgs::Header_<ContainerAllocator>  _header_type;
  _header_type header;

   typedef  ::actionlib_msgs::GoalID_<ContainerAllocator>  _goal_id_type;
  _goal_id_type goal_id;

   typedef  ::smach_usecase::FibonacciGoal_<ContainerAllocator>  _goal_type;
  _goal_type goal;




  typedef boost::shared_ptr< ::smach_usecase::FibonacciActionGoal_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::smach_usecase::FibonacciActionGoal_<ContainerAllocator> const> ConstPtr;

}; // struct FibonacciActionGoal_

typedef ::smach_usecase::FibonacciActionGoal_<std::allocator<void> > FibonacciActionGoal;

typedef boost::shared_ptr< ::smach_usecase::FibonacciActionGoal > FibonacciActionGoalPtr;
typedef boost::shared_ptr< ::smach_usecase::FibonacciActionGoal const> FibonacciActionGoalConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::smach_usecase::FibonacciActionGoal_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::smach_usecase::FibonacciActionGoal_<ContainerAllocator> >::stream(s, "", v);
return s;
}

} // namespace smach_usecase

namespace ros
{
namespace message_traits
{



// BOOLTRAITS {'IsFixedSize': False, 'IsMessage': True, 'HasHeader': True}
// {'smach_usecase': ['/home/marlon/catkin_ws/devel/share/smach_usecase/msg'], 'actionlib_msgs': ['/opt/ros/indigo/share/actionlib_msgs/cmake/../msg'], 'std_msgs': ['/opt/ros/indigo/share/std_msgs/cmake/../msg']}

// !!!!!!!!!!! ['__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_parsed_fields', 'constants', 'fields', 'full_name', 'has_header', 'header_present', 'names', 'package', 'parsed_fields', 'short_name', 'text', 'types']




template <class ContainerAllocator>
struct IsFixedSize< ::smach_usecase::FibonacciActionGoal_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::smach_usecase::FibonacciActionGoal_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct IsMessage< ::smach_usecase::FibonacciActionGoal_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::smach_usecase::FibonacciActionGoal_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::smach_usecase::FibonacciActionGoal_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::smach_usecase::FibonacciActionGoal_<ContainerAllocator> const>
  : TrueType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::smach_usecase::FibonacciActionGoal_<ContainerAllocator> >
{
  static const char* value()
  {
    return "006871c7fa1d0e3d5fe2226bf17b2a94";
  }

  static const char* value(const ::smach_usecase::FibonacciActionGoal_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x006871c7fa1d0e3dULL;
  static const uint64_t static_value2 = 0x5fe2226bf17b2a94ULL;
};

template<class ContainerAllocator>
struct DataType< ::smach_usecase::FibonacciActionGoal_<ContainerAllocator> >
{
  static const char* value()
  {
    return "smach_usecase/FibonacciActionGoal";
  }

  static const char* value(const ::smach_usecase::FibonacciActionGoal_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::smach_usecase::FibonacciActionGoal_<ContainerAllocator> >
{
  static const char* value()
  {
    return "# ====== DO NOT MODIFY! AUTOGENERATED FROM AN ACTION DEFINITION ======\n\
\n\
Header header\n\
actionlib_msgs/GoalID goal_id\n\
FibonacciGoal goal\n\
\n\
================================================================================\n\
MSG: std_msgs/Header\n\
# Standard metadata for higher-level stamped data types.\n\
# This is generally used to communicate timestamped data \n\
# in a particular coordinate frame.\n\
# \n\
# sequence ID: consecutively increasing ID \n\
uint32 seq\n\
#Two-integer timestamp that is expressed as:\n\
# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')\n\
# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')\n\
# time-handling sugar is provided by the client library\n\
time stamp\n\
#Frame this data is associated with\n\
# 0: no frame\n\
# 1: global frame\n\
string frame_id\n\
\n\
================================================================================\n\
MSG: actionlib_msgs/GoalID\n\
# The stamp should store the time at which this goal was requested.\n\
# It is used by an action server when it tries to preempt all\n\
# goals that were requested before a certain time\n\
time stamp\n\
\n\
# The id provides a way to associate feedback and\n\
# result message with specific goal requests. The id\n\
# specified must be unique.\n\
string id\n\
\n\
\n\
================================================================================\n\
MSG: smach_usecase/FibonacciGoal\n\
# ====== DO NOT MODIFY! AUTOGENERATED FROM AN ACTION DEFINITION ======\n\
#goal definition\n\
int32 order\n\
";
  }

  static const char* value(const ::smach_usecase::FibonacciActionGoal_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::smach_usecase::FibonacciActionGoal_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.header);
      stream.next(m.goal_id);
      stream.next(m.goal);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct FibonacciActionGoal_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::smach_usecase::FibonacciActionGoal_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::smach_usecase::FibonacciActionGoal_<ContainerAllocator>& v)
  {
    s << indent << "header: ";
    s << std::endl;
    Printer< ::std_msgs::Header_<ContainerAllocator> >::stream(s, indent + "  ", v.header);
    s << indent << "goal_id: ";
    s << std::endl;
    Printer< ::actionlib_msgs::GoalID_<ContainerAllocator> >::stream(s, indent + "  ", v.goal_id);
    s << indent << "goal: ";
    s << std::endl;
    Printer< ::smach_usecase::FibonacciGoal_<ContainerAllocator> >::stream(s, indent + "  ", v.goal);
  }
};

} // namespace message_operations
} // namespace ros

#endif // SMACH_USECASE_MESSAGE_FIBONACCIACTIONGOAL_H