#!/usr/bin/env python3
# coding:utf-8

# !/usr/bin/env python3
# coding:utf-8

import rospy
import tf
from find_object_2d.msg import ObjectsStamped
from geometry_msgs.msg import PoseStamped


class TfExample:
    def __init__(self):
        self.objFramePrefix = "object"
        self.targetFrameId = rospy.get_param("~target_frame_id", "/map")  # 修改为/map
        self.objFramePrefix = rospy.get_param("~object_prefix", self.objFramePrefix)

        rospy.init_node("get_pose_node")
        self.tf_listener = tf.TransformListener()
        self.subs = rospy.Subscriber("objectsStamped", ObjectsStamped, self.objects_detected_callback)

    def objects_detected_callback(self, msg):
        if msg.objects.data:
            target_frame_id = self.targetFrameId if self.targetFrameId else msg.header.frame_id
            multi_sub_id = 'b'
            previous_id = -1
            for i in range(0, len(msg.objects.data), 12):
                id = int(msg.objects.data[i])
                multi_suffix = "_{}".format(multi_sub_id) if id == previous_id else ""
                multi_sub_id = chr(ord(multi_sub_id) + 1) if id == previous_id else 'b'
                previous_id = id

                object_frame_id = "{}_{}{}".format(self.objFramePrefix, id, multi_suffix)
                try:
                    (trans, rot) = self.tf_listener.lookupTransform(target_frame_id, object_frame_id, msg.header.stamp)
                    rospy.loginfo("{} [x,y,z] [x,y,z,w] in \"{}\" frame: [{},{},{}] [{},{},{},{}]".format(
                        object_frame_id, target_frame_id, trans[0], trans[1], trans[2], rot[0], rot[1], rot[2], rot[3]))

                    # send map coordinate to goal
                    self.send_goal(trans[0], trans[1], rot[2])

                except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException) as ex:
                    rospy.logwarn(str(ex))
                    continue

    def send_goal(self, x, y, z):
        # create publisher
        pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=10)

        goal = PoseStamped()
        goal.header.stamp = rospy.Time.now()
        goal.header.frame_id = "map"
        goal.pose.position.x = x
        goal.pose.position.y = y
        goal.pose.orientation.z = z
        goal.pose.orientation.x = 0
        goal.pose.orientation.y = 0
        goal.pose.orientation.z = 0
        goal.pose.orientation.w = 1
        # publish goal
        pub.publish(goal)

        # wait 1 sec
        rospy.sleep(1)


if __name__ == '__main__':
    TfExample()
    rospy.spin()

