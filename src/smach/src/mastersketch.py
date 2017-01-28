#!/usr/bin/env python
import smach_ros
import roslib; # roslib.load_manifest('smach_tutorials')
import rospy
import smach


object1 = [1,2]
object2 = [3,4]
object3 = [5,6]


class Stop(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['outcome1','outcome2'])
        self.counter = 0

    def execute(self, userdata):
        rospy.loginfo('Executing state Stop')
        if self.counter < 1:
            self.counter += 1
            return 'outcome1'
        else:
            return 'outcome2'


# define state Bar
class Start(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['stop_all','liste_abarbeiten'],
                                    output_keys=['liste'])
        self.counter = 0

    def execute(self, userdata):
        self.counter += 1
        rospy.loginfo('Executing state Start')
        #ciao = rospy.loginfo('System Down at Start')

        # liste muss hier gebaut werden
        liste = [object1,object2,object3]

        if self.counter == 2:
            return 'stop_all'

        else:
            while not rospy.is_shutdown():
                return 'liste_abarbeiten'




class next_Obj(smach.State):
    def __init__(self):
        smach.State.__init__(self,outcomes=['alleine','done'],
                             input_keys=['list_of_objects'],
                             output_keys=['object'])
        self.counter = 0

    def execute(self, userdata):
        rospy.loginfo('Executing state next_Obj')


        rospy.loginfo(userdata.list_of_objects)
        #ciao = rospy.loginfo('System Down at next_Obj')
        if userdata.list_of_objects:
            return 'done'
        else:
            if self.counter < 3:
                self.counter += 1
                return 'alleine'
            else:
                return 'done'




class wegschaffen(smach.State):
    def __init__(self):
        smach.State.__init__(self,outcomes=['outcome4','next_object'],
                                output_keys=['object_done','object_rejected'])
        self.counter = 0

    def execute(self, userdata):
        rospy.loginfo('Executing state wegschaffen')
        #ciao = rospy.loginfo('System Down at wegschaffen')
        if self.counter < 3:
            self.counter += 1
            userdata.object_done = True
            return 'next_object'

class get_help(smach.State):
    def __init__(self):
        smach.State.__init__(self,outcomes=[])

    def execute(self, userdata):
        rospy.loginfo('Executing state get_help')
        #ciao = rospy.loginfo('System Down')
        return 0



# ------------ Hauptfunktion --------------------------
# main
def main():
    rospy.init_node('smach_master_state_machine')

    # Create a SMACH state machine
    sm = smach.StateMachine(outcomes=['outcome5'])
    sm.userdata.sm_liste = []

    # Open the container
    with sm:
        # Add states to the container
        smach.StateMachine.add('STOP', Stop(),
                               transitions={'outcome1':'START',
                                            'outcome2':'outcome5'})
        smach.StateMachine.add('START', Start(),
                               transitions={'stop_all':'STOP',
                                            'liste_abarbeiten':'NEXT OBJEKT'},
                               remapping={'liste':'sm_liste'})

        sm_liste_abarbeiten = smach.StateMachine(outcomes=['outcome4'])

        with sm_liste_abarbeiten:

            smach.StateMachine.add('NEXT OBJEKT', next_Obj(),
                                transitions={'alleine':'WEGSCHAFFEN',
                                             'done':'START'},
                                remapping={'list_of_objects':'sm_liste'})

            smach.StateMachine.add('WEGSCHAFFEN', wegschaffen(),
                                transitions={'next_object':'NEXT OBJEKT'})


        smach.StateMachine.add('LISTE_ABARBEITEN', sm_liste_abarbeiten,
                                transitions={'outcome4':'START'})




    #sis = smach_ros.IntrospectionServer('sever_name', sm,'/SM_ROOT')
    #sis.start()

    # Execute SMACH plan

    outcome = sm.execute()

    #rospy.spin()
    #sis.stop()



if __name__ == '__main__':
    main()
