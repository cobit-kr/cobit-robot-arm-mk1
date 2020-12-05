from adafruit_servokit import ServoKit
from time import sleep

kit = ServoKit(channels=16)
while True:
	kit.continuous_servo[2].throttle = 0.2
	sleep(10)
	kit.continuous_servo[2].throttle = -0.2
	sleep(10)

	
