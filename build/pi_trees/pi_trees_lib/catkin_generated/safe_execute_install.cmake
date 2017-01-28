execute_process(COMMAND "/home/marlon/catkin_ws/build/pi_trees/pi_trees_lib/catkin_generated/python_distutils_install.sh" RESULT_VARIABLE res)

if(NOT res EQUAL 0)
  message(FATAL_ERROR "execute_process(/home/marlon/catkin_ws/build/pi_trees/pi_trees_lib/catkin_generated/python_distutils_install.sh) returned error code ")
endif()
