cap = None
img = None
key = None


import cv2

cap = cv2.VideoCapture(0)

while True:
  img = cap.read()[1]

  cv2.imshow('my win',img)
  key = cv2.waitKey(1)&0xff
  if key == 27:
    break