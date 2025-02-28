#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import math

# Global velocity_publisher
velocity_publisher = None

def duvara_git():
    global velocity_publisher
    rospy.init_node('duvara_git', anonymous=True)
    velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    scan_subscriber = rospy.Subscriber('/scan', LaserScan, callback)
    rospy.spin()

def callback(data):
    twist = Twist()
    ranges = data.ranges
    valid_ranges = [r if not math.isinf(r) else 10.0 for r in ranges]  # Sonsuz mesafeleri yok say
    
    # En yakın mesafeyi ve bu mesafenin açısını bul
    min_distance = min(valid_ranges)
    angle_to_wall = valid_ranges.index(min_distance)
    
    # Robotun dönüş yönünü belirlemek için açıyı radian cinsine çevir
    angle_to_wall_rad = (angle_to_wall - len(ranges) / 2) * (2 * math.pi / len(ranges))
    
    rospy.loginfo(f"En yakın mesafe: {min_distance:.2f} m, Açı: {math.degrees(angle_to_wall_rad):.2f} derece")
    
    # Eğer duvar 0.2 metreden uzaktaysa, hareket et
    if min_distance > 0.2:
        twist.linear.x = 0.15  # İleri hareket hızı biraz artırıldı
        twist.angular.z = -0.5 * angle_to_wall_rad  # Açısal hız azaltılarak stabilite sağlandı
    else:
        twist.linear.x = 0.0  # Dur
        twist.angular.z = 0.0
        rospy.loginfo("Robot durdu. Duvara ulaşıldı.")
        rospy.signal_shutdown("Duvara ulaşıldı.")  # Düğümü kapat

    velocity_publisher.publish(twist)

if __name__ == '__main__':
    try:
        duvara_git()
    except rospy.ROSInterruptException:
        pass

