#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float32
from duckietown_msgs.msg import Twist2DStamped
from duckietown_msgs.msg import FSMState

class Square:
	def __init__(self):
		self.pub = rospy.Publisher("/doczy/wheels_driver_node/wheels_cmd", Twist2DStamped, queue_size=10)
		self.sub = rospy.Subscriber("/doczy/fsm_node/mode", FSMState, self.callback)
		self.flag = True

	def moving(self, speed, turn_ratio):

		self.turnout = Twist2DStamped()
		self.turnout.v = speed
		self.turnout.omega = turn_ratio
		self.pub.publish(self.turnout)

	def callback(self, message):
		if message.state == "LANE_FOLLOWING" and self.flag == True:
	
			self.flag = False

			c.moving(0.4, 0.6)
			rospy.sleep(5.0)
			c.moving(0.0, 0.0)
			rospy.sleep(0.52)
			c.moving(0.0, 5.8)
			rospy.sleep(0.52)
			c.moving(0, 0)

			c.moving(0.4, 0.6)
			rospy.sleep(5.0)
			c.moving(0.0, 0.0)
			rospy.sleep(0.52)
			c.moving(0.0, 5.8)
			rospy.sleep(0.52)
			c.moving(0, 0)

			c.moving(0.4, 0.6)
			rospy.sleep(5.0)
			c.moving(0.0, 0.0)
			rospy.sleep(0.52)
			c.moving(0.0, 5.8)
			rospy.sleep(0.52)
			c.moving(0, 0)

			c.moving(0.4, 0.6)
			rospy.sleep(5.0)
			c.moving(0.0, 0.0) #stop
			rospy.sleep(0.52)
			c.moving(0.0, 5.8) #turning
			rospy.sleep(0.52)  #pause
			c.moving(0, 0)     #completely stops after all turns are made
	
	
if __name__ == '__main__':
	try:
		rospy.init_node('Circle', anonymous=True)
		c = Square()
		rospy.spin()
        
except rospy.ROSInterruptException:
	pass
