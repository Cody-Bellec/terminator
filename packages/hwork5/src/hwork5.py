#!/usr/bin/env python3

from math import radians, sin, cos
import numpy
import rospy
from duckietown_msgs.msg import Vector2D

class Listener:
    def _init_(self):
        self.sub = rospy.Subscriber('/input_vector', Vector2D,self.callback)
        self.pub = rospy.Publisher('/world_vector', Vector2D, queue_size=10)
        self.pub = rospy.Publisher('/bot_vector' , Vector2D, queue_size=10)


        robot = numpy.matrix([[(-sqrt(2)/2),(-sqrt(2)/2),2],[(sqrt(2)/2),(-sqrt(2)/2),7],[0,0,1]])
        sensor = numpy.matrix([[-1,0,-2],[0,-1,0],[0,0,1]])
        x = input("enter x coordinate:")
        y = input ("enter y coordinate:")
    def callback_function(self,msg):
        v = [[x],[y],[1]]
        bot_coor_v = sensor * v
        wrld_coor_v = robot * v
        
        self.pub.publisher(bot_coor_v)
        print("robot coordinates:")
        self.pub.publisher(wrld_coor_v)
        print("wrld coordinates:")
if __name__=='__main__':
    rospy.init_node('listener',anonymous=True)
    Listener()


    rospy.spin()
