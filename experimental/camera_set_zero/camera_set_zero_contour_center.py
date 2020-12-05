import cv2
import numpy as np

cap = cv2.VideoCapture(0)
high = np.array([ 176, 255, 255])
low = np.array([ 156, 100, 100])

first_x = 0
first_y = 0

second_x = 0
second_y = 0

temp_x = []
temp+y = []

img = cap.read()[1]
hsv = cv2.cvtColor( img, cv2.COLOR_BGR2HSV)
mask = cv2.inRange( hsv, low, high)
cont = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
#c = max(cont, key=cv2.contourArea)
length = len(cont)
print(length)
for i in range(length):
    M = cv2.moments(cont[i])
    #center = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))
    ((x, y), rad ) = cv2.minEnclosingCircle(cont[i])
    if rad > 6:
        cv2.circle(img, (int(x), int(y)), int(rad), (51,255,51), 2 )
        print("x: "+str(int(x))+" y: "+str(int(y)))
       
    #image = cv2.drawContours(img, cont, -1, (51,255,51), 3)
    
cv2.imshow('img',img)
key = cv2.waitKey(0)&0xff
   
