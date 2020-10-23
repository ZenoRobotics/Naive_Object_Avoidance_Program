#! /usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

# rosmsg show LaserScan
# rostopic echo /scan

# Global Constants
scan_index_array = [377, 314, 251, 188, 125]  #Ls, Lw, F, Rs, Rw 
num_of_samples = 5
lsMin = 0.2           #min range in meters (8 in)
lwMin = 0.25          #min range in meters (10 in)
fMin  = 0.2           #min range in meters (8 in)
rwMin = 0.25          #min range in meters (10 in)
rsMin = 0.2           #min range in meters (8 in)
minRange = 0.12       #min and max range values (meters) reported by YDlidar G2
maxRange = 12         #
noReadingRange = 0.0  #usually reported for past maxRange (?)


# Define a function called 'callback' that receives a parameter named 'msg'
def callback(msg):             

    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Print the distance to an obstacle in front of the robot. The sensor returns a vector of m values, 
    # where m = 2*angle_max/angle_increment and the elements go from -180 degrees (element 0) to +180 degrees 
    # (element m-1) following the right hand rule (YDLidar G2 specific?):
    #
    #                     ^ 0
    #                     | x
    #                 y   |
    #             +90<----+---- -90
    #                     |
    #                     |
    #                 +180/-180
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
      
    #print('======================================')
    #print('Rs [125]')         #value right-direction laser beam
    #print msg.ranges[125] 
    #print('Rw [188]')         #value right/front-direction (9 o'clock) laser beam
    #print msg.ranges[188] 
    #print('F [251]')          #value front-direction laser beam
    #print msg.ranges[251]   
    #print('Lw [314]')         #value left/front-direction (3 o'clock) laser beam
    #print msg.ranges[314]    
    #print('Ls [377]')         #value left-direction laser beam
    #print msg.ranges[377] 

    Ls_Dist = getMinScanValue(msg, scan_index_array[0], num_of_samples)
    Lw_Dist = getMinScanValue(msg, scan_index_array[1], num_of_samples)
    F_Dist  = getMinScanValue(msg, scan_index_array[2], num_of_samples)
    Rw_Dist = getMinScanValue(msg, scan_index_array[3], num_of_samples)
    Rs_Dist = getMinScanValue(msg, scan_index_array[4], num_of_samples)
    
    # Obstacle avoidance logic
    if F_Dist <= fMin:  # front blocked?
      #check left or right 
      if Lw_Dist <= lwMin or Ls_Dist <= lsMin:  # left side blocked?
         if Rw_Dist <= rwMin or Rs_Dist <= rsMin:  # right side blocked?
           move.linear.x =  -0.5  # go backwards
           move.angular.z =  0.0
         else:
           move.linear.x  =  0.0  # turn right
           move.angular.z = -0.5
      elif Rw_Dist <= rwMin or Rs_Dist <= rsMin:  # right side blocked?
         move.linear.x  = 0.0
         move.angular.z = 0.5     # turn left
      else: #turn left or right based on greatest distance
         if Lw_Dist < Rw_Dist or Ls_Dist < Rs_Dist:   # right max
            move.linear.x  =  0.0  # turn right
            move.angular.z = -0.5
         else:
            move.linear.x  =  0.0  # turn left
            move.angular.z =  0.5

    elif Lw_Dist <= lwMin or Ls_Dist <= lsMin:  # left side blocked?
         if Rw_Dist <= rwMin or Rs_Dist <= rsMin:  # right side blocked?
           move.linear.x =  -0.5  # go backwards
           move.angular.z =  0.0
         else:
           move.linear.x  =  0.0  # turn right
           move.angular.z = -0.5

    elif Rw_Dist <= rwMin or Rs_Dist <= rsMin:  # right side blocked?
       move.linear.x  = 0.0
       move.angular.z = 0.5     # turn left
      
    else: #go forward
       move.linear.x  =  0.5 
       move.angular.z =  0.0
            

    pub.publish(move)


def getMinScanValue(msg, scan_index, angle_width):
    start_i = scan_index - angle_width//2
    end_i   = scan_index + angle_width//2
    min_reading = maxRange

    #find minimum range reading in angle_width beam
    for i in range(start_i, end_i, 1):
       if msg.ranges[i] > noReadingRange and msg.ranges[i] < min_reading:
           min_reading = msg.ranges[i]

    return min_reading
    
    

rospy.init_node('obstacle_avoidance')                  # Init a Node call 'obstacle_avoidance'
sub = rospy.Subscriber('/scan', LaserScan, callback)   # Create a Subscriber to the /scan topic
pub = rospy.Publisher('/cmd_vel', Twist)               # Create a Publisher on the /cmd_vel topic
move = Twist()

rospy.spin()
