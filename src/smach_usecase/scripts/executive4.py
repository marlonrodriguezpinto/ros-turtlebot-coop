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
from std_msgs.msg import String
import smach_moveToGoal


# gets called when ANY child state terminates
def child_term_cb(outcome_map):
  # terminate all running states if BAR finished
    if outcome_map['searchObject']:
        return True
    if outcome_map['PartnerCalled']:
        return True
    # in all other case, just keep running, don't terminate anything
    return False

def out_cb(outcome_map):
    if outcome_map['searchObject'] == 'succeeded':
        return 'decide'
    if outcome_map['searchObject'] == 'newObject':
        return 'aborted'
    elif outcome_map['PartnerCalled'] == 'succeeded':
        return 'help'
    else:
        return 'preempted'

def get_object():
    list = rospy.get_param('/Objectlist')
    if list:
        object = list[0]
        rospy.loginfo(list)
        del list[0]
        rospy.loginfo('New List online %s', list)
        rospy.set_param('Objectlist', list)
        return object
    else:
        rospy.loginfo('List is Empty')
        return 0

def put_object_back(object):
    list = rospy.get_param('/Objectlist')
    list.append(object)
    rospy.set_param('Objectlist'. list)
    rospy.loginfo('Object %s back in List again %s', object, list)
    return 0

def callback(data):
    rospy.loginfo('I heard %s', data.data)
    return data.data


