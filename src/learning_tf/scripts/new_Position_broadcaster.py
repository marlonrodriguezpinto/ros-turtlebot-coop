#!/usr/bin/env python

import roslib
# roslib.load_manifest('learning_tf')

import rospy
import tf
import turtlesim.msg

def listen_for_Position(msg, name):
    br = tf.TransformBroadcaster()
    br.sendTransform((msg.x, msg.y, 0),
                     tf.transformations.quaternion_from_euler(0, 0, msg.theta),
                     rospy.Time.now(),
                     name,
                     "world")


if __name__ == '__main__':
    rospy.init_node('new_Position_broadcaster')
    name = '/chatter'
    rospy.Subscriber('/chatter/pose',
                    turtlesim.msg.Pose,
                    listen_for_Position,
                    name)

    rospy.spin()
