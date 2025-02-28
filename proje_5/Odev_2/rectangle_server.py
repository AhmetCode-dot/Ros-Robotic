#!/usr/bin/env python3

from akif_package.srv import RectangleArea
from akif_package.srv import RectangleAreaRequest
from akif_package.srv import RectangleAreaResponse

import rospy

def handle_rectangle(req):
    print ("Returning [%s * %s = %s]"%(req.a, req.b, (req.a * req.b)))
    return RectangleAreaResponse(req.a * req.b)

def rectangle_server():
    rospy.init_node('rectangle_server')
    s = rospy.Service('rectangle', RectangleArea, handle_rectangle)
    print ("Ready to regtangle area.")
    rospy.spin()
    
if __name__ == "__main__":
    rectangle_server()
