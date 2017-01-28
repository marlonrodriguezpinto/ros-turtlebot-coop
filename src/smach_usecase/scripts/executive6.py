#!/usr/bin/env python


import roslib; # roslib.load_manifest('smach_usecase')
import std_srvs.srv
import rospy
import smach
import smach_ros
import turtlesim.srv
import turtlesim.msg
import turtle_actionlib.msg
from smach_ros import ServiceState
from math import sqrt, pow, atan2
import threading
from std_msgs.msg import String

# includes for searchObjekt class
from geometry_msgs.msg  import Twist
from turtlesim.msg import Pose



# gets called when ANY child state searchobjekt or PartnerCalled terminates
def child_term_cb(outcome_map):
  # terminate all running states if one State is finished
    if outcome_map['searchObjekt']:
        return True
    if outcome_map['PartnerCalled']:
        return True
    # in all other case, just keep running, don't terminate anything
    return False

def out_cb(outcome_map):

    if outcome_map['searchObjekt'] == 'succeeded':
        return 'decide'
    if outcome_map['searchObjekt'] == 'newobjekt':
        return 'aborted'
    elif outcome_map['PartnerCalled'] == 'succeeded':
        return 'help'
    else:
        return 'preempted'

def get_objekt():
    # get objektliste and check if liste ist Empty and if Obejct is in World
    while True:
        liste = rospy.get_param('/Objektliste')
        world = rospy.get_param('/Worldparameter')
        if liste:
            objekt = liste[0]
            rospy.loginfo(liste)
            del liste[0]
            rospy.loginfo('New liste online %s', liste)
            rospy.set_param('Objektliste', liste)
            if (world[0] < objekt[0] or world[1] < objekt[1] or objekt[0] < 0 or objekt[1] < 0):
                rospy.loginfo('Objekt not in World')
                continue
            return objekt
        else:
            rospy.loginfo('Liste is Empty')
            return 0

def put_objekt_back(objekt):
    liste = rospy.get_param('/Objektliste')
    liste.append(objekt)
    rospy.set_param('Objektliste'. liste)
    rospy.loginfo('objekt %s back in liste again %s', objekt, liste)
    return 0

def callback(data):
    rospy.loginfo('I heard %s', data.data)
    return data.data


