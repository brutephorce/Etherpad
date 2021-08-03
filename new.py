from typing import ContextManager
import numpy as np
import cv2
from collections import deque
import os



brushThickness = 25
eraserThickness = 100

def setValues(x):
    print("")


folderPath = "header"
myList = os.listdir(folderPath)
print(myList)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
print(len(overlayList))
header = overlayList[0]
drawColor = (255, 0, 255)



cv2.namedWindow("Color detectors")
cv2.createTrackbar("Upper Hue", "Color detectors", 179, 180, setValues)
cv2.createTrackbar("Upper Saturation", "Color detectors", 255, 255, setValues)
cv2.createTrackbar("Upper Value", "Color detectors", 255, 255, setValues)
cv2.createTrackbar("Lower Hue", "Color detectors", 130, 180, setValues)
cv2.createTrackbar("Lower Saturation", "Color detectors", 141, 255, setValues)
cv2.createTrackbar("Lower Value", "Color detectors", 148, 255, setValues)



kernel = np.ones((5, 5), np.uint8)



paintWindow = np.zeros((720, 1280, 3)) + 255


cv2.namedWindow('Paint', cv2.WINDOW_AUTOSIZE)

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

while True:
    
    ret, frame = cap.read()


    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    u_hue = cv2.getTrackbarPos("Upper Hue", "Color detectors")
    u_saturation = cv2.getTrackbarPos("Upper Saturation", "Color detectors")
    u_value = cv2.getTrackbarPos("Upper Value", "Color detectors")
    l_hue = cv2.getTrackbarPos("Lower Hue", "Color detectors")
    l_saturation = cv2.getTrackbarPos("Lower Saturation", "Color detectors")
    l_value = cv2.getTrackbarPos("Lower Value", "Color detectors")
    Upper_hsv = np.array([u_hue, u_saturation, u_value])
    Lower_hsv = np.array([l_hue, l_saturation, l_value])

  
    Mask = cv2.inRange(hsv, Lower_hsv, Upper_hsv)
    Mask = cv2.erode(Mask, kernel, iterations=1)
    Mask = cv2.morphologyEx(Mask, cv2.MORPH_OPEN, kernel)
    Mask = cv2.dilate(Mask, kernel, iterations=1)

 
    cnts, _ = cv2.findContours(Mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    center = None

   
    if len(cnts) > 0:
        
        cnt = sorted(cnts, key=cv2.contourArea, reverse=True)[0]
        
        ((x, y), radius) = cv2.minEnclosingCircle(cnt)
        
        cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
        
        M = cv2.moments(cnt)
        center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
        x1, y1 = center
        if center:
            xp, yp = center
            print("Selection Mode")
            
            if y1 < 125:
                if 250 < x1 < 450:
                    header = overlayList[0]
                    drawColor = (255, 0, 255)
                elif 550 < x1 < 750:
                    header = overlayList[1]
                    drawColor = (255, 0, 0)
                elif 800 < x1 < 950:
                    header = overlayList[2]
                    drawColor = (0, 255, 0)
                elif 1050 < x1 < 1200:
                    header = overlayList[3]
                    drawColor = (0, 0, 0)

            else:
                cv2.circle(frame, (x1, y1), 15, drawColor, cv2.FILLED)
                print("Drawing Mode")
                if xp == 0 and yp == 0:
                    xp, yp = x1, y1

                cv2.line(frame, (xp, yp), (x1, y1), drawColor, brushThickness)

                if drawColor == (0, 0, 0):
                    cv2.line(frame, (xp, yp), (x1, y1), drawColor, eraserThickness)
                    cv2.line(paintWindow, (xp, yp), (x1, y1),
                            drawColor, eraserThickness)

                else:
                    cv2.line(frame, (xp, yp), (x1, y1), drawColor, brushThickness)
                    cv2.line(paintWindow, (xp, yp), (x1, y1),
                            drawColor, brushThickness)

                xp, yp = x1, y1

    frame[0:125, 0:1280] = header
    paintWindow[0:125, 0:1280] = header

    cv2.imshow("Tracking", frame)
    cv2.imshow("Paint", paintWindow)
    cv2.imshow("mask", Mask)

    
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()
