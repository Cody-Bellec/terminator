#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float32
from mystery_package.msg import UnitsLabelled

class Homework3:
    def __init__(self):
        rospy.Subscriber("output2", Units Labelled, self.callback)
        self.pub = rospy.Publisher("/homework3/converted_total", Float32, queue_size=10)
    def callback(self, data):
        		
        if rospy.has_param("value"):
            self.mode = rospy.get_param("value")
        else:
            self.mode = 'meters'
    			
        if self.mode == 'smoots':
            turnout = data.data * 1.7018
        elif self.mode == 'feet':
            turnout = data.data
        else:
            turnout = data.data * 3.2808
		
            self.pub.publish(turnout)
            rospy.loginfo("input data: %lf feet. output data: %lf %s", data.data, turnout, self.mode)
        if rospy.has_param("value"):
            rospy.has_param("value", self.mode)
        else:
            rospy.logwarn("No parameter mode found!")
		
if __name__ == '__main__':
	rospy.init_node('homework3', anonymous=True)
	Homework3()

    # spin() simply keeps python from exiting until this node is stopped
	rospy.spin()
