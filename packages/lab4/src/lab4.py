#!/usr/bin/env python3

import sys
import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import numpy as np

class ImageProcess:
    def __init__(self):
        # Instatiate the converter class once by using a class member
        self.bridge = CvBridge()
        rospy.Subscriber("/canard/camera_node/image/compressed", CompressedImage, self.processing, queue_size=1, buff_size=2**24)
        self.pub = rospy.Publisher("/image_cropped", Image, queue_size=10)
        
        
    def output_lines(self, original_image, lines):
        output = np.copy(original_image)
        if lines is not None:
            for i in range(len(lines)):
                l = lines[i][0]
                cv2.line(output, (l[0],l[1]), (l[2],l[3]), (255,0,0), 2, cv2.LINE_AA)
                cv2.circle(output, (l[0],l[1]), 2, (0,255,0))
                cv2.circle(output, (l[2],l[3]), 2, (0,0,255))
        return output
        
        
    def processing(self, msg):
    
        #cut off top half
        cv_img1 = self.bridge.compressed_imgmsg_to_cv2(msg, "bgr8")
        
        
        image_size = (160, 120)
        offset = 40
        new_image = cv2.resize(cv_img1, image_size, interpolation=cv2.INTER_NEAREST)
        cropped = new_image[offset:, :]
        
        
   
        #line processing
        
        orig = croppped
        Gauss = cv2.GaussianBlur(cropped,(5,5), 0)
        Gauss = cv2.Sobel(Gauss,cv2.CV_8U,1,0)
        cvimg1 = cv2.Sobel(Gauss,cv2.CV_8U,0,1)
        img1 = cv2.Canny(cvimg1, 1, 10)
                
               
        #white filtering
        cv2cropped = cv2.cvtColor(cropped, cv2.COLOR_BGR2HSV)
        white_filtered = cv2.inRange(cv2cropped, (40,0,240),(180,255,255))
       
        cvim = cv2.bitwise_and(white_filtered, img1)
        lines1 = cv2.HoughLinesP(cvim,rho = 1,theta = 1*np.pi/180,threshold = 1,minLineLength = 1,maxLineGap = 1)
        out1 = self.output_lines(orig, lines1)
        #output = self.bridge.cv2_to_imgmsg(out, "bgr8")
        #self.pubwhite.publish(output)
       
        
        
        #yellow filtering
        yellow_filtered = cv2.inRange(cv2cropped, (20, 100, 100),(180,255,255))
        
       
        cvim1 = cv2.bitwise_and(yellow_filtered, img1)
        lines11 = cv2.HoughLinesP(cvim1,rho = 1,theta = 1*np.pi/180,threshold = 1,minLineLength = 1,maxLineGap = 1)
        out2 = self.output_lines(orig, lines11)


        
        output = cv2.bitwise_or(out1, out2)
        outputfinal = self.bridge.cv2_to_imgmsg(output, "bgr8")
        self.pub.publish(outputfinal)
        #

if __name__=="__main__":
    # initialize our node and create a publisher as normal
    rospy.init_node("lab5", anonymous=True)
    img_flip = ImageProcess()
    rospy.spin()
