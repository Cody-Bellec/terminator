#!/usr/bin/env python3
# adapted from http://wiki.ros.org/ROS/Tutorials/WritingPublisherSubscriber%28python%29

import rospy
from std_msgs.msg import Float32

class Listener:
    def __init__(self):
        rospy.Subscriber("output1", Float32, self.callback)

    def callback(self, data):
        rospy.loginfo(data.data)
    

if __name__ == '__main__':
    rospy.init_node('homework2_1', anonymous=True)
    Listener()

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


