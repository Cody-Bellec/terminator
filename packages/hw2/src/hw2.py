#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float32

class Homework1:
    def __init__(self):
        rospy.Subscriber("output1", Float32, self.callback)
        self.pub = rospy.Publisher("input", Float32, queue_size=10)
        self.total = 0

    def callback(self, data):
        self.total += data.data
        self.pub.publish(self.total)

if __name__ == '__main__':
    rospy.init_node('hw2')
    hw2()

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

