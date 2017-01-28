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


from math import sqrt, pow
import threading


class Stop(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded','aborted'])
        self.counter = 0

    def execute(self, userdata):
        rospy.loginfo('Executing state Stop')
        if self.counter < 1:
            self.counter += 1
            """ start another file to set parameter 'Objectlist' """
            rospy.loginfo('List of Objects should be ready in ROS')
            return 'aborted'
        else:
            return 'succeeded'




def get_object():

    rospy.loginfo('New List online')
    list = rospy.get_param('/Objectlist')
    if list:
        object = list[0]
        rospy.loginfo(list)
        del list[0]
        rospy.loginfo(list)
        rospy.set_param('Objectlist', list)

        return object
    else:
        rospy.loginfo('List is Empty')
        return 0

""" holt sich Objectposition
 faehrt Hin
 entscheidet, ob er alleine oder zusammen schiebt"""

class getObject(smach.State):
    def __init__(self):
        smach.State.__init__(self,outcomes=['succeeded','aborted','preempted'],
                             output_keys=['object'])
        self.counter = 0

    def execute(self, userdata):
        rospy.loginfo('Executing state getObject')
        object = get_object()
        if object:
            rospy.loginfo('Got this Position:')
            rospy.loginfo(object)
            userdata.object = object
            return 'succeeded'
        else:
            return 'aborted'

class searchObject(smach.State):
    def __init__(self):
        smach.State.__init__(self,outcomes=['succeeded','aborted','preempted'],
                            input_keys=['object'],
                            output_keys=['object_output','object_type'])
        self.counter = 0

    def execute(self,userdata):
        rospy.loginfo('Executing state searchObject')
        rospy.loginfo('ArUco searching for Object while driving to Location')
        userdata.object_output = userdata.object
        return 'succeeded'


class Decision(smach.State):
    def __init__(self):
        smach.State.__init__(self,outcomes=['singleObject','multiObject'],
                            input_keys=['object','object_type'],
                             output_keys=['object_output','object_type_output'])
        self.counter = 0

    def execute(self, userdata):
        rospy.loginfo('Executing state Decision')
        # get userdata to make Decision
        if userdata.object:
            rospy.loginfo(userdata.object)
            return 'singleObject'
        else:
            rospy.loginfo('multiObject')
            rospy.loginfo(userdata.object)
            return 'multiObject'

class Alone(smach.State):
    def __init__(self):
        smach.State.__init__(self,outcomes=['succeeded','aborted','preempted'])
        self.counter = 0

    def execute(self, userdata):
        rospy.loginfo('ALONE ALONE ALONE')
        return 'succeeded'

class getHelp(smach.State):
    def __init__(self):
        smach.State.__init__(self,outcomes=['succeeded','aborted','preempted'])
        self.counter = 0

    def execute(self, userdata):
        rospy.loginto('NEED HELP')
        return 'succeeded'


class Turtledance(smach.State):
    def __init__(self):
        smach.State.__init__(self,outcomes=['succeeded','aborted','preempted'])
        self.counter = 0

    def execute(self, userdata):
        rospy.loginfo('DANCE DANCE DANCE')
        return 'succeeded'



def main():
    rospy.init_node('smach_usecase_executive2')
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
        sm_start.userdata.sm_object = []
        sm_start.userdata.sm_object_type = []


        smach.StateMachine.add('START', sm_start)

        with sm_start:


            smach.StateMachine.add('getObject', getObject(),
                                transitions={'succeeded':'searchObject',
                                            'aborted':'succeeded',
                                            'preempted':'preempted'},
                                remapping={'object':'sm_object'})

            smach.StateMachine.add('searchObject', searchObject(),
                                transitions={'succeeded':'Decision',
                                            'preempted':'preempted'},
                                remapping={'object':'sm_object',
                                            'real_object':'sm_object',
                                            'object_type':'sm_object_type'})

            smach.StateMachine.add('Decision', Decision(),
                                transitions={'singleObject':'Alone',
                                            'multiObject':'getHelp'},
                                remapping={'object':'sm_object',
                                        'object_type':'sm_object_type'})

            smach.StateMachine.add('Alone', Alone(),
                                transitions={'succeeded':'getObject',
                                            'preempted':'preempted'})

            smach.StateMachine.add('getHelp', getHelp(),
                                transitions={'succeeded':'getObject',
                                            'preempted':'preempted'})

        smach.StateMachine.add('Turtledance', Turtledance(),
                            transitions={'succeeded':'STOP'})










    sis = smach_ros.IntrospectionServer('sever_name', sm_root, 'SM_ROOT')
    sis.start()

    smach_ros.set_preempt_handler(sm_root)

    smach_thread = threading.Thread(target = sm_root.execute)
    smach_thread.start()




    #outcome = sm_root.execute()

    rospy.spin()
    sis.stop()

if __name__ == '__main__':
    main()
