import cv2
import numpy as np
import time
import os
import handgesturemodule as htm
brushThickness = 4
cap= cv2.VideoCapture(0)
cap.set(3,1920)
cap.set(4,1080)
DRAWCOLOUR=(255,0,255)
detector=htm.handDetector(detectionCon=0.9,maxHands=1)
xp,yp=0,0
imgCanvas = np.zeros((490,640, 3), np.uint8)
while True:
    success, img = cap.read()
    img=detector.findHands(img)
    lmlist,bbox=detector.findPosition(img)


    if len(lmlist)!=0:
        x1, y1 = lmlist[8][1], lmlist[8][2]
        x2, y2 = lmlist[12][2], lmlist[12][1]



        fingers=detector.fingersUp()
        if fingers[1]==True and fingers[2]==True:
            if xp==0 and yp==0:
                xp, yp=x1,y1
            cv2.line(img, (xp, yp), (x1, y1), DRAWCOLOUR, brushThickness)
            cv2.line(imgCanvas,(xp,yp),(x1,y1),DRAWCOLOUR, brushThickness)
            xp,yp=x1,y1
            print("Draw")

    cv2.imshow("Image",img)
    cv2.imshow("canvas", imgCanvas)

    cv2.waitKey(1)