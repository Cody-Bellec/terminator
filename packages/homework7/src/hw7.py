#!/usr/bin/env python3

import sys
import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

class ImageProcess:
    def __init__(self):
        # Instatiate the converter class once by using a class member
        self.bridge = CvBridge()
        rospy.Subscriber("/image", Image, self.processing)
        self.pubcrop = rospy.Publisher("/image_cropped", Image, queue_size=10)
        self.pubw = rospy.Publisher("/image_white", Image, queue_size=10)
        self.puby = rospy.Publisher("/image_yellow", Image, queue_size=10)
        
    def processing(self, msg):
    
        #cut off top half
        cv_image1 = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        height = cv_image1.shape[0]
        width = cv_image1.shape[1]
        cropped = cv_image1[int(height/2):height, 0:width]
        roscropped = self.bridge.cv2_to_imgmsg(cropped, "bgr8")
        self.pubcrop.publish(roscropped)
        #
        
        
        
        cv2cropped = cv2.cvtColor(cropped, cv2.COLOR_BGR2HSV)
        w_filter = cv2.inRange(cv2cropped, (40,0,240),(180,255,255))
        wf = self.bridge.cv2_to_imgmsg(w_filter, "mono8")
        self.pubw.publish(wf)
        #w-filtering
        
        
        
        
        y_filter = cv2.inRange(cv2cropped, (20, 100, 100),(180,255,255))
        yf = self.bridge.cv2_to_imgmsg(y_filter, "mono8")
        self.puby.publish(yf)
        #y-filtering
        

if __name__=="__main__":
    # initialize node and create a publisher
    rospy.init_node("homework7", anonymous=True)
    img_flip = ImageProcess()
    rospy.spin()
