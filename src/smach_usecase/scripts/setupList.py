#!/usr/bin/env python

# sets new List of Objects

import roslib; # roslib.load_manifest('smach_usecase')
import std_srvs.srv
import rospy
import smach
import smach_ros






def publish_list():
    rospy.set_param('Objektliste', [(2,3,0),(4,4,0),(6,7,0),(2,2,0)])
    rospy.loginfo('List is online')
    return 0

def set_world_parameter():
    rospy.set_param('Worldparameter', (5.0, 5.0))
    rospy.loginfo('World is online')

def publish_startposition():
    rospy.set_param('Startposition', (0,0))


def publish_helpcall():
    rospy.set_param('Helpcall', False)
    rospy.loginfo('Helpcall is online')

def main():

    rospy.init_node('setObject')
    publish_list()
    publish_helpcall()
    set_world_parameter()
    publish_startposition()
    rospy.loginfo('Done')



if __name__ == '__main__':
    main()
