#!/usr/bin/env python
import roslib

import rospy
from std_msgs.msg import Float64
import dynamixel_msgs.msg
import sensor_msgs.msg

class dynamixelState:
    def __init__(self):
        self.pub = rospy.Publisher('/neckHead/state', sensor_msgs.msg.JointState, queue_size=1)
        self.sub = rospy.Subscriber('/neckHead_controller/state', dynamixel_msgs.msg.JointState, self.callback)
        self.msg = sensor_msgs.msg.JointState()
	self.msg.name.append(0)
        self.msg.velocity.append(0)
        self.msg.position.append(0)
        self.msg.effort.append(0)

    def callback(self, data):
        self.msg.name[0] = data.name
        self.msg.position[0] = data.current_pos
        self.msg.velocity[0] = data.velocity
        self.msg.effort[0] = 0

    def publish(self):
        self.pub.publish(self.msg)

def main():
    rospy.init_node('dynamixel_publisher')
    rate = rospy.Rate(10)  # 10hz
    neckHeadDynamixel = dynamixelState()
    while not rospy.is_shutdown():
        neckHeadDynamixel.publish()
        rate.sleep()

if __name__ == '__main__':
    main()
