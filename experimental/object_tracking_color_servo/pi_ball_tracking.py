'''
Object detection ("Ball tracking") with OpenCV
    Adapted from the original code developed by Adrian Rosebrock
    Visit original post: https://www.pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/
Developed by Marcelo Rovai - MJRoBot.org @ 7Feb2018 
'''

# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
from time import sleep
import RPi.GPIO as GPIO
import sys
from adafruit_servokit import ServoKit

"""
def setServoAngle(servo, angle):
    pwm = GPIO.PWM(servo, 50)
    pwm.start(8)
    dutyCycle = angle / 18. + 3.
    pwm.ChangeDutyCycle(dutyCycle)
    #sleep(0.3)
    pwm.stop()

# position servos to present object at center of the frame
def mapServoPosition (x, y):
    global panAngle
    global tiltAngle
    global pan_servo
    global tilt_servo
#    if (y < 120):
#        panAngle += 20
#        if panAngle > 140:
#            panAngle = 140
#        setServoAngle(pan_servo, panAngle)

#    if (y > 180):
#        panAngle -= 20
#        if panAngle < 40:
#            panAngle = 49
#        setServoAngle(pan_servo, panAngle)

    if (x < 120):
        tiltAngle += 10
        if tiltAngle > 140:
            tiltAngle = 140
        setServoAngle(tilt_servo, tiltAngle)

    if (x > 180):
        tiltAngle -= 10
        if tiltAngle < 40:
            tiltAngle = 40
        setServoAngle(tilt_servo, tiltAngle)


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

tilt_servo = 17
GPIO.setup(tilt_servo, GPIO.OUT)

pan_servo = 27
GPIO.setup(pan_servo, GPIO.OUT)

setServoAngle(pan_servo, 90)
setServoAngle(tilt_servo, 90)
"""

y = 0
x = 0

# position servos to present object at center of the frame
def mapServoPosition (x, y, kit):
    global panAngle
    global tiltAngle
    global pan_servo
    global tilt_servo

    if (x < 50):
        panAngle += 5
        if panAngle > 140:
            panAngle = 140
        kit.servo[0].angle = panAngle
        #setServoAngle(tilt_servo, tiltAngle)


    if (x > 260):
        panAngle -= 5
        if panAngle < 40:
            panAngle = 40
        kit.servo[0].angle = panAngle
        #setServoAngle(tilt_servo, tiltAngle)
    
    if (y > 160):
        tiltAngle += 5
        if tiltAngle > 160:
            tiltAngle = 160
        kit.servo[1].angle = tiltAngle
        #positionServo (tiltServo, tiltAngle)
 
    if (y < 40):
        tiltAngle -= 5
        if tiltAngle < 60:
            tiltAngle = 60
        kit.servo[1].angle = tiltAngle
        #positionServo (tiltServo, tiltAngle)


kit = ServoKit(channels=16)
kit.servo[0].angle = 90
kit.servo[1].angle = 120
panAngle = 90
tiltAngle = 65

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
    help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
    help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "yellow object"
# (or "ball") in the HSV color space, then initialize the
# list of tracked points
colorLower = (160, 100, 100)
colorUpper = (190, 255, 255)
#pts = deque(maxlen=args["buffer"])
 
# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
    camera = cv2.VideoCapture(0)
 
# otherwise, grab a reference to the video file
else:
    camera = cv2.VideoCapture(args["video"])

# keep looping
while True:
    # grab the current frame
    (grabbed, frame) = camera.read()

    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if args.get("video") and not grabbed:
        break
 
    # resize the frame, inverted ("vertical flip" w/ 180degrees),
    # blur it, and convert it to the HSV color space
    frame = imutils.resize(frame, width=300)
    #frame = cv2.resize(frame, (300, 300),fx=1, fy=1, interpolation=cv2.INTER_CUBIC)
    frame = imutils.rotate(frame, angle=180)
    # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
 
    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, colorLower, colorUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    
    # find contours in the mask and initialize the current
    # (x, y) center of the ball

    mask_copy, cnts, dummy = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    center = None
    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])) 
       
        #mapServoPosition (center[0], center[1], kit)
        

        # only proceed if the radius meets a minimum size
        #if radius > 10:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
        cv2.circle(frame, (int(x), int(y)), int(radius),
            (0, 255, 255), 2)
        cv2.circle(frame, center, 5, (0, 0, 255), -1)
        mapServoPosition (int(x), int(y), kit)
        
 
    # update the points queue
    #pts.appendleft(center)
    
        # loop over the set of tracked points
    #for i in range(1, len(pts)):
        # if either of the tracked points are None, ignore
        # them
        #if pts[i - 1] is None or pts[i] is None:
        #    continue
 
        # otherwise, compute the thickness of the line and
        # draw the connecting lines
        #thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
        #cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
 
    # show the frame to our screen
    cv2.imshow("Frame", frame)
    cv2.imshow("mask", mask_copy)
    
    print(str(int(y))+" "+str(tiltAngle))
    
    key = cv2.waitKey(1) & 0xFF
 
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break
 
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
