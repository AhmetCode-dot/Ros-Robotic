#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class ObstacleAvoidance:
    def __init__(self):
        rospy.init_node('duvara_gitme', anonymous=True)
        self.cmd_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.scan_sub = rospy.Subscriber('/scan', LaserScan, self.scan_callback)
        self.twist = Twist()
        self.safe_distance = 0.5  # Güvenli mesafe (metre cinsinden)

    def scan_callback(self, scan_data):
        # LIDAR verilerini işleme
        ranges = scan_data.ranges
        # En yakın mesafeyi bul
        min_distance = min(ranges)
        angle_to_wall = ranges.index(min_distance)

        # Duvara yönelme
        if min_distance > self.safe_distance:
            self.twist.linear.x = 0.2  # Duvara doğru hareket et
            self.twist.angular.z = self.angle_correction(angle_to_wall)  # Açı düzeltme
        else:
            self.twist.linear.x = 0.0  # Duvara yaklaşıldığında dur
            self.twist.angular.z = 0.0  # Dönmeyi durdur

        self.cmd_pub.publish(self.twist)

    def angle_correction(self, angle):
        # LIDAR'dan gelen açıya göre düzeltme yapma
        # (LIDAR açısal aralığı genellikle 360 derece)
        # Bu kısmı daha hassas hale getirebilirsiniz
        return (angle - len(range(360)) / 2) * 0.01  # Açı düzeltme faktörü

    def run(self):
        rospy.spin()

if __name__ == '__main__':
    try:
        ObstacleAvoidance().run()
    except rospy.ROSInterruptException:
        pass

