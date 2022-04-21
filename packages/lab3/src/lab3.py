#!/usr/bin/env python3

import sys
import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import numpy as np

class ImageProcess:

	global orig
	global img1	
		
	def __init__(self):
		# Instatiate the converter class once by using a class member
		self.bridge = CvBridge()
		rospy.Subscriber("/doczy/camera_node/image/compressed", CompressedImage, self.output_lines, queue_size=1, buff_size=2**24)
		self.pubw = rospy.Publisher("/image_lines_white", Image, queue_size=10)
		self.puby = rospy.Publisher("/image_lines_yellow", Image, queue_size=10)
		#self.pubcrop = rospy.Publisher("/image_cropped", Image, queue_size=10)
		#self.pubw = rospy.Publisher("/image_white", Image, queue_size=10)
		#self.puby = rospy.Publisher("/image_yellow", Image, queue_size=10)
        
        
	def output_lines(self, original_image, lines, msg):
		output = np.copy(original_image)
		if lines is not None:
			for i in range(len(lines)):
				l = lines[i][0]
				cv2.line(output, (l[0],l[1]), (l[2],l[3]), (255,0,0), 2, cv2.LINE_AA)
				cv2.circle(output, (l[0],l[1]), 2, (0,255,0))
				cv2.circle(output, (l[2],l[3]), 2, (0,0,255))
		return output
		
		#make lines and cut off top half
		global orig
		global img1
		cv_img1 = self.bridge.imgmsg_to_cv2(msg, "bgr8")
		height = cv_image1.shape[0]
		width = cv_image1.shape[1]
		cropped = cv_image1[int(height/2):height, 0:width]
		roscropped = self.bridge.cv2_to_imgmsg(cropped, "bgr8")
		self.pubcrop.publish(roscropped)
		
		orig = cv_img1
		Gauss = cv2.GaussianBlur(cv_img1,(5,5), 0)
		Gauss = cv2.Sobel(Gauss,cv2.CV_8U,1,0)
		cvimg1 = cv2.Sobel(Gauss,cv2.CV_8U,0,1)
		
		img1 = cv2.Canny(cvimg1, 1, 10)
		
		#White
		#White Filtering
		cv2cropped = cv2.cvtColor(cropped, cv2.COLOR_BGR2HSV)
		w_filter = cv2.inRange(cv2cropped, (40,0,240), (180,255,255))
		wf = self.bridge.cv2_to_imgmsg(w_filter, "mono8")
		self.pubw.publish(wf)
		
		#White Lines
		cvim = cv2.bitwise_and(cv_img1, img1)
		lines1 = cv2.HoughLinesP(cvim,rho = 1,theta = 1*np.pi/180, threshold = 1,minLineLength = 1,maxLineGap = 1)
		out = self.output_lines(orig, lines1)
		outputw = self.bridge.cv2_to_imgmsg(out, "bgr8")
		self.pubw.publish(outputw)
		
		#Yellow
		#Yellow Filtering
		y_filter = cv2.inRange(cv2cropped, (20,100,100), (180,255,255))
		yf = self.bridge.cv2_to_imgmsg(y_filter, "mono8")
		self.puby.publish(yf)
		
		#Yellow Lines
		cvim = cv2.bitwise_and(cv_img2, img1)
		lines2 = cv2.HoughLinesP(cvim,rho = 1,theta = 1*np.pi/180,threshold = 1,minLineLength = 1,maxLineGap = 1)
		out = self.output_lines(orig, lines2)
		outputy = self.bridge.cv2_to_imgmsg(out, "bgr8")
		self.puby.publish(outputy)

if __name__=="__main__":
	# initialize our node and create a publisher as normal
	rospy.init_node("lab3", anonymous=True)
	img_flip = ImageProcess()
	rospy.spin()