def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber('chatter', String, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

def talker():
    pub = rospy.Publisher('chatter', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        hello_str = "hello world %s" % rospy.get_time()
        rospy.loginfo(hello_str)
        pub.publish(hello_str)
        rate.sleep()

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


class getObject(smach.State):
    def __init__(self):
        smach.State.__init__(self,outcomes=['succeeded','aborted','preempted'],
                             output_keys=['object'])
        self.counter = 0

    def execute(self, userdata):
        rospy.loginfo('Executing state getObject')
        object = get_object()
        if self.preempt_requested():
            self.service_preempt()
            return 'preempted'
        if object:
            rospy.loginfo('Got this Position: %s', object)
            userdata.object = object
            return 'succeeded'
        else:
            return 'aborted'

class PartnerCalled(smach.State):
    def __init__(self):
        smach.State.__init__(self,outcomes=['succeeded','preempted'],
                            input_keys=['object'])
        self.counter = 0

    def execute(self,userdata):
        rospy.loginfo('Listening if Partner called')
        while True:
            if self.preempt_requested():
                self.service_preempt()
                return 'preempted'
            helpcall = rospy.get_param('/Helpcall')
            if helpcall:
                object = userdata.object
                put_object_back(object)
                return 'succeeded'


class searchObject(smach.State):
    def __init__(self):
        smach.State.__init__(self,outcomes=['succeeded','aborted','preempted'],
                            input_keys=['object'],
                            output_keys=['object_output','object_type'])
        self.counter = 0

    def execute(self,userdata):
        self.counter += 1
        rospy.loginfo('Executing state searchObject')
        userdata.object_type = []
        time = rospy.get_time()
        duration = 30
        rospy.sleep(2.)
        current_time = rospy.get_time() - time
        while (duration > (rospy.get_time() - time)):
            rospy.loginfo('ArUco searching for Object while driving to Location')
            smach_moveToGoal.main(userdata.object)
            rospy.loginfo('Get ObjectCode and save in userdata')
            userdata.object_output = userdata.object
            rospy.loginfo(self.counter)
            if (self.counter == 1):
                userdata.object_type = 24
                return 'succeeded'
            if self.preempt_requested():
                self.service_preempt()
                return 'preempted'
            return 'succeeded'
        rospy.loginfo('No Object found -> deleting Object')
        userdata.object_output = []
        return 'aborted'


class Decision(smach.State):
    def __init__(self):
        smach.State.__init__(self,outcomes=['singleObject','multiObject'],
                            input_keys=['object','object_type'],
                             output_keys=['object_output','object_type_output','object_right'])
        self.counter = 0

    def execute(self, userdata):
        rospy.loginfo('Executing state Decision')
        rospy.loginfo('Check for single or multi and if multi left or right for Partner')
        rospy.loginfo('TYPE is %s', userdata.object_type)
        if (userdata.object_type == 24):
            rospy.loginfo('set userdata type and right for multiObject')
            rospy.loginfo(userdata.object)
            userdata.object_type_output = []
            return 'multiObject'
        else:
            rospy.loginfo('A singleObject in Position %s', userdata.object)
            return 'singleObject'

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
                            input_keys=['object','object_type','object_right'],
                            output_keys=['object_output','object_type_output','object_right'])
        self.counter = 0

    def execute(self, userdata):
        rospy.loginfo('NEED HELP -> changed Helpcall to True')
        rospy.set_param('Helpcall', True)
        rospy.sleep(1.)
        if rospy.has_param('/Helpmode'):
            if rospy.get_param('/Helpmode'):
                rospy.loginfo('Send Location and listen for arrivial')
                helpPosition = userdata.object
                if object_right:
                    rospy.loginfo('helpPosition needs x y angle -> do it with TF')
                    helpPosition = helpPosition + 0.30
                rospy.set_param('HelpPosition', helpPosition)
                return 'succeeded'
            else:
                rospy.loginfo('Partner had no Time -> put Object back -> reset Helpcall')
                rospy.set_param('Helpcall', False)
                put_object_back(userdata)
                return 'aborted'
        else:
            rospy.loginfo('No Robot answered -> reset Helpcall -> going for next Object')
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
        rospy.loginfo('Listen to Partner, Partner sending Position and sending OK when in Position')

        rospy.loginfo('Checking Position updates to know if progress is made - otherwise Together fails -> Object back to list -> Helpmode to False -> Helpcall to False')
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
    rospy.init_node('smach_ex4')
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
        sm_start.userdata.sm_right = []
        smach.StateMachine.add('START', sm_start,
                            transitions={'succeeded':'STOP',
                                        'preempted':'preempted'})
        with sm_start:

            smach.StateMachine.add('getObject', getObject(),
                                transitions={'succeeded':'Surrounding',
                                            'aborted':'succeeded',
                                            'preempted':'preempted'},
                                remapping={'object':'sm_object'})

            sm_surrounding_cc = smach.Concurrence(outcomes=['help','decide','preempted','newObject'],
                                            default_outcome='decide',
                                            input_keys = ['sm_object','sm_object_type'],
                                            output_keys = ['sm_object','sm_object_type'],
                                            child_termination_cb = child_term_cb,
                                            outcome_cb = out_cb)
            sm_surrounding_cc.userdata.sm_object = []
            sm_surrounding_cc.userdata.sm_object_type = []

            smach.StateMachine.add('Surrounding', sm_surrounding_cc,
                                    transitions={'decide':'Decision',
                                                'help':'Helpmode',
                                                'newObject':'getObject',
                                                'preempted':'preempted'},
                                    remapping={'sm_object':'sm_object',
                                            'sm_object_type':'sm_object_type'})

            with sm_surrounding_cc:

                smach.Concurrence.add('PartnerCalled', PartnerCalled())

                smach.Concurrence.add('searchObject', searchObject(),
                                remapping={'object':'sm_object',
                                            'real_object':'sm_object',
                                            'object_type':'sm_object_type'})


            smach.StateMachine.add('Helpmode', Helpmode(),
                                transitions={'succeeded':'succeeded',
                                            'aborted':'getObject',
                                            'preempted':'preempted'})


            smach.StateMachine.add('Decision', Decision(),
                                transitions={'singleObject':'Alone',
                                            'multiObject':'getHelp'},
                                remapping={'object':'sm_object',
                                        'object_type':'sm_object_type',
                                        'object_right':'sm_right'})



            smach.StateMachine.add('Alone', Alone(),
                                transitions={'succeeded':'getObject',
                                            'preempted':'preempted'})

            smach.StateMachine.add('getHelp', getHelp(),
                                transitions={'succeeded':'Together',
                                            'aborted':'getObject',
                                            'preempted':'preempted'})





            smach.StateMachine.add('Together', Together(),
                                transitions={})

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
