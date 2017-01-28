#!/usr/bin/env python

import rospy
from std_msgs.msg import String
import turtlesim.msg

def talker():
    pub = rospy.Publisher('NewObjektR0', turtlesim.msg.Pose, queue_size=10)
    rospy.init_node('NewObjekt_Publisher', anonymous=True)
    while not rospy.is_shutdown():
        rate = rospy.Rate(10)
        if rospy.has_param('/CurrentObjektR0'):
            objekt = rospy.get_param('/CurrentObjektR0')

        cmd = turtlesim.msg.Pose()
        cmd.x = objekt[0]
        cmd.y = objekt[1]
        cmd.theta = 0

    rospy.loginfo('Kommand von broadcastNewGoal %s', cmd)
    pub.publish(cmd)


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
