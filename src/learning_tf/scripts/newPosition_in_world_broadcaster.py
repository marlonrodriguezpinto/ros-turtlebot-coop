#!/usr/bin/env python
import roslib
import rospy

import tf
import turtlesim.msg


def handle_turtle_pose(msg, name):
    br = tf.TransformBroadcaster()
    br.sendTransform((msg.x, msg.y, 0),
                     tf.transformations.quaternion_from_euler(0, 0, msg.theta),
                     rospy.Time.now(),
                     name,
                     "world")

if __name__ == '__main__':
    rospy.init_node('chatter_tf_broadcaster')
    name = '/chatter'
    rospy.Subscriber('chatter',
                    turtlesim.msg.Pose,
                     handle_turtle_pose,
                     name)
    rospy.spin()
