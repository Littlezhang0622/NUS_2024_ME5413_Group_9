#!/usr/bin/env python3
# coding:utf-8
import rospy
from std_msgs.msg import Float32MultiArray
from geometry_msgs.msg import PoseStamped

rospy.init_node('trans_cam_node', anonymous=True)

last_value = None  # Initialize the last received value


def callback(data):
    global last_value
    if data.data:
        last_value = data.data


def publish_at_fixed_frequency():
    global last_value
    box_position_publisher = rospy.Publisher('/2d_goal', PoseStamped, queue_size=1)
    rate = rospy.Rate(5)  # 10Hz, adjust as needed

    while not rospy.is_shutdown():
        if last_value:  # If there's new data
            if len(last_value) >= 8:
                x = last_value[9]
                y = last_value[10]
                current_x = 13.5
                current_y = 2.1
                map_x = current_x - (x - 320) * 0.0137248
                map_y = current_y + (y - 256) * 0.0137248 - 3

                custom_box_position = PoseStamped()
                custom_box_position.header.stamp = rospy.Time.now()
                custom_box_position.header.frame_id = "map"
                custom_box_position.pose.position.x = map_x
                custom_box_position.pose.position.y = map_y
                custom_box_position.pose.position.z = 0.0
                custom_box_position.pose.orientation.x = 0.0
                custom_box_position.pose.orientation.y = 0.0
                custom_box_position.pose.orientation.z = 0.0
                custom_box_position.pose.orientation.w = 1.0

                box_position_publisher.publish(custom_box_position)
        else:  # If no new data, publish the last received data
            if last_value is not None:  # If there's any previous data
                box_position_publisher.publish(custom_box_position)
        rate.sleep()


if __name__ == '__main__':
    rospy.Subscriber('/objects_2d', Float32MultiArray, callback)
    publish_at_fixed_frequency()
