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



def main():
    rospy.init_node('smach_usecase_executive')

    sm_root = smach.StateMachine(outcomes=['succeeded','aborted','preempted'])

    with sm_root:

        smach.StateMachine.add('ResetTurtlesim',
                           ServiceState('reset',
                                        std_srvs.srv.Empty()),
                                        transitions={'succeeded':'spawnTurtle'})

        smach.StateMachine.add('spawnTurtle',
                           ServiceState('spawn',
                                        turtlesim.srv.Spawn,
                                        turtlesim.srv.SpawnRequest(0,0,0,'turtle2')),
                                        transitions={'succeeded':'moveTurtle1'})

        smach.StateMachine.add('moveTurtle1',
                            ServiceState('turtle1/teleport_absolute',
                                        turtlesim.srv.TeleportAbsolute,
                                        turtlesim.srv.TeleportAbsoluteRequest(5.0,1.0,0)),
                                        transitions={'succeeded':'moveTurtle2'})

        smach.StateMachine.add('moveTurtle2',
                            ServiceState('turtle2/teleport_absolute',
                                        turtlesim.srv.TeleportAbsolute,
                                        turtlesim.srv.TeleportAbsoluteRequest(9.0,5.0,0)),
                                        transitions={'succeeded':'draw_shapes'})

        sm_shapes_cc = smach.Concurrence(outcomes=['succeeded','aborted','preempted'],
                                        default_outcome='aborted',
                                        outcome_map= {'succeeded':{'undecagon':'succeeded', 'hexagon':'succeeded'}})

        smach.StateMachine.add('draw_shapes', sm_shapes_cc)

        with sm_shapes_cc:
            smach.Concurrence.add('undecagon',
                                smach_ros.SimpleActionState('turtle_shape1',
                                            turtle_actionlib.msg.ShapeAction,
                                            turtle_actionlib.msg.ShapeGoal(edges = 11, radius = 4.0)))

            sm_draw_monitor_cc = smach.Concurrence(['succeeded','aborted','preempted'],
                                'aborted',
                                child_termination_cb = lambda so: True,
                                outcome_map = {
                                'succeeded':{'DRAW':'succeeded'},
                                'preempted':{'DRAW':'preempted','MONITOR':'preempted'},
                                'aborted':{'MONITOR':'invalid'}})


            smach.Concurrence.add('hexagon', sm_draw_monitor_cc)
            with sm_draw_monitor_cc:

                smach.Concurrence.add('DRAW',
                        smach_ros.SimpleActionState('turtle_shape2',
                                turtle_actionlib.msg.ShapeAction,
                                turtle_actionlib.msg.ShapeGoal(edges = 6, radius = 0.5)))

                def turtle_far_away(userdata, msg):
                    if sqrt(pow(msg.x-9.0,2) + pow(msg.y-5.0,2)) > 1.0:
                        return True
                    return False

                smach.Concurrence.add('MONITOR',
                        smach_ros.MonitorState('/turtle1/pose',
                                turtlesim.msg.Pose,
                                cond_cb = turtle_far_away))







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
