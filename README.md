# Naive_Object_Avoidance_Program

This is a simple, relatively naive object avoidance algorithm using Python for the ZRbot and tankbot (YDLidar G2 specific). 
The Python code creates an ‘obstacle_avoidance node in ROS, which subscribes to the /scan topic that is supplied by the lidar & code,
and publishes the /cmd_vel topic. The Arduino subscribes to the /cmd_vel topic using ROSSerial. The Arduino then controls the robot’s 
motors based on /cmd_vel topic (Twist data) values. An essential part of the explore algorithm is to perform obstacle avoidance. 
