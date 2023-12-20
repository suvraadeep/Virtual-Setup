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
    success, img = cap.read()
    cv2.imshow("image", img)

    imgRGB = cv2.cvtColor(cv2.flip(img, 1), cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    if cv2.waitKey(1)==13:
        break


    if results.multi_hand_landmarks:

        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                nx, ny, nz = int(lm.x * w), int(lm.y * h), int(lm.z * c)
                print(id, ":", nx, ny, nz)
            # mpDraw.draw_landmarks(img, handLms, handsconnection)


        def coordinate(results, landmark, num):

            return float(str(results.multi_hand_landmarks[-1].landmark[landmark]).split('\n')[num].split(" ")[1])
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    
    
    
cv2.destroyWindow()




