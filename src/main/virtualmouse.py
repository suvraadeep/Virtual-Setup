import cv2
import time
import numpy as np
import pyautogui
import handgesturemodule as htm

##############################################################
pyautogui.FAILSAFE=False
wcam,hcam=640,480
cap = cv2.VideoCapture(0)
cap.set(3, wcam)
cap.set(4, hcam)
pTime=0
screenWidth, screenHeight = pyautogui.size()
detector=htm.handDetector(maxHands=1)
frameR=100
smooth=1
plocx,plocy=0,0
clocx,clocy=0,0
##############################################################


while True:
    #find hand landmark
    success, img = cap.read()
    img=detector.findHands(img)
    lmlist, bbox=detector.findPosition(img)



    # get the tip of the index and middle fingers
    if len(lmlist)!=0:
        x1, y1 = lmlist[8][2], lmlist[8][1]
        x2, y2 = lmlist[12][2], lmlist[12][1]
        x3, y3 = lmlist[4][2], lmlist[4][1]

        #print(x1,y1,x2,y2)
        #checking which fingers are up
        fingers=detector.fingersUp()
        #print(fingers)
        #only index finger:moving mode
        #cv2.rectangle(img, (frameR, frameR), (screenWidth - frameR, screenHeight - frameR), (255, 0, 255), 2)
        cv2.rectangle(img, (frameR, frameR), (wcam - frameR, hcam - frameR), (255, 0, 255), 2)
        if fingers[1]==1 and fingers[2]==0:
            #converting the coordinates
            y4=np.interp(x1,(frameR,wcam-frameR),(0,screenWidth))
            x4=np.interp(y1,(frameR, hcam-frameR),(0,screenHeight))
            clocx =plocx+(x4-plocx)/smooth
            clocy = plocy + (y4 - plocy) / smooth
            
            pyautogui.moveTo(screenWidth-(clocx*1.8),clocy)       #issue that half screen is being covered temp solution is multiplying it with 1.8
            plocx,plocy=clocx,clocy
            
            
        #both index and middle fingers are up clicking mode
        if fingers[1] == 1 and fingers[2] == 1:
            # find distance between fingers
            length,img,isc= detector.findDistance(8,12,img)
            #y4 = np.interp(x1, (frameR, wcam - frameR), (0, screenWidth))
            #x4 = np.interp(y1, (frameR, hcam - frameR), (0, screenHeight))
            #clocx = plocx + (x4 - plocx) / smooth
            #clocy = plocy + (y4 - plocy) / smooth
            print(length)
            # click mouse if distance short
            if length<42:
                #pyautogui.moveTo(screenWidth - (clocx * 1.9), clocy)  # issue that half screen is being covered
                #plocx, plocy = clocx, clocy
                pyautogui.click()

        # both index and thumb are up then double click
        if fingers[1] == 1 and fingers[0] == 1:
            # find distance between fingers
            length, img, isc = detector.findDistance(8, 12, img)
            y4 = np.interp(x1, (frameR, wcam - frameR), (0, screenWidth))
            x4 = np.interp(y1, (frameR, hcam - frameR), (0, screenHeight))
            clocx = plocx + (x4 - plocx) / smooth
            clocy = plocy + (y4 - plocy) / smooth
            print(length)
            if length<96:
                pyautogui.moveTo(screenWidth - (clocx * 1.9), clocy)  # issue that half screen is being covered
                plocx, plocy = clocx, clocy
                pyautogui.doubleClick()

    #frame rate
    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img,str(int(fps)),(20,50),cv2.FONT_ITALIC,2,(255,0,0))
    #display
    cv2.imshow("Image", img)

    if cv2.waitKey(1) == 13:
        break
cv2.destroyWindow()