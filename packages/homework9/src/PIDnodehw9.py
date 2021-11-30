#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float32
from PIDclasshw5 import PID

class hw5_node:
    def __init__(self):
        global remote
        remote = PID(30,20)
        remote.changeGainz(0.5,0,1.58)
        
        if rospy.has_param("/controller_ready"):
            rospy.set_param("/controller_ready", 'true')       
    
        rospy.Subscriber("/controls_hw/error", Float32, self.recall)
        self.pub = rospy.Publisher('/controls_hw/control_input', Float32, queue_size=10)
        
    def recall(self, value):
        self.signal = remote.calc(value.data)
        if value.data < 0.2:
            if value.data >- 0.2:
                self.signal = 0
        self.pub.publish(self.signal)

if __name__ == '__main__':
    rospy.init_node('PIDnodehw5', anonymous=True)
    hw5_node()

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
