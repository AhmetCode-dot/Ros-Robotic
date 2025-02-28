#!/usr/bin/env python3
import rospy
import os
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class ObstacleAvoidance:
    def __init__(self):
        rospy.init_node('obstacle_avoidance', anonymous=True)
        self.cmd_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.scan_sub = rospy.Subscriber('/scan', LaserScan, self.scan_callback)
        self.twist = Twist()
        self.safe_distance = 0.5  # Güvenli mesafe (metre)
        self.rate = rospy.Rate(10)  # 10 Hz

        # Harita kaydetme ve süre kontrolü
        self.map_saved = False  # Haritanın kaydedilip kaydedilmediğini kontrol eder
        self.start_time = rospy.Time.now()  # Başlangıç zamanı

    def scan_callback(self, scan_data):
        # LIDAR verisini işleme
        ranges = scan_data.ranges
        front = min(min(ranges[:30]), min(ranges[-30:]))  # Ön taraf mesafesi
        left = min(ranges[60:120])  # Sol taraf mesafesi
        right = min(ranges[240:300])  # Sağ taraf mesafesi

        # Engel algılama ve hareket
        if front < self.safe_distance:
            self.twist.linear.x = 0.0  # Dur
            self.twist.angular.z = 0.5 if left > right else -0.5  # Dön
        else:
            self.twist.linear.x = 0.2  # İleri hareket
            self.twist.angular.z = 0.0  # Dönüş yok

        self.cmd_pub.publish(self.twist)

    def save_map(self):
        """Haritayı kaydet."""
        if not self.map_saved:  # Haritanın yalnızca bir kez kaydedilmesini sağlar
            rospy.loginfo("Harita kaydediliyor...")
            os.system("rosrun map_server map_saver -f ~/rgiriss_ws/src/final_odev/src/map")
            rospy.loginfo("Harita kaydedildi.")
            self.map_saved = True
            self.stop_robot()  # Robotu durdur

    def stop_robot(self):
        """Robotu durdur."""
        rospy.loginfo("Robot durduruluyor.")
        self.twist.linear.x = 0.0
        self.twist.angular.z = 0.0
        self.cmd_pub.publish(self.twist)
        rospy.signal_shutdown("Görev tamamlandı ve robot durduruldu.")

    def run(self):
        rospy.loginfo("Engelden kaçınma başlatıldı.")
        while not rospy.is_shutdown():
            current_time = rospy.Time.now()
            elapsed_time = (current_time - self.start_time).to_sec()  # Geçen süreyi hesapla

            # Eğer 165 saniye (2dk 45sn) geçtiyse ve harita henüz kaydedilmediyse
            if elapsed_time >= 85.0 and not self.map_saved:
                self.save_map()

            self.rate.sleep()

if __name__ == '__main__':
    try:
        obstacle_avoidance = ObstacleAvoidance()
        obstacle_avoidance.run()
    except rospy.ROSInterruptException:
        pass

