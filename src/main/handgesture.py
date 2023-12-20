import cv2
import mediapipe as mp
import time

pTime = 0
CTime = 0
cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
handsconnection = mpHands.HAND_CONNECTIONS

while True:
    rv, img = cap.read()

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h,w,c = img.shape
                cx,cy,cz = int(lm.x * w),int(lm.y * h),int(lm.y * c)
                print(id,":",cx,cy,cz)
            #mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    cTime=time.time()
    fps =1/(cTime - pTime)
    pTime=cTime
    cv2.putText(img, str(int(fps)), (20, 80), cv2.FONT_HERSHEY_COMPLEX_SMALL, 3,(255, 0, 255), 3)

    cv2.imshow("Camera", img)
    
    if cv2.waitKey(1) == 13:
        break
cv2.destroyWindow()