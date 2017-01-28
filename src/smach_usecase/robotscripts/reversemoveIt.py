#!/usr/bin/env python
import roslib
roslib.load_manifest('turtlebot_actions')

import rospy

import os
import sys
import time
import math
import numpy as np
from turtlebot_actions.msg import *
from actionlib_msgs.msg import *


import actionlib


# nur sinnvoll wenn moveIt und reversemoveIt sich wirklich aufheben


def main():
  rospy.init_node("reversemoveIt_action_client")

  angle = rospy.get_param("/CurrentAngle")
  distance = rospy.get_param("/CurrentDistance")

  rospy.delete_param("/CurrentAngle")
  rospy.delete_param("/CurrentDistance")







  # Construct action ac
  rospy.loginfo("Starting action client...")
  action_client = actionlib.SimpleActionClient('turtlebot_move', TurtlebotMoveAction)
  action_client.wait_for_server()
  rospy.loginfo("Action client connected to action server.")

  # Call the action
  rospy.loginfo("Calling the action server...")
  action_goal = TurtlebotMoveGoal()

  action_goal.turn_distance = np.deg2rad(0)
  action_goal.forward_distance = -distance # in m

  if action_client.send_goal_and_wait(action_goal, rospy.Duration(50.0), rospy.Duration(50.0)) == GoalStatus.SUCCEEDED:
    rospy.loginfo('Call to action server succeeded')
  else:
    rospy.logerr('Call to action server failed')


if __name__ == "__main__":
  main()
