#!/usr/bin/env python3
import rospy
from akif_package.msg import OdevSensor
import math

def robot_status_callback(msg):
    rospy.loginfo(f"Received Robot Status: x={msg.x}, y={msg.y}, velocity={msg.velocity}")
    rospy.loginfo(f"Target Position: ({msg.target_x}, {msg.target_y})")

    # Robotun hedefe olan uzaklığını hesapla
    distance_to_target = math.sqrt((msg.target_x - msg.x) ** 2 + (msg.target_y - msg.y) ** 2)
    rospy.loginfo(f"Distance to Target: {distance_to_target:.2f} meters")

    if distance_to_target < 0.5:
        rospy.loginfo("Target reached!")
    else:
        rospy.loginfo("Moving towards target...")

# Düğüm başlatma
rospy.init_node('robot_subscriber_node', anonymous=True)

# Abonelik oluşturma
rospy.Subscriber('robot_status_topic', OdevSensor, robot_status_callback)

# Düğümün sürekli çalışmasını sağla
rospy.spin()

