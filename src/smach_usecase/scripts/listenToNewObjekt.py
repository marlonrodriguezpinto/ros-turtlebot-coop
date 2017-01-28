#!/usr/bin/env python
import roslib
import rospy
import math
import tf
import geometry_msgs.msg

if __name__ == '__main__':
    rospy.init_node('tf_R0NewGoal')

    listener_new = tf.TransformListener()

    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
        try:
            (distance,rot) = listener_new.lookupTransform('/robot_0/odom', '/NewObjektR0', rospy.Time(0))
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue

        rospy.set_param('NewObjektR0/distance', distance)
        rospy.set_param('NewObjektR0/rot', rot)

        rate.sleep()
