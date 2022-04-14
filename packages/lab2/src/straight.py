#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float32
from duckietown_msgs.msg import Twist2DStamped
from duckietown_msgs.msg import FSMState

class Straight:
    def __init__(self):
        self.pub = rospy.Publisher("/doczy/wheels_driver_node/wheels_cmd", Twist2DStamped, queue_size=10)
        self.sub = rospy.Subscriber("/doczy/fsm_node/mode", FSMState, self.callback)
        self.flag = True

    def moving(self, speed):
        
        self.turnout = Twist2DStamped()
        self.turnout.v = speed
          
        self.pub.publish(self.turnout)
    
    def callback(self, message):
    	if message.state == "LANE_FOLLOWING" and self.flag == True:
    		
    		self.flag = False
    		
    		c.moving(0.4, 0.6)
        	rospy.sleep(2.5)
        	c.moving(0.0, 0.0) #stop
        	c.moving(0, 0)     #completely stops after all turns are made

if __name__ == '__main__':
    try:
        rospy.init_node('Straight Line', anonymous=True)
        c = Straight()
        rospy.spin()
        
    except rospy.ROSInterruptException:
        pass
