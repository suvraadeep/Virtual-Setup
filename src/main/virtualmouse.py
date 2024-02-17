import cv2
import time
import numpy as np
import pyautogui
import handgesturemodule as htm


##############################################################
#Preprocessing templates 
pyautogui.FAILSAFE=False
wcam,hcam=640,480
cap = cv2.VideoCapture(0)
cap.set(3, wcam)
cap.set(4, hcam)
pTime=0
screenWidth, screenHeight = pyautogui.size()
detector=htm.handDetector(maxHands=2)
frameR=100
smooth=1
plocx,plocy=0,0
clocx,clocy=0,0
##############################################################


while True:
    success, img = cap.read()
    img=detector.findHands(img)
    lmlist, bbox=detector.findPosition(img)



    if len(lmlist)!=0:
        x1, y1 = lmlist[8][2], lmlist[8][1]
        x2, y2 = lmlist[12][2], lmlist[12][1]
        x3, y3 = lmlist[4][2], lmlist[4][1]


        fingers=detector.fingersUp()

        cv2.rectangle(img, (frameR, frameR), (wcam - frameR, hcam - frameR), (255, 0, 255), 2)
        if fingers[1]==1 and fingers[2]==0:

            y4=np.interp(x1,(frameR,wcam-frameR),(0,screenWidth))
            x4=np.interp(y1,(frameR, hcam-frameR),(0,screenHeight))
            clocx =plocx+(x4-plocx)/smooth
            clocy = plocy + (y4 - plocy) / smooth
            
            pyautogui.moveTo(screenWidth-(clocx*1.8),clocy)       #issue that half screen is being covered temp solution is multiplying it with 1.8
            plocx,plocy=clocx,clocy

        if fingers[1] == 1 and fingers[2] == 1:
            length,img,isc= detector.findDistance(8,12,img)
            print(length)
            if length<42:
                pyautogui.click()


        if fingers[1] == 1 and fingers[0] == 1:

            length, img, isc = detector.findDistance(8, 12, img)
            y4 = np.interp(x1, (frameR, wcam - frameR), (0, screenWidth))
            x4 = np.interp(y1, (frameR, hcam - frameR), (0, screenHeight))
            clocx = plocx + (x4 - plocx) / smooth
            clocy = plocy + (y4 - plocy) / smooth
            print(length)
            if length<96:
                pyautogui.moveTo(screenWidth - (clocx * 1.9), clocy) 
                plocx, plocy = clocx, clocy
                pyautogui.doubleClick()

    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img,str(int(fps)),(20,50),cv2.FONT_ITALIC,2,(255,0,0))
    cv2.imshow("Image", img)

    if cv2.waitKey(1) == 13:
        break
cv2.destroyWindow()