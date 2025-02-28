#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import tf
import math
import sys
import termios
import tty

class TurtlebotController:
    def __init__(self):
        # ROS düğümünü başlat
        rospy.init_node('turtlebot_move_sequence', anonymous=True)
        
        # Publisher ve Subscriber tanımla
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.sub = rospy.Subscriber('/odom', Odometry, self.odom_callback)
        
        # Yönelim açısı (yaw) ve hedef açı
        self.yaw = 0.0
        self.target_yaw = None
        self.x = 0.0
        self.y = 0.0
        rospy.sleep(2)

    def odom_callback(self, msg):
        # Turtlebot'un anlık yönelim açısını hesapla (yaw)
        orientation_q = msg.pose.pose.orientation
        orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
        (roll, pitch, yaw) = tf.transformations.euler_from_quaternion(orientation_list)
        self.yaw = yaw
        self.x = msg.pose.pose.position.x
        self.y = msg.pose.pose.position.y

    def move_forward(self, duration):
        # İleriye hareket etme
        move_cmd = Twist()
        move_cmd.linear.x = 0.2
        move_cmd.angular.z = 0.0
        self.pub.publish(move_cmd)
        rospy.sleep(duration)
        move_cmd.linear.x = 0.0
        self.pub.publish(move_cmd)

    def move_backward(self, duration):
        # Geriye hareket etme
        move_cmd = Twist()
        move_cmd.linear.x = -0.2
        move_cmd.angular.z = 0.0
        self.pub.publish(move_cmd)
        rospy.sleep(duration)
        move_cmd.linear.x = 0.0
        self.pub.publish(move_cmd)

    def rotate(self, angle):
        # Yönelime göre dönme
        start_yaw = self.yaw
        self.target_yaw = start_yaw + math.radians(angle)
        
        # Açıyı normalize et
        if self.target_yaw > math.pi:
            self.target_yaw -= 2 * math.pi
        elif self.target_yaw < -math.pi:
            self.target_yaw += 2 * math.pi
        
        move_cmd = Twist()
        move_cmd.angular.z = 0.3 if angle > 0 else -0.3
        while abs(self.target_yaw - self.yaw) > 0.05 and not rospy.is_shutdown():
            self.pub.publish(move_cmd)
            rospy.sleep(0.1)
        
        move_cmd.angular.z = 0.0
        self.pub.publish(move_cmd)

    def execute_sequence(self):
        # Hareket sırasını uygula
        self.move_forward(5)
        rospy.sleep(1)
        self.rotate(90)
        rospy.sleep(1)
        self.move_backward(5)
        rospy.sleep(1)
        self.rotate(-90)
        rospy.sleep(1)
        self.move_forward(5)
        rospy.sleep(1)
        self.rotate(135)
        rospy.sleep(1)
        self.move_forward(5)
        rospy.sleep(1)
        self.enable_keyboard_control()

    def enable_keyboard_control(self):
        # Klavye kontrolü için tuşları dinle
        rospy.loginfo("Klavyeden kontrol aktif. W/A/S/D tuşları ile hareket ettirebilirsiniz.")
        settings = termios.tcgetattr(sys.stdin)
        try:
            while not rospy.is_shutdown():
                tty.setraw(sys.stdin.fileno())
                key = sys.stdin.read(1)
                if key == 'w':
                    self.move_cmd(0.2, 0.0)
                elif key == 's':
                    self.move_cmd(-0.2, 0.0)
                elif key == 'a':
                    self.move_cmd(0.0, 0.3)
                elif key == 'd':
                    self.move_cmd(0.0, -0.3)
                elif key == '\x03':
                    break
                rospy.loginfo(f"Anlık Pozisyon - X: {self.x:.2f}, Y: {self.y:.2f}")
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)

    def move_cmd(self, linear, angular):
        move_cmd = Twist()
        move_cmd.linear.x = linear
        move_cmd.angular.z = angular
        self.pub.publish(move_cmd)

if __name__ == '__main__':
    try:
        controller = TurtlebotController()
        controller.execute_sequence()
    except rospy.ROSInterruptException:
        pass

