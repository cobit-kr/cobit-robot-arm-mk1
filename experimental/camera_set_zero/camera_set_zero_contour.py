import cv2
import numpy as np

cap = cv2.VideoCapture(0)
high = np.array([ 176, 255, 255])
low = np.array([ 156, 100, 100])
while True:
  img = cap.read()[1]
  hsv = cv2.cvtColor( img, cv2.COLOR_BGR2HSV)
  mask = cv2.inRange( hsv, low, high)
  cont = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
  c = max(cont, key=cv2.contourArea)
  M = cv2.moments(c)
  center = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))
  ((x, y), rad ) = cv2.minEnclosingCircle(c)
  cv2.circle(img, (int(x), int(y)), int(rad), (51,255,51), 2 )
  #image = cv2.drawContours(img, cont, -1, (51,255,51), 3)
  print(center)
  cv2.imshow('img',img)
  key = cv2.waitKey(1)&0xff
  if key == 27:
    break