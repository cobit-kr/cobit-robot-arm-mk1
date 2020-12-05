from adafruit_servokit import ServoKit
from time import sleep

kit = ServoKit(channels=16)
kit.servo[0].angle = 90
kit.servo[1].angle = 120
panAngle = 90
tiltAngle = 20

kit.servo[1].angle = 150
sleep(1)
	
