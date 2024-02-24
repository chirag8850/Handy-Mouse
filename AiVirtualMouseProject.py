import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy
import autopy.mouse
import pyautogui

wCam, hCam = 640, 460
frameR = 120  # Frame Reduction
smoothening = 7

plocX, plocY = 0, 0
clocX, clocY = 0, 0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
detector = htm.handDetector(maxHands=1)
wScr, hScr = autopy.screen.size()

while True:


    # hand Landmarks
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)


    # Getting the tip of the index and middle finger
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        # print(x1, y1, x2, y2)

    # Check which finger are up
        fingers = detector.fingersUp()
        # print(fingers)

        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)
        # Only index finger : Moving Mode
        if fingers[1] == 1 and fingers[2] == 0:
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))

        # Smoothen Values
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

        # Move Mouse
            autopy.mouse.move(wScr - clocX, clocY)
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY

        # Both Index and Middle Finger are up : Clicking Mode
        if fingers[1] == 1 and fingers[2] == 1:

        # Find distance between fingers
            length, img, lineInfo = detector.findDistance(8, 12, img)
#             print(length)
#             # 10. Click Mouse if distance short
            if length < 40:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click()
            elif y1 > y2+10:
                pyautogui.scroll(-5)  # scroll down
        if fingers[1] == 0 and fingers[2] == 0:
            if y1 > y2-10:
                pyautogui.scroll(5)  # scroll up
#
        # Both Index and Thumb Finger are up : Right Clicking Mode
        if fingers[0] == 1 and fingers[1] == 1:
        # Find distance between fingers
            length2, img2, lineInfo2 = detector.findDistance(4, 8, img)
#             print(length2)
        # Right CLick Mouse if distance short
            if length2 < 40:
                cv2.circle(img, (lineInfo2[4], lineInfo2[5]), 15, (0, 255, 0), cv2.FILLED)
                pyautogui.click(button='right')

        if fingers[1] == 0 and fingers[2] == 0 and fingers[3]==0:
            if y1 > y2 - 20:
                pyautogui.hotkey('alt', 'tab')

# 11. Frame Rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (15, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
#
    # 12. Display
    cv2.imshow("Image", img)
    cv2.waitKey(1)
    keyCode = cv2.waitKey(1)
    if cv2.getWindowProperty("Image", cv2.WND_PROP_VISIBLE) >= 1:
        continue
    break

cv2.destroyAllWindows()
