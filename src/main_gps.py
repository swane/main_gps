#!/usr/bin/env python


import rospy
from std_msgs.msg import String
from math import pi, sin, cos, tan, sqrt, atan2
from geometry_msgs.msg import Twist
from ar_gps.msg import GPS_data

fE=0
fN=0
fB=0

goal_N=5848199.0
goal_E=538479.0
def callback(data):
    global fE
    global fN
    global fB

    rospy.loginfo(data.UTM_lat)
    rospy.loginfo(data.UTM_lon)
    rospy.loginfo(data.bearing) 
    fE=data.UTM_lon
    fN=data.UTM_lat
    fB=data.bearing
  # rospy.loginfo(hello_str)

def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'talker' node so that multiple talkers can
    # run simultaneously.
    rospy.Subscriber("argpschatter", GPS_data, callback)
    rospy.init_node('main_gps',anonymous=False)
    #rospy.on_shutdown(self.shutdown)
    #self.cmd_vel=rospy.Publisher('cmd_vel',Twist,queue_size=5)
    #rate=5
    #r=rospy.Rate(rate)


    # spin() simply keeps python from exiting until this node is stopped
    #rospy.spin()

def dist_bearing(StN,StE,EnN,EnE):
	dist=sqrt(((EnN-StN)*(EnN-StN))+((EnE-StE)*(EnE-StE)))
	bearing=atan2((EnE-StE),(EnN-StN))
	bearing=bearing*57.29578
	if bearing<0:
		bearing=360+bearing
	return (dist, bearing)

def seek_point():
	
	#Read the GPS location from the subscription
	dist, goalbearing=dist_bearing(fN,fE,goal_N,goal_E)
	print "Hello, I'm at: %f, %f, dist=%f, bearing=%f, goal bearing:%f" % (fE, fN, dist, fB,goalbearing)
	p = rospy.Publisher('cmd_vel', Twist)
	move_cmd=Twist()
	if dist>2:
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

	rospy.sleep(1)

def shutdown(self):
	rospy.loginfo("Stopping the robot...")
	self.cmd_vel.publish(Twist())

if __name__ == '__main__':
	listener()
	while True:
		seek_point()




