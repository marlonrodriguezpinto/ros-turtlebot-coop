#!/usr/bin/env python

import rospy
from std_msgs.msg import String
import nav_msgs.msg

def talker():
    pub = rospy.Publisher('NewObjekt/pose', nav_msgs.msg._Odometry, queue_size=10)
    rospy.init_node('NewObjekt', anonymous=True)
    while not rospy.is_shutdown():
        rate = rospy.Rate(10)
        if rospy.has_param('/Current_Objekt'):
            objekt = rospy.get_param('/Current_Objekt')

        cmd = nav_msgs.msg._Odometry()
        cmd.x = objekt[0]
        cmd.y = objekt[1]
        cmd.theta = 0

    rospy.loginfo(cmd)
    pub.publish(cmd)


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
