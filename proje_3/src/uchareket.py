#!/usr/bin/env python3
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

def move_to_goal(x, y, w=1.0):
    # Action Client oluştur
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()

    # Hedef noktayı belirle
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = x
    goal.target_pose.pose.position.y = y
    goal.target_pose.pose.orientation.w = w

    # Hedefe git
    rospy.loginfo(f"Robot hedefe gidiyor: x={x}, y={y}")
    client.send_goal(goal)
    client.wait_for_result()

    if client.get_state() == actionlib.GoalStatus.SUCCEEDED:
        rospy.loginfo("Robot hedefe başarıyla ulaştı!")
        return True
    else:
        rospy.loginfo("Robot hedefe ulaşamadı!")
        return False

if __name__ == "__main__":
    rospy.init_node('uchareket')

    # Hedef koordinatlar
    hedefler = [
        (1.0, 2.0),  # İlk nokta
        (3.0, 4.0),  # İkinci nokta
        (-2.0, 1.0)  # Üçüncü nokta
    ]

    for hedef in hedefler:
        x, y = hedef
        if not move_to_goal(x, y):
            rospy.logerr("Hedefe ulaşma başarısız! Program sonlandırılıyor.")
            break

