#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float32
from duckietown_msgs.msg import Twist2DStamped

class Square:
    def __init__(self):
        self.pub = rospy.Publisher("/canard/car_cmd_switch_node/cmd", Twist2DStamped, queue_size=10)

    def moving(self, speed, turn_ratio):
        
        self.turnout = Twist2DStamped()
        self.turnout.v = speed
        self.turnout.omega = turn_ratio
          
        self.pub.publish(self.turnout)

if __name__ == '__main__':
    try:
        c = Square()
        rospy.init_node('circle', anonymous=True)
        
        c.moving(0.4, 0.6)
        rospy.sleep(2.5)
        c.moving(0.0, 0.0)
        c.moving(0.0, 5.8)
        rospy.sleep(0.52)
        c.moving(0, 0)
        
        c.moving(0.4, 0.6)
        rospy.sleep(2.5)
        c.moving(0.0, 0.0)
        c.moving(0.0, 5.8)
        rospy.sleep(0.52)
        c.moving(0, 0)
        
        c.moving(0.4, 0.6)
        rospy.sleep(2.5)
        c.moving(0.0, 0.0)
        c.moving(0.0, 5.8)
        rospy.sleep(0.52)
        c.moving(0, 0)
        
        c.moving(0.4, 0.6)
        rospy.sleep(2.5)
        c.moving(0.0, 0.0) #stop
        c.moving(0.0, 5.8) #turning
        rospy.sleep(0.52)  #pause
        c.moving(0, 0)     #completely stops after all turns are made
        
    except rospy.ROSInterruptException:
        pass
