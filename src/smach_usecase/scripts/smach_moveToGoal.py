#!/usr/bin/env python
import rospy
from geometry_msgs.msg  import Twist
from turtlesim.msg import Pose
from math import pow,atan2,sqrt
import sys
import executive6

class turtlebot():

    def __init__(self):
        #Creating the node,publisher and subscriber
        # rospy.init_node('turtlebot_controller', anonymous=True)
        self.velocity_publisher = rospy.Publisher('/robot_0/cmd_vel', Twist, queue_size=10)
        self.pose_subscriber = rospy.Subscriber('/robot_0/odom', Pose, self.callback)
        self.pose = Pose()
        # self.rate = rospy.Rate(10)

    #Callback function implementing the pose value received
    def callback(self, data):
        self.pose = data
        self.pose.x = round(self.pose.x, 4)
        self.pose.y = round(self.pose.y, 4)

    def get_distance(self, goal_x, goal_y):
        distance = sqrt(pow((goal_x - self.pose.x), 2) + pow((goal_y - self.pose.y), 2))
        return distance

    def move2goal(self, datalala):
        goal_pose = Pose()
        goal_pose.x = datalala[0]
        goal_pose.y = datalala[1]
        distance_tolerance = 0.2
        vel_msg = Twist()

        while sqrt(pow((goal_pose.x - self.pose.x), 2) + pow((goal_pose.y - self.pose.y), 2)) >= distance_tolerance:

            #Porportional Controller
            #linear velocity in the x-axis:
            vel_msg.linear.x = 1.5 * sqrt(pow((goal_pose.x - self.pose.x), 2) + pow((goal_pose.y - self.pose.y), 2))
            vel_msg.linear.y = 0
            vel_msg.linear.z = 0

            #angular velocity in the z-axis:
            vel_msg.angular.x = 0
            vel_msg.angular.y = 0
            vel_msg.angular.z = 4 * (atan2(goal_pose.y - self.pose.y, goal_pose.x - self.pose.x) - self.pose.theta)

            #Publishing our vel_msg
            self.velocity_publisher.publish(vel_msg)
            # self.rate.sleep()
        #Stopping the robot after the movement is over
        vel_msg.linear.x = 0
        vel_msg.angular.z =0
        self.velocity_publisher.publish(vel_msg)

def main():
    rospy.init_node('moveToGoal')
    objekt = rospy.get_param('/Current_Objekt')
    x = turtlebot()
    x.move2goal(objekt)


if __name__ == '__main__':
        #Testing the function
        try:
            main()
            if executive6.searchObjekt.preempt_requested():
                sys.exit(0)

        except rospy.ROSInterruptException, sys.exit:
            sys.exit(0)
