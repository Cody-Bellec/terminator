#!/usr/bin/env python3

import rospy
import math
from std_msgs.msg import Float32
from odometry_hw.msg import Pose2D, DistWheel
from duckietown_msgs.msg import WheelEncoderStamped

class Odometry:
	def __init__(self):
		rospy.Subscriber("/doczy/left_wheel_encoder_node/tick", WheelEncoderStamped, self.callback_left)
		rospy.Subscriber("/doczy/right_wheel_encoder_node/tick", WheelEncoderStamped, self.callback_right)
		self.pub = rospy.Publisher('/pose', Pose2D, queue_size=10)
		
		self.prev_left = 0
		self.prev_right = 0
		
		self.flag_right = True
		self.flag_left = True
		
		self.new_flag_right = False
		self.new_flag_left = False
		
		self.Delta_sR = 0
		self.Delta_sL = 0

	global Pose
	Pose = Pose2D()
	Pose.x = 0
	Pose.y = 0
	Pose.theta = 0
	
	def odometry_calc(self):
	
	
		if self.new_flag_right == True and self.new_flag_left == True:
			
			L = 0.05

			Delta_s = (self.Delta_sL + self.Delta_sR)/2
			Delta_theta = (self.Delta_sR - self.Delta_sL)/(2*L)
			Delta_x = Delta_s * math.cos(Pose.theta + (Delta_theta/2))
			Delta_y = Delta_s * math.sin(Pose.theta + (Delta_theta/2))
			Pose.theta = Pose.theta + Delta_theta
			Pose.x = Pose.x + Delta_x
			Pose.y = Pose.y + Delta_y
			self.new_flag_right = False
			self.new_flag_left = False
			
			self.rospy.logwarn(Pose)
		
	def callback_right(self, tick):
	
		if self.flag_right == True:
			self.prev_right = tick.data
			self.flag_right = False
		else:
			self.Delta_sR = tick.data - self.prev_right
			self.prev_right = tick.data
			self.Delta_sR = self.Delta_sR * 0.001559 
			self.new_flag_right = True
		
	def callback_left(self, tick):
	
		if self.flag_left == True:
			self.prev_left = tick.data
			self.flag_left = False
		else:
			self.Delta_sL = tick.data - self.prev_left
			self.prev_left = tick.data
			self.Delta_sL = self.Delta_sL * 0.001559 
			self.new_flag_left = True
        
if __name__ == '__main__':
	try:
		rospy.init_node('Odometry', anonymous = True)
		lab2 = Odometry()
		while True:
			lab2.odometry_calc()
		
	except rospy.ROSInterruptException:
		pass
