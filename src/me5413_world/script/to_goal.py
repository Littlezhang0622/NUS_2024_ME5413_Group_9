#!/usr/bin/env python3
# coding:utf-8

import rospy
from geometry_msgs.msg import PoseStamped


def goal_callback(msg):
    global goal_msg
    goal_msg = msg


def publish_goal():
    rospy.init_node('to_goal_node', anonymous=True)

    rospy.Subscriber('/2d_goal', PoseStamped, goal_callback)

    goal_publisher = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=10)
    rospy.sleep(1)

    goal_publisher.publish(goal_msg)
    rospy.loginfo("Goal published")


if __name__ == '__main__':
    try:
        publish_goal()
    except rospy.ROSInterruptException:
        pass
