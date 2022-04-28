#!/usr/bin/env python3

import sys
import rospy
import cv2
from std_msgs.msg import Header
from duckietown_msgs.msg import SegmentList, Segment
from sensor_msgs.msg import CompressedImage, Image
from cv_bridge import CvBridge
from  
import numpy as np

class ImageProcess:

	global orig
	global img1	
		
	def __init__(self):
		# Instatiate the converter class once by using a class member
		self.bridge = CvBridge()
		rospy.Subscriber("/doczy/camera_node/image/compressed", CompressedImage, self.callback, queue_size=1, buff_size=2**24)
		self.pub = rospy.Publisher("/image_cropped", Image, queue_size=10)
		self.hough = rospy.Publisher("/doczy/line_detector_node/segment_list", SegmentList, queue_size=10)
		#self.pubw = rospy.Publisher("/image_white", Image, queue_size=10)
		#self.puby = rospy.Publisher("/image_yellow", Image, queue_size=10)
		#self.pubw = rospy.Publisher("/image_lines_white", Image, queue_size=10)
		#self.puby = rospy.Publisher("/image_lines_yellow", Image, queue_size=10)
        
        
	def output_lines(self, original_image, lines):
		output = np.copy(original_image)
		if lines is not None:
			for i in range(len(lines)):
				l = lines[i][0]
				cv2.line(output, (l[0],l[1]), (l[2],l[3]), (255,0,0), 2, cv2.LINE_AA)
				cv2.circle(output, (l[0],l[1]), 2, (0,255,0))
				cv2.circle(output, (l[2],l[3]), 2, (0,0,255))
		return output
		
	def callback(self, msg):
		#cut off top half
		cv_img1 = self.bridge.compressed_imgmsg_to_cv2(msg, "bgr8")
		
		image_size = (160, 120)
		offset = 40
		new_image = cv2.resize(cv_img1, image_size, interpolation=cv2.INTER_NEAREST)
		cropped = new_image[offset:, :]
        
		#line processing
		orig = cropped
		Gauss = cv2.GaussianBlur(cropped,(5,5), 0)
		Gauss = cv2.Sobel(Gauss,cv2.CV_8U,1,0)
		cvimg1 = cv2.Sobel(Gauss,cv2.CV_8U,0,1)
		img1 = cv2.Canny(cvimg1, 1, 10)
		
		arr_cutoff = np.array([0, offset, 0, offset])
		arr_ratio = np.array([1. / image_size[0], 1. / image_size[1], 1. / image_size[0], 1. / image_size[1]])
		
		
		#White Filtering
		cv2cropped = cv2.cvtColor(cropped, cv2.COLOR_BGR2HSV)
		w_filter = cv2.inRange(cv2cropped, (40,0,240), (180,255,255))
		
		cvim = cv2.bitwise_and(w_filter, img1)
		lines1 = cv2.HoughLinesP(cvim,rho = 1,theta = 1*np.pi/180, threshold = 1,minLineLength = 1,maxLineGap = 1)
		out1 = self.output_lines(orig, lines1)
		#self.hough.publish(line_normalized1)
		
		b = SegmentList()
		
		for points1 in lines1:
			s = Segment()
			s.color = 0
			line_normalized1 = (points1 + arr_cutoff) * arr_ratio
			#rospy.logwarn(line_normalized1)	
			s.pixels_normalized[0].x = line_normalized1[0][0]
			s.pixels_normalized[0].y = line_normalized1[0][1]
			s.pixels_normalized[1].x = line_normalized1[0][2]
			s.pixels_normalized[1].y = line_normalized1[0][3]
			b.segments.append(s)
		
		#Yellow Filtering
		y_filter = cv2.inRange(cv2cropped, (20,100,100), (180,255,255))
		
		cvim1 = cv2.bitwise_and(y_filter, img1)
		lines2 = cv2.HoughLinesP(cvim1,rho = 1,theta = 1*np.pi/180,threshold = 1,minLineLength = 1,maxLineGap = 1)
		out2 = self.output_lines(orig, lines2)
		
		for points2 in lines2:
			c = Segment()
			c.color = 0
			line_normalized2 = (points2 + arr_cutoff) * arr_ratio
			c.pixels_normalized[0].x = line_normalized2[0][0]
			c.pixels_normalized[0].y = line_normalized2[0][1]
			c.pixels_normalized[1].x = line_normalized2[0][2]
			c.pixels_normalized[1].y = line_normalized2[0][3]
			b.segments.append(c)

		self.hough.publish(b)
		
		#h = Header(stamp=rospy.Time.now(), frame_id = "base")
		#out3 = self.output_lines(orig, line_normalized1)
		#out4 = self.output_lines(orig, line_normalized2)
		
		output = cv2.bitwise_or(out1, out2)
		outputfinal = self.bridge.cv2_to_imgmsg(output, "bgr8")
		self.pub.publish(outputfinal)
		
		#output1 = cv2.bitwise_or(out3, out4)
		#outputfinal2 = self.bridge.cv2_to_imgmsg(output1, "bgr8")
		#self.hough.publish(outputfinal2)

if __name__=="__main__":
	# initialize our node and create a publisher as normal
	rospy.init_node("lab3", anonymous=True)
	img_flip = ImageProcess()
	rospy.spin()
