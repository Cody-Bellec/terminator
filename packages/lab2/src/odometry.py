#!/usr/bin/env python3

import rospy
import math
from std_msgs.msg import Float32
from odometry_hw.msg import Pose2D, DistWheel
from duckietown_msgs.msg import WheelEncoderStamped
from numpy import *

class Odometry(object):
	def __init__(self):
		self.node_name = rospy.get_name()
		self.vehicle_name = self.node_name.split("/")[1]
		
		self.last_position = Pose2D()
		self.last_theta_dot = 0
		self.last_velocity = 0
		
		rospy.Subscriber("/dist_wheel", DistWheel, self.velocity_callback)
		rospy.Subscriber("/doczy/left_wheel_encoder_node/tick", WheelEncoderStamped, self.velocity_callback)
		rospy.Subscriber("/doczy/right_wheel_encoder_node/tick", WheelEncoderStamped, self.velocity_callback)
		self.pub_pose = rospy.Publisher('/pose', Pose2D, queue_size=1)
		rospy.loginfo("[%s] Initialized.", self.node_name)

		
	def velocity_callback(self, msg_velocity):
		if self.last_pose.header.stamp.to_sec() > 0:
			delta_t = (msg_velocity.header.stamp - self.last_pose.header.stamp).to_sec()
			[Delta_theta, Delta_x, Delta_y] = self.integrate(self.last_theta_dot, self.last_velocity, delta_t)
			[theta_res, x_res, y_res] = self.propagate(self.last_pose.theta, self.last_pose.x, self.last_pose.y, Delta_theta, Delta_x, Delta_y)
			
			self.last_pose.theta = theta_res
			self.last_pose.x = x_res
			self.last_pose.y = y_res
			
			msg_pose = Pose2D()
			msg_pose.header = msg_velocity.header
			msg_pose.header.frame_id = self.vehicle_name
			msg_pose.theta = theta_res
			msg_pose.x = x_res
			msg_pose.y = y_res
			self.pub_pose.publish(msg_pose)
		
		self.last_pose.header.stamp = msg_velocity.header.stamp
		self.last_theta_dot = msg_velocity.omega
		self.last_velocity = msg_velocity.v
	
	def integrate(theta_dot, v,dt):
		Delta_theta = theta_dot * dt
		if abs(theta_dot) < 0.000001:
			Delta_x = v * dt
			Delta_y = 0
		else:
			radius = v / theta_dot
			Delta_x = radius * sin(Delta_theta)
			Delta_y = radius * (1.0 - cos(Delta_theta))
		return [Delta_theta, Delta_x, Delta_y]
        
	def propagate(theta, x, y, Delta_theta, Delta_x, Delta_y):
        	theta_res = theta + Delta_theta
        	x_res = x + Delta_x * cos(theta) - Delta_y * sin(theta)
        	y_res = y + Delta_y * cos(theta) + Delta_x * sin(theta)
        	return [theta_res, x_res, y_res]
        	
if __name__ == '__main__':
		rospy.init_node('odometry_node', anonymous = True)
		position_filter_node = Odometry()
		rospy.spin()
