#! /usr/bin/env python

import roslib
roslib.load_manifest('moveaction')
import rospy
import actionlib

from moveaction.msg import MoveAction, MoveActionGoal

if __name__ == '__main__':
    rospy.init_node('goalaction')
    client = actionlib.SimpleActionClient('goalaction', MoveAction)
    client.wait_for_server()

    goal = MoveActionGoal()
    # Fill in the goal here
    client.send_goal(goal)
    client.wait_for_result(rospy.Duration.from_sec(5.0))