class Stop(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded','aborted'])
        self.counter = 0

    def execute(self, userdata):
        rospy.loginfo('Executing state Stop')
        if self.counter < 1:
            self.counter += 1
            rospy.loginfo('liste of objekts should be ready in ROS')
            return 'aborted'
        else:
            return 'succeeded'


class getObjekt(smach.State):
    def __init__(self):
        smach.State.__init__(self,outcomes=['succeeded','aborted','preempted'],
                             output_keys=['objekt'])
        self.counter = 0

    def execute(self, userdata):
        rospy.loginfo('Executing state getObjekt')
        objekt = get_objekt()
        if self.preempt_requested():
            self.service_preempt()
            return 'preempted'
        if objekt:
            rospy.loginfo('Got this Position: %s', objekt)
            userdata.objekt = objekt
            return 'succeeded'
        else:
            return 'aborted'

class PartnerCalled(smach.State):
    def __init__(self):
        smach.State.__init__(self,outcomes=['succeeded','preempted'],
                            input_keys=['objekt'])
        self.counter = 0

    def execute(self,userdata):
        rospy.loginfo('listening if Partner called')
        while True:
            if self.preempt_requested():
                self.service_preempt()
                return 'preempted'
            helpcall = rospy.get_param('/Helpcall')
            if helpcall:
                objekt = userdata.objekt
                put_objekt_back(objekt)
                return 'succeeded'


class searchObjekt(smach.State):
    def __init__(self):
        self.velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
        self.pose_subscriber = rospy.Subscriber('/turtle1/pose', Pose, self.callback)
        self.pose = Pose()
        smach.State.__init__(self,outcomes=['succeeded','aborted','preempted'],
                            input_keys=['objekt'],
                            output_keys=['objekt_output','objekt_type'])
        self.counter = 0

    def callback(self, data):
        self.pose = data
        self.pose.x = round(self.pose.x, 2)
        self.pose.y = round(self.pose.y, 2)

    def move2goal(self, datalala):
        goal_pose = Pose()
        goal_pose.x = datalala[0]
        goal_pose.y = datalala[1]
        distance_tolerance = 0.1
        vel_msg = Twist()

        while sqrt(pow((goal_pose.x - self.pose.x), 2) + pow((goal_pose.y - self.pose.y), 2)) > distance_tolerance:

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

    def execute(self,userdata):
        self.counter += 1
        rospy.loginfo('Executing state searchObjekt')
        userdata.objekt_type = []
        time = rospy.get_time()
        duration = 30
        rospy.sleep(2.)
        while rospy.Duration(30) or not smach.is_shutdown():
            rospy.loginfo('ArUco searching for objekt while driving to Location')


            # broadcast_position.main(userdata.objekt)

            # smach_moveToGoal.main(userdata.objekt)
            rospy.loginfo('Get objektCode and save in userdata')
            userdata.objekt_output = userdata.objekt
            rospy.loginfo(self.counter)
            if (self.counter == 1):
                userdata.objekt_type = 24
                return 'succeeded'
            if self.preempt_requested():
                self.service_preempt()
                return 'preempted'
            return 'succeeded'
        rospy.loginfo('No objekt found -> deleting objekt')
        userdata.objekt_output = []
        return 'aborted'


class Decision(smach.State):
    def __init__(self):
        smach.State.__init__(self,outcomes=['singleobjekt','multiobjekt'],
                            input_keys=['objekt','objekt_type'],
                             output_keys=['objekt_output','objekt_type_output','objekt_right'])
        self.counter = 0

    def execute(self, userdata):
        rospy.loginfo('Executing state Decision')
        rospy.loginfo('Check for single or multi and if multi left or right for Partner')
        rospy.loginfo('TYPE is %s', userdata.objekt_type)
        if (userdata.objekt_type == 24):
            rospy.loginfo('set userdata type and right for multiobjekt')
            rospy.loginfo(userdata.objekt)
            userdata.objekt_type_output = []
            return 'multiobjekt'
        else:
            rospy.loginfo('A singleobjekt in Position %s', userdata.objekt)
            return 'singleobjekt'

class Alone(smach.State):
    def __init__(self):
        smach.State.__init__(self,outcomes=['succeeded','aborted','preempted'])
        self.counter = 0

    def execute(self, userdata):
        if self.preempt_requested():
            self.service_preempt()
            return 'preempted'
        rospy.loginfo('ALONE ALONE ALONE')
        rospy.loginfo('get in Position and go!')
        return 'succeeded'

class getHelp(smach.State):
    def __init__(self):
        smach.State.__init__(self,outcomes=['succeeded','aborted','preempted'],
                            input_keys=['objekt','objekt_type','objekt_right'],
                            output_keys=['objekt_output','objekt_type_output','objekt_right'])
        self.counter = 0

    def execute(self, userdata):
        rospy.loginfo('NEED HELP -> changed Helpcall to True')
        rospy.set_param('Helpcall', True)
        rospy.sleep(1.)
        if rospy.has_param('/Helpmode'):
            if rospy.get_param('/Helpmode'):
                rospy.loginfo('Send Location and listen for arrivial')
                helpPosition = userdata.objekt
                if objekt_right:
                    rospy.loginfo('helpPosition needs x y angle -> do it with TF')
                    helpPosition = helpPosition + 0.30
                rospy.set_param('HelpPosition', helpPosition)
                return 'succeeded'
            else:
                rospy.loginfo('Partner had no Time -> put objekt back -> reset Helpcall')
                rospy.set_param('Helpcall', False)
                put_objekt_back(userdata)
                return 'aborted'
        else:
            rospy.loginfo('No Robot answered -> reset Helpcall -> going for next objekt')
            rospy.set_param('Helpcall', False)
            return 'aborted'

class Helpmode(smach.State):
    def __init__(self):
        smach.State.__init__(self,outcomes=['succeeded','aborted','preempted'])
        self.counter = 0

    def execute(self, userdata):
        rospy.set_param('Helpmode', True)
        rospy.sleep(0.5)
        if rospy.has_param('/HelpPosition'):
            helpPosition = rospy.get_param('/HelpPosition')
            rospy.loginfo('Go to Goal and publish current distance to Goal')
            return 'succeeded'
        else:
            rospy.loginfo('No HelpPosition available')
            return 'aborted'


class Together(smach.State):
    def __init__(self):
        smach.State.__init__(self,outcomes=['succeeded','aborted','preempted'])
        self.counter = 0

    def execute(self, userdata):
        rospy.loginfo('Waiting for other Robot to get in Position')
        rospy.loginfo('listen to Partner, Partner sending Position and sending OK when in Position')

        rospy.loginfo('Checking Position updates to know if progress is made - otherwise Together fails -> objekt back to liste -> Helpmode to False -> Helpcall to False')
        rospy.loginfo('Set Time to Start moving at same time in same direction with same pace')
        return 'succeeded'

class Turtledance(smach.State):
    def __init__(self):
        smach.State.__init__(self,outcomes=['succeeded','aborted','preempted'])
        self.counter = 0

    def execute(self, userdata):
        rospy.loginfo('TODO: CONCURRENCE IF Helpcall ist True')
        rospy.loginfo('DANCE DANCE DANCE')

        return 'succeeded'



def main():
    rospy.init_node('smach_ex6')
    sm_root = smach.StateMachine(outcomes=['succeeded','aborted','preempted'])

    with sm_root:

        smach.StateMachine.add('STOP', Stop(),
                               transitions={'aborted':'getPosition',
                                            'succeeded':'succeeded'})

        smach.StateMachine.add('getPosition',
                            ServiceState('turtle1/teleport_absolute',
                                        turtlesim.srv.TeleportAbsolute,
                                        turtlesim.srv.TeleportAbsoluteRequest(5.0,1.0,0)),
                                        transitions={'succeeded':'START',
                                                    'aborted':'STOP'})

        sm_start = smach.StateMachine(outcomes=['aborted','preempted','succeeded'])
        sm_start.userdata.sm_objekt = []
        sm_start.userdata.sm_objekt_type = []
        sm_start.userdata.sm_right = []
        smach.StateMachine.add('START', sm_start,
                            transitions={'succeeded':'STOP',
                                        'preempted':'preempted'})
        with sm_start:

            smach.StateMachine.add('getObjekt', getObjekt(),
                                transitions={'succeeded':'Surrounding',
                                            'aborted':'succeeded',
                                            'preempted':'preempted'},
                                remapping={'objekt':'sm_objekt'})

            sm_surrounding_cc = smach.Concurrence(outcomes=['help','decide','preempted','newobjekt'],
                                            default_outcome='decide',
                                            input_keys = ['sm_objekt','sm_objekt_type'],
                                            output_keys = ['sm_objekt','sm_objekt_type'],
                                            child_termination_cb = child_term_cb,
                                            outcome_cb = out_cb)
            sm_surrounding_cc.userdata.sm_objekt = []
            sm_surrounding_cc.userdata.sm_objekt_type = []

            smach.StateMachine.add('Surrounding', sm_surrounding_cc,
                                    transitions={'decide':'Decision',
                                                'help':'Helpmode',
                                                'newobjekt':'getObjekt',
                                                'preempted':'preempted'},
                                    remapping={'sm_objekt':'sm_objekt',
                                            'sm_objekt_type':'sm_objekt_type'})

            with sm_surrounding_cc:

                smach.Concurrence.add('PartnerCalled', PartnerCalled())

                smach.Concurrence.add('searchObjekt', searchObjekt(),
                                remapping={'objekt':'sm_objekt',
                                            'real_objekt':'sm_objekt',
                                            'objekt_type':'sm_objekt_type'})


            smach.StateMachine.add('Helpmode', Helpmode(),
                                transitions={'succeeded':'succeeded',
                                            'aborted':'getObjekt',
                                            'preempted':'preempted'})


            smach.StateMachine.add('Decision', Decision(),
                                transitions={'singleobjekt':'Alone',
                                            'multiobjekt':'getHelp'},
                                remapping={'objekt':'sm_objekt',
                                        'objekt_type':'sm_objekt_type',
                                        'objekt_right':'sm_right'})



            smach.StateMachine.add('Alone', Alone(),
                                transitions={'succeeded':'getObjekt',
                                            'preempted':'preempted'})

            smach.StateMachine.add('getHelp', getHelp(),
                                transitions={'succeeded':'Together',
                                            'aborted':'getObjekt',
                                            'preempted':'preempted'})





            smach.StateMachine.add('Together', Together(),
                                transitions={})

        smach.StateMachine.add('Turtledance', Turtledance(),
                            transitions={'succeeded':'STOP'})










    sis = smach_ros.IntrospectionServer('sever_name2', sm_root, 'SM_ROOT2')
    sis.start()

    smach_ros.set_preempt_handler(sm_root)

    smach_thread = threading.Thread(target = sm_root.execute)
    smach_thread.start()




    #outcome = sm_root.execute()

    rospy.spin()
    sm_root.recall_preempt()
    smach_thread.join()
    sis.stop()

if __name__ == '__main__':
    main()
