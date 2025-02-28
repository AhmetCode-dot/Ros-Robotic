#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class ObstacleAvoidance:
    def __init__(self):
        rospy.init_node('obstacle_avoidance', anonymous=True)
        self.cmd_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.scan_sub = rospy.Subscriber('/scan', LaserScan, self.scan_callback)
        self.twist = Twist()
        self.safe_distance = 0.5  # Safe distance (in meters)

    def scan_callback(self, scan_data):
        # Process LIDAR data
        ranges = scan_data.ranges
        front = min(min(ranges[:30]), min(ranges[-30:]))  # Front ranges
        left = min(ranges[60:120])  # Left ranges
        right = min(ranges[240:300])  # Right ranges

        if front < self.safe_distance:
            self.twist.linear.x = 0.0  # Stop
            self.twist.angular.z = 0.5 if left > right else -0.5  # Rotate
        else:
            self.twist.linear.x = 0.2  # Move forward
            self.twist.angular.z = 0.0  # No rotation

        self.cmd_pub.publish(self.twist)

    def run(self):
        rospy.spin()

if __name__ == '__main__':
    try:
        ObstacleAvoidance().run()
    except rospy.ROSInterruptException:
        pass

