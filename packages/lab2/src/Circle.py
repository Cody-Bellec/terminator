#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float32
from duckietown_msgs.msg import Twist2DStamped

class Circle:
    def __init__(self):
        self.pub = rospy.Publisher("/canard/car_cmd_switch_node/cmd", Twist2DStamped, queue_size=10)

    def moving(self, speed, turn_ratio):
        
        self.turnout = Twist2DStamped()
        self.turnout.v = speed
        self.turnout.omega = turn_ratio
          
        self.pub.publish(self.turnout)

if __name__ == '__main__':
    try:
        c = Circle()
        rospy.init_node('circle', anonymous=True)
        c.moving(0.4, 3.8)
        rospy.sleep(10)
        c.moving(0, 0)
        
    except rospy.ROSInterruptException:
        pass
