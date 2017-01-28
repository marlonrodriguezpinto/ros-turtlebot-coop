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
        rospy.loginfo('Executing state Start')
        #ciao = rospy.loginfo('System Down at Start')

        # liste muss hier gebaut werden
        liste = [object1,object2,object3]
        userdata.liste = liste

        if self.counter > 0:
            return 'stop_all'

        else:
            self.counter += 1
            while not rospy.is_shutdown():
                return 'liste_abarbeiten'




class next_Obj(smach.State):
    def __init__(self):
        smach.State.__init__(self,outcomes=['alleine','done'],
                             input_keys=['list_of_objects', 'success'],
                             output_keys=['list_of_objects', 'object'])
        self.counter = 0

    def execute(self, userdata):
        rospy.loginfo('Executing state next_Obj')


        rospy.loginfo(userdata.list_of_objects)
        rospy.loginfo(userdata.success)
        # obejct = userdata.list_of_objects[self.counter]
        if self.counter == 0:
            self.counter += 1
            return 'alleine'

        else:
            if userdata.list_of_objects:
                if userdata.success:
                    del userdata.list_of_objects[0]
                    userdata.object = userdata.list_of_objects[0]
                else:
                    # get new order
                    problem_object = userdata.list_of_objects[0]
                    userdata.list_of_objects = userdata.list_of_objects[1:]
                    userdata.list_of_objects.append(problem_object)
                    # new obejct to work on
                    userdata.object = userdata.list_of_objects[0]

                rospy.loginfo(userdata.list_of_objects)
                rospy.loginfo(userdata.success)
                return 'alleine'
            else:
                return 'done'




class wegschaffen(smach.State):
    def __init__(self):
        smach.State.__init__(self,outcomes=['next_object'],
                                input_keys=['object'],
                                output_keys=['success'])
        self.counter = 0

    def execute(self, userdata):
        rospy.loginfo('Executing state wegschaffen')
        #ciao = rospy.loginfo('System Down at wegschaffen')
        if self.counter < 4:
            self.counter += 1
            if userdata.object == [3,4]:
                userdata.success = False
            else:
                userdata.success = True
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
    sm = smach.StateMachine(outcomes=['outcome4', 'outcome5'])
    sm.userdata.sm_liste = []
    sm.userdata.sm_object = []
    sm.userdata.success = 0

    # Open the container
    with sm:
        # Add states to the container
        smach.StateMachine.add('STOP', Stop(),
                               transitions={'outcome1':'START',
                                            'outcome2':'outcome4'})
        smach.StateMachine.add('START', Start(),
                               transitions={'stop_all':'STOP',
                                            'liste_abarbeiten':'NEXT OBJEKT'},
                               remapping={'liste':'sm_liste'})

        smach.StateMachine.add('NEXT OBJEKT', next_Obj(),
                                transitions={'alleine':'WEGSCHAFFEN',
                                             'done':'START'},
                                remapping={'list_of_objects':'sm_liste',
                                            'object':'sm_object'})

        smach.StateMachine.add('WEGSCHAFFEN', wegschaffen(),
                                transitions={'next_object':'NEXT OBJEKT'},
                                remapping={'object':'sm_object'})





    #sis = smach_ros.IntrospectionServer('sever_name', sm,'/SM_ROOT')
    #sis.start()

    # Execute SMACH plan

    outcome = sm.execute()

    #rospy.spin()
    #sis.stop()



if __name__ == '__main__':
    main()
