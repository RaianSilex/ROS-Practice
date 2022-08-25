import rospy
from std_msgs.msg import String

def pub():
	pub = rospy.Publisher('str_topic', String, queue_size = 10)
	rospy.init_node('pub', anonymous=True)
	rate = rospy.Rate(0.5)
	while not rospy.is_shutdown():
		strmsg = "Y"
		pub.publish(strmsg)
		rate.sleep()


if __name__ == '__main__':
	try:
		pub()
	except rospy.ROSInterruptException:
		pass