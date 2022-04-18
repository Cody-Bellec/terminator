#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float32
from duckietown_msgs.msg import Twist2DStamped
from duckietown_msgs.msg import FSMState

class Circle:
	def __init__(self):
		self.pub = rospy.Publisher("/doczy/car_cmd_switch_node/cmd", Twist2DStamped, queue_size=10)
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

			c.moving(0.4, 2.4)
			rospy.sleep(10)
			c.moving(0, 0)
if __name__ == '__main__':
	try:
		rospy.init_node('Circle', anonymous=True)
		c = Circle()
		rospy.spin()
        
	except rospy.ROSInterruptException:
		pass
