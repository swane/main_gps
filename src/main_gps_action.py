#!/usr/bin/env python


import rospy
from std_msgs.msg import String
from math import pi, sin, cos, tan, sqrt, atan2
from geometry_msgs.msg import Twist
import actionlib
from main_gps.msg import PlaceAction,PlaceGoal,PlaceResult,PlaceFeedback

fE=0
fN=0
fB=0


def dist_bearing(StN,StE,EnN,EnE):
	dist=sqrt(((EnN-StN)*(EnN-StN))+((EnE-StE)*(EnE-StE)))
	bearing=atan2((EnE-StE),(EnN-StN))
	bearing=bearing*57.29578
	if bearing<0:
		bearing=360+bearing
	return (dist, bearing)

def seek_point(goal):
	while(goal.distance>5):
		feedback=PlaceFeedback()
		feedback.current_N=fN
		feedback.current_N=fE
		server.publish_feedback(feedback)
		update_count+=1

		
		#Read the GPS location from the subscription
		dist, goalbearing=dist_bearing(fN,fE,goal_N,goal_E)
		print "Hello, I'm at: %f, %f, dist=%f, bearing=%f, goal bearing:%f" % (fE, fN, dist, fB,goalbearing)
		p = rospy.Publisher('cmd_vel', Twist)
		move_cmd=Twist()
		if dist>5:
			linear_speed=2
		else:
			linear_speed=0
		rotation_speed=fB-goalbearing
		if rotation_speed>5:
			rotation_speed=5
		if rotation_speed<-5:
			rotation_speed=-5

	    	move_cmd.linear.x=linear_speed
	    	move_cmd.angular.z=rotation_speed
	    	p.publish(move_cmd)

		time.sleep(1.0)
	result=PlaceResult()
	result.actual_N=fN
	result.actual_E=fE
	result.actual_dist=dist
	server.set_succeeded(result,"Within 5m of location")

def shutdown(self):
	rospy.loginfo("Stopping the robot...")
	self.cmd_vel.publish(Twist())

#rospy.Subscriber("argpschatter", GPS_data, callback)
rospy.init_node('main_gps',anonymous=False)
server=actionlib.SimpleActionServer('timer',PlaceAction,seek_goal,False)
server.start()
rospy.spin()


