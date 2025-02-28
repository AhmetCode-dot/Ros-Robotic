#!/usr/bin/env python3
import rospy
from nav_msgs.msg import Odometry
import math

class YolNode:
    def __init__(self):
        # ROS düğümünü başlat
        rospy.init_node('yol', anonymous=True)
        
        # Odometre topiğine abone ol
        self.sub = rospy.Subscriber('/odom', Odometry, self.odom_callback)
        
        # Başlangıç pozisyonu
        self.initial_x = None
        self.initial_y = None
        self.distance_traveled = 0.0

    def odom_callback(self, msg):
        # Pozisyon bilgilerini al
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y

        # Başlangıç pozisyonunu ilk veri geldiğinde ayarla
        if self.initial_x is None or self.initial_y is None:
            self.initial_x = x
            self.initial_y = y

        # X ve Y eksenlerinde gidilen toplam mesafeyi hesapla
        delta_x = x - self.initial_x
        delta_y = y - self.initial_y
        distance = math.sqrt(delta_x**2 + delta_y**2)

        # Toplam mesafeyi güncelle
        self.distance_traveled = distance
        
        # Anlık pozisyonu ve mesafeyi logla
        rospy.loginfo(f"Anlık Pozisyon - X: {delta_x:.2f}, Y: {delta_y:.2f}, Toplam Mesafe: {self.distance_traveled:.2f} m")

    def run(self):
        rospy.spin()

if __name__ == '__main__':
    try:
        yol_node = YolNode()
        yol_node.run()
    except rospy.ROSInterruptException:
        pass

