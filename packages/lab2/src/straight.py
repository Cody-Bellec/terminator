#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float32
from duckietown_msgs.msg import Twist2DStamped

class Straight:
    def __init__(self):
        self.pub = rospy.Publisher("/doczy/wheels_driver_node/wheels_cmd", Twist2DStamped, queue_size=10)

    def moving(self, speed):
        
        self.turnout = Twist2DStamped()
        self.turnout.v = speed
          
        self.pub.publish(self.turnout)

if __name__ == '__main__':
    try:
        c = Straight()
        rospy.init_node('Straight Line', anonymous=True)
        
        c.moving(0.4, 0.6)
        rospy.sleep(2.5)
        c.moving(0.0, 0.0) #stop
        c.moving(0, 0)     #completely stops after all turns are made
        
    except rospy.ROSInterruptException:
        pass
