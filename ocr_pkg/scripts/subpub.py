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


bridge = CvBridge()

def callback(data):
    if data.data == "Y":

        cap = cv2.VideoCapture('/dev/video0', cv2.CAP_V4L)
        #cap = cv2.VideoCapture(0)
        #cap.set(3,640)
        #cap.set(4,480)

        if cap.isOpened():
            _,frame = cap.read()
            cap.release() #releasing camera immediately after capturing picture
            if _ and frame is not None:
                cv2.imwrite('img.jpg', frame)

        

        img = cv2.imread('img.jpg',cv2.IMREAD_COLOR)
        img = cv2.resize(img, (600,400))

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
        gray = cv2.bilateralFilter(gray, 13, 15, 15) 

        edged = cv2.Canny(gray, 30, 200) 
        contours = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        contours = sorted(contours, key = cv2.contourArea, reverse = True)[:10]
        screenCnt = None

        for c in contours:
        
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.018 * peri, True)
     
            if len(approx) == 4:
                screenCnt = approx
                break

        if screenCnt is None:
            detected = 0
            print ("No contour detected")
        else:
            detected = 1

        if detected == 1:
            cv2.drawContours(img, [screenCnt], -1, (0, 0, 255), 3)
            mask = np.zeros(gray.shape,np.uint8)
            new_image = cv2.drawContours(mask,[screenCnt],0,255,-1,)
            new_image = cv2.bitwise_and(img,img,mask=mask)

            (x, y) = np.where(mask == 255)
            (topx, topy) = (np.min(x), np.min(y))
            (bottomx, bottomy) = (np.max(x), np.max(y))
            #Cropped = gray[topx:bottomx+1, topy:bottomy+1]
            dry = img[topx:bottomx+1, topy:bottomy+1]
            #img = cv2.resize(img,(500,300))
            #Cropped = cv2.resize(Cropped,(400,200))
            #cv2.imwrite("cropped.jpg", Cropped)
            #cropped = cv2.imread('cropped.jpg', cv2.IMREAD_COLOR)
            #cv2.imwrite("/home/ocr_ws/src/ocr_pkg/NumberPlate.jpg", dry)
            send = bridge.cv2_to_imgmsg(dry, "bgr8")
            pub.publish(send)

            

            # print(candidates[len(candidates) - 1])


def subpub():
    
    rospy.init_node('subpub', anonymous=True)

    rate = rospy.Rate(0.5)

    rospy.Subscriber("str_topic", String, callback)

    rospy.spin()

if __name__ == '__main__':

    try:
        pub = rospy.Publisher("img_topic", Image, queue_size=1)

        subpub()

    except rospy.ROSInterruptException:

        pass