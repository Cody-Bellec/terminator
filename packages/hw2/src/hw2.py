#!/usr/bin/env python3
# Adapted from http://wiki.ros.org/ROS/Tutorials/WritingPublisherSubscriber%28python%29

import rospy
from std_msgs.msg import Float32

class Talker:
    def __init__(self):
        self.pub = rospy.Publisher('input', Float32, queue_size=10)
    
    def talk(self):
        hello_str = rospy.get_time()
        self.pub.publish(hello_str)
    
if __name__ == '__main__':
    try:
        t = Talker()
        rospy.init_node('talker', anonymous=True)
        rate = rospy.Rate(1) # 1hz
        while not rospy.is_shutdown():
            t.talk()
            rate.sleep()
    except rospy.ROSInterruptException:
        pass


