#!/usr/bin/env python3

import sys
import rospy
import cv2
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

class ImageProcess:

    global orig
    global img1
    
    def __init__(self):
        
        # Instatiate the converter class once by using a class member
        self.bridge = CvBridge()
        rospy.Subscriber("/image_cropped", Image, self.processlines)		#subscribe to cropped images
        rospy.Subscriber("/image_white", Image, self.whitelines)
        rospy.Subscriber("/image_yellow", Image, self.yellowlines)
        
        self.pubw = rospy.Publisher("/image_lines_white", Image, queue_size=10)
        self.puby = rospy.Publisher("/image_lines_yellow", Image, queue_size=10)
        #self.pubcrop = rospy.Publisher("/image_cropped", Image, queue_size=10)
        #self.pubw = rospy.Publisher("/image_white", Image, queue_size=10)
        #self.puby = rospy.Publisher("/image_yellow", Image, queue_size=10)
        
    def output_lines(self, original_image, lines):
        output = np.copy(original_image)
        if lines is not None:
            for i in range(len(lines)):
                l = lines[i][0]
                cv2.line(output, (l[0],l[1]), (l[2],l[3]), (255,0,0), 2, cv2.LINE_AA)
                cv2.circle(output, (l[0],l[1]), 2, (0,255,0))
                cv2.circle(output, (l[2],l[3]), 2, (0,0,255))
        return output
        
    def processlines(self, msg):
        #make lines
        global orig
        global img1
        cv_img1 = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        
        orig = cv_img1
        Gauss = cv2.GaussianBlur(cv_img1,(5,5), 0)
        Gauss = cv2.Sobel(Gauss,cv2.CV_8U,1,0)
        cvimg1 = cv2.Sobel(Gauss,cv2.CV_8U,0,1)

        img1 = cv2.Canny(cvimg1, 1, 10)
        
        
        #output edges
        
    def whitelines(self, msg):
        global orig
        global img1
        cv_img1 = self.bridge.imgmsg_to_cv2(msg, "mono8")
        #orig = cv_img1
        
        #prep for Hough
        #Gauss = cv2.GaussianBlur(cv_img1,(5,5), 0)
        #Gauss = cv2.Sobel(Gauss,cv2.CV_8U,1,0)
        #cvimg1 = cv2.Sobel(Gauss,cv2.CV_8U,0,1)
        #img1 = cv2.Canny(cvimg1, 1, 10)
        
        #cvim = bitwise and cv_img1 with img1
        cvim = cv2.bitwise_and(cv_img1, img1)
        lines1 = cv2.HoughLinesP(cvim,rho = 1,theta = 1*np.pi/180,threshold = 1,minLineLength = 1,maxLineGap = 1)
        out = self.output_lines(orig, lines1)
        output = self.bridge.cv2_to_imgmsg(out, "bgr8")
        self.pubw.publish(output)
        #output output
    
    def yellowlines(self, msg):
        global orig
        global img1
        cv_img2 = self.bridge.imgmsg_to_cv2(msg, "mono8")
        #orig = cv_img2
        
        #cvim = bitwise and cv_img2 with img1
        cvim = cv2.bitwise_and(cv_img2, img1)
        lines2 = cv2.HoughLinesP(cvim,rho = 1,theta = 1*np.pi/180,threshold = 1,minLineLength = 1,maxLineGap = 1)
        out = self.output_lines(orig, lines2)
        output = self.bridge.cv2_to_imgmsg(out, "bgr8")
        self.puby.publish(output)
        #self.pubyellow.publish(output)
        #output output
        

if __name__=="__main__":
    # initialize our node and create a publisher as normal
    rospy.init_node("hw7", anonymous=True)
    img_flip = ImageProcess()
    rospy.spin()
