#!/usr/bin/env python3
import rospy
import actionlib
from example_service.srv import *
import example_action_server.msg


def SC(n):
	rospy.logwarn("SCTest1")
	Stime = rospy.get_time()
	rospy.wait_for_service('calc_fibonacci')
	try:
		Fibonacci = rospy.ServiceProxy('calc_fibonacci', Fibonacci)
		NPower = Fibonacci(n)
		Stime2 = rospy.get_time()
		rospy.loginfo("Service time for " +str(n) +" request is " +str(Stime2-Stime))
		return NPower.sequence
	except rospy.ServiceException as e:
		print("Service call failure %s " %e)
	        
        
def AC(n):
	CL = actionlib.SimpleActionClient('fibonacci', example_action_server.msg.FibonacciAction)
	CL.wait_for_server()
	FGoal = example_action_server.msg.FibonacciGoal(order=n)

	ACtime1 = rospy.get_time()
	client.send_goal(FGoal)
	ACtime2 = rospy.get_time()
	client.wait_for_result()
	ACtime3 = rospy.get_time()
	rospy.logwarn("SCTest2")
	
	time_sending = ACtime2 - ACtime1
	rospy.logwarn("Action for " +str(n)+ "the send time is " +str(time_sending))
	waiting_time = ACtime3 - ACtime2
	rospy.logwarn("Action" +str(n)+ "the wait time is " +str(waiting_time))
	rospy.logwarn("SCTest3")
	
	return client.get_result()

    
if __name__=="__main__":
    rospy.init_node('hw10')
    rospy.logwarn("SCTest4")
    SCOrder3 = SC(3)
    rospy.logwarn("Service Order 3 is " +str(SCOrder3))
    SCOrder15= SC(15)
    rospy.logwarn("Service Order 15 is " +str(SCOrder15))
    ACOrder3 = AC(3)
    rospy.logwarn("Action order 3 is " +str(ACOrder3))
    ACOrder15 = AC(15)
    rospy.logwarn("Action order 15 is " +str(ACOrder15))
    rospy.logwarn("SCTest5")
    
