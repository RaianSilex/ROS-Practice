#!/usr/bin/env python3

import cv2
import imutils
import numpy as np
import pytesseract
from pytesseract import Output
import rospy
from std_msgs.msg import String
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
import os

bridge = CvBridge()

def callback(img):

    #nplates_file = open("number_plates.txt", "a")

    img_source = bridge.imgmsg_to_cv2(img, "bgr8")

    kernel = np.ones((5, 5), np.uint8)

    #img_source = cv2.imread('cropped.jpg')
    gray1 = cv2.cvtColor(img_source, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        
    opening = cv2.morphologyEx(gray1, cv2.MORPH_OPEN, kernel)
    canny = cv2.Canny(gray1, 100, 200)

    candidates = []

    for img in [img_source, gray1, thresh, opening, canny]:
        d = pytesseract.image_to_string(img)
        candidates.append(d)

    candidates.sort(key=len)
    data = candidates[len(candidates) - 1]
    print(data)
    #nplates_file.write(data + "\n")
    #nplates_file.close()




def sub():
    
    rospy.init_node('sub', anonymous=True)

    rospy.Subscriber("img_topic", Image, callback)

    rospy.spin()

if __name__ == '__main__':
    sub()