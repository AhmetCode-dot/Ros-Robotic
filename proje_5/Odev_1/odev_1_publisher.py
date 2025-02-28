#!/usr/bin/env python3
import rospy
from akif_package.msg import OdevSensor  # Doğru import
import random

# Publisher oluşturma
pub = rospy.Publisher('robot_status_topic', OdevSensor, queue_size=10)

# Düğüm başlatma
rospy.init_node('robot_publisher_node', anonymous=True)

# Yayım frekansı
rate = rospy.Rate(1)  # 1 Hz

while not rospy.is_shutdown():
    # Robotun durum bilgilerini içeren mesaj oluşturma
    robot_status = OdevSensor()
    robot_status.x = random.uniform(0, 10)  # X pozisyonu
    robot_status.y = random.uniform(0, 10)  # Y pozisyonu
    robot_status.velocity = random.uniform(0, 5)  # Hız

    # Hedef koordinatlarını belirleme
    robot_status.target_x = 10.0
    robot_status.target_y = 10.0

    # Yayınlanan verileri log ile göster
    rospy.loginfo(f"Publishing Robot Status: x={robot_status.x}, y={robot_status.y}, velocity={robot_status.velocity}")
    pub.publish(robot_status)
    rate.sleep()

