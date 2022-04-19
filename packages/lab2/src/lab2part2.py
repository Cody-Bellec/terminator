#!/usr/bin/env python3

import rospy
import math
from std_msgs.msg import Float32
from odometry_hw.msg import Pose2D
from duckietown_msgs.msg import WheelEncoderStamped

class Odometry:
	def __init__(self):
		rospy.Subscriber("/doczy/left_wheel_encoder_node/tick", WheelEncoderStamped, self.callback)
		rospy.Subscriber("/doczy/right_wheel_encoder_node/tick", WheelEncoderStamped, self.callback)
		self.pub = rospy.Publisher('/pose', Pose2D, queue_size=10)

	global Pose
	Pose = Pose2D()
	Pose.x = 0
	Pose.y = 0
	Pose.theta = 0
		
	def callback(self,wheel):
		Delta_sL = wheel.dist_wheel_left
		Delta_sR = wheel.dist_wheel_right

		L = 0.05

		Delta_s = (Delta_sL + Delta_sR)/2
		Delta_theta = (Delta_sR - Delta_sL)/(2*L)
		Delta_x = Delta_s * math.cos(Pose.theta + (Delta_theta/2))
		Delta_y = Delta_s * math.sin(Pose.theta + (Delta_theta/2))
		Pose.theta = Pose.theta + Delta_theta
		Pose.x = Pose.x + Delta_x
		Pose.y = Pose.y + Delta_y
		

		self.pub.publish(Pose)
        
if __name__ == '__main__':
	try:
		rospy.init_node('Odometry', anonymous = True)
		lab2part2()
		rospy.spin()
	except rospy.ROSInterruptException:
		pass
