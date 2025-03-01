#!/usr/bin/env python3
import rospy
from akif_package.msg import IoTSensor

def iot_sensor_callback(iot_sensor_message):
    rospy.loginfo("new IoT data received: (%d, %s, %.2f ,%.2f)", 
        iot_sensor_message.id,iot_sensor_message.name,
        iot_sensor_message.temperature,iot_sensor_message.humidity)
    
rospy.init_node('iot_sensor_subscriber_node', anonymous=True)

rospy.Subscriber("iot_sensor_topic", IoTSensor, iot_sensor_callback)

# spin() simply keeps python from exiting until this node is stopped
rospy.spin()
