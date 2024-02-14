import cv2
import time
import numpy as np
import pyautogui
import handgesturemodule as htm

##############################################################
brushThickness = 4
pyautogui.FAILSAFE=False
wcam,hcam=640,480
cap = cv2.VideoCapture(0)
cap.set(3, wcam)
cap.set(4, hcam)
pTime=0
screenWidth, screenHeight = pyautogui.size()
frameR=100
smooth=0.9
plocx,plocy=0,0
clocx,clocy=0,0
DRAWCOLOUR=(255,0,255)
detector=htm.handDetector(detectionCon=0.9,maxHands=1)
xp,yp=0,0
imgCanvas = np.zeros((490,640, 3), np.uint8)
##############################################################


while True:
    success, img = cap.read()
    img=detector.findHands(img)
    lmlist, bbox=detector.findPosition(img)

    if len(lmlist)!=0:
        x1, y1 = lmlist[8][2], lmlist[8][1]
        x2, y2 = lmlist[12][2], lmlist[12][1]
        y3,x3 = lmlist[4][2], lmlist[4][1]

        fingers=detector.fingersUp()
        cv2.rectangle(img, (frameR, frameR), (wcam - frameR, hcam - frameR), (255, 0, 255), 2)
        if fingers[1]==1 and fingers[2]==0:

            y4=np.interp(x1,(frameR,wcam-frameR),(0,screenWidth))
            x4=np.interp(y1,(frameR, hcam-frameR),(0,screenHeight))

            clocx =plocx+(x4-plocx)/smooth
            clocy = plocy + (y4 - plocy) / smooth

            pyautogui.moveTo(screenWidth-(clocx*1.9),clocy)
            plocx,plocy=clocx,clocy

        if fingers[1] == 1 and fingers[2] == 1:
            length,img,isc= detector.findDistance(8,12,img)

            print(length)
            if length<42:
                pyautogui.click()

        if fingers[1] == 1 and fingers[0] == 1:
            fingers = detector.fingersUp()
            if fingers[0] == True and fingers[1] == True:
                if xp == 0 and yp == 0:
                    xp, yp = x3,y3
                cv2.line(img, (xp, yp), (x3,y3), DRAWCOLOUR, brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x3,y3), DRAWCOLOUR, brushThickness)
                xp, yp = x3,y3
                print("Draw")

    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img,str(int(fps)),(20,50),cv2.FONT_ITALIC,2,(255,0,0))
    cv2.imshow("Image", img)
    cv2.imshow("canvas", imgCanvas)


    if cv2.waitKey(1) == 13:
        break
cv2.destroyWindow()