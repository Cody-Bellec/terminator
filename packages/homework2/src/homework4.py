#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float32
from homework2.msg import hw4

class Homework4:
    def __init__(self):
        rospy.Subscriber("/homework1/total", Float32, self.callback)
        self.pub = rospy.Publisher("hw4_msg", hw4, queue_size=10)
        turnout = 0 
        data.data = 0
    def callback(self, data):
		
        if rospy.has_param("unit_holder"):
            self.mode = rospy.get_param("unit_holder")
        else:
            self.mode = 'meters'
    			
        if self.mode == 'smoots':
            turnout = data.data * 1.7018
        elif self.mode == 'feet':
            turnout = data.data
        else:
            turnout = data.data * 3.2808

        message = hw4()
        message.unit_holder = self.mode
        message.c = turnout
        		
        self.pub.publish(msg)
        rospy.loginfo(msg)
       	
if __name__ == '__main__':
	rospy.init_node('homework4', anonymous=True)
	Homework4()

    # spin() simply keeps python from exiting until this node is stopped
	rospy.spin()
