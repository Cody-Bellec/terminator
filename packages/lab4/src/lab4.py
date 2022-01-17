#!/usr/bin/env python3

import rospy
import math 
import time
from duckietown_msgs.msg import WheelsCmdStamped


class lab4:
        
    def __init__(self):
        global x
        global y
        global theta
        global oldt
        global oldwheeldat
        
        oldwheeldat = WheelsCmdStamped()
        
        x = y = theta = 0
       
        oldt = time.time()
        
        rospy.Subscriber("/canard/wheels_driver_node/wheels_cmd", WheelsCmdStamped, self.callback)
    
    def calcDist(self, dt, wheel):
        #use conversion to calculate distance based on v and t
        dist = dt * (wheel/0.047752) * 0.02857
        return dist
        
    def callback(self, wheeldat):
        
        global x, y, theta, oldt
        global oldwheeldat
        
        #calculate dt
        newt = time.time()
        dt = newt - oldt
        oldt = newt
    
        dR = self.calcDist(dt, oldwheeldat.vel_right)
        dL = self.calcDist(dt, oldwheeldat.vel_left)
        oldwheeldat = wheeldat
        
        #use wheeldat left and right to calculate new angle and position based on old 
        ds = (dL + dR)/2
        dtheta = (dR - dL)/(0.1)
        deltax = ds * math.cos(theta + dtheta/2)
        deltay = ds * math.sin(theta + dtheta/2)
        theta = theta + dtheta
        x = x + deltax
        y = y + deltay
        
        rospy.logwarn("x = %lf, y = %lf, theta = %lf", x,y,theta)


if __name__ == '__main__':
    rospy.init_node('lab4', anonymous=True)
    lab4()
    rospy.spin()
