#!/usr/bin/env python
import roslib
import rospy
import math
import tf
import geometry_msgs.msg
import nav_msgs.msg
import turtlesim.srv

if __name__ == '__main__':
    rospy.init_node('tf_robot1_newGoal')

    listener = tf.TransformListener()

    # turtle_vel = rospy.Publisher('turtle1/cmd_vel', nav_msgs.msg.Twist, queue_size=10)

    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
        try:
            (trans,rot) = listener.lookupTransform('/odomR1', '/NewObjekt/pose', rospy.Time(0))
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue

        rospy.set_param("NewObjekt/trans", trans)
        rospy.set_param("NewObjekt/rot", rot)



        rate.sleep()
