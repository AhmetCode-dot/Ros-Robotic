#!/usr/bin/env python3

import sys
import rospy
from akif_package.srv import RectangleArea
from akif_package.srv import RectangleAreaRequest
from akif_package.srv import RectangleAreaResponse

def rectangle_client(x, y):
    rospy.wait_for_service('rectangle')
    try:
        rectangle = rospy.ServiceProxy('rectangle', RectangleArea)
        resp1 = rectangle(x, y)
        return resp1.alan
    except rospy.ServiceException(e):
        print ("Service call failed: %s"%e)

def usage():
    return 

if __name__ == "__main__":
    if len(sys.argv) == 3:
        x = float(sys.argv[1])
        y = float(sys.argv[2])
    else:
        print (" %s [x y]"%sys.argv[0])
        sys.exit(1)
    print ("Requesting %s*%s"%(x, y))
    s = rectangle_client(x, y)
    print ("Rectangle Area: %s * %s = %s"%(x, y, s))
