#!/usr/bin/env python3
import rospy
import requests
from std_msgs.msg import Float32

def get_temperature():
    api_key = "0b7b5ef0b03ad7b17a095b9bf0a7ffbd"
    url = f"http://api.openweathermap.org/data/2.5/weather?q=Konya,tr&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    temperature = data['main']['temp']
    return temperature

def publish_temperature():
    rospy.init_node('konya_hava', anonymous=True)
    pub = rospy.Publisher('konya_temperature', Float32, queue_size=10)
    rate = rospy.Rate(1)  # 1 Hz

    while not rospy.is_shutdown():
        try:
            temp = get_temperature()
            rospy.loginfo(f"Konya'nın sıcaklığı: {temp} °C")
            pub.publish(temp)
        except Exception as e:
            rospy.logerr(f"API Hatası: {e}")
        rate.sleep()

if __name__ == '__main__':
    try:
        publish_temperature()
    except rospy.ROSInterruptException:
        pass
