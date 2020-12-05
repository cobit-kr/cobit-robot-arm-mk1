# -*- coding: utf-8 -*-
# USAGE
# python detect_shapes.py --image shapes_and_colors.png

# import the necessary packages
from pyimagesearch.shapedetector import ShapeDetector
import argparse
import imutils
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to the input image")
args = vars(ap.parse_args())

# load the image and resize it to a smaller factor so that
# the shapes can be approximated better

# 저장된 이미지를 연다. 
image = cv2.imread(args["image"])
# 우선 이미지를 디스플레이 한다. 비교를 위해서. 
cv2.imshow("image", image)
# 사이즈를 바꾼다. 아마도 편의성을 위해서 인 듯 하다. imutils는 openCV에서 많이 사용. CV 자체 함수가 불편? 
resized = imutils.resize(image, width=300)
# 역시 이미지를 디스플레이 한다. 비교를 위해서. 
cv2.imshow("resized", resized)
# 원본 이미지와 리사이징 된 것의 비율을 구한다. 왜?
ratio = image.shape[0] / float(resized.shape[0])

# convert the resized image to grayscale, blur it slightly,
# and threshold it

# 흑백으로 바꾼다. 
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
# foreground와 background를 바꾼다. background가 검정이어야 동작한다. bitwise_not함수가 이것을 행한다.
# 배경이 검은색인 이미지에는 적용하면 오동작한다.  
gray1 = cv2.bitwise_not(gray)
# 이미지를 디스플레이 한다. 비교를 위해. 
cv2.imshow("gray", gray1)
# 이미지를 blur 처리한다. 왜? 이미지를 좀 무디게 하려고 하나? 
blurred = cv2.GaussianBlur(gray1, (5, 5), 0)
# 비료를 위해 이미지를 디스플레이 한다. 
cv2.imshow("Blur", blurred)
# threshold값을 적용한다. 흑백의 차이가 극대화 된다. 
thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
# 비교를 위해 이미지를 디스플레이 한다. 
cv2.imshow("thresh", thresh)
# find contours in the thresholded image and initialize the
# shape detector

# 경로선 contour를 발견한다. contour는 여러개가 나오므로 cnts는 여러개의 contour 어레이 이다. 
# 또 하나의 contour, 예를 들어 cnts[0]는 경로를 구성하는 좌표 (x, y)의 어레이 이다. 
# cv2.CHAIN_APPROX_NONE 이 옵션이 계산량이 많아지는 단점이 있지만 모양 판정에서 조금 정확하다. 
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
#	cv2.CHAIN_APPROX_SIMPLE)

# grap_contour는 opeCV버전에 따라 findContour의 출력 순서가 다른 것을 해결해준다. 
# 즉 findContour의 출력중 진자 contour만 걸러서 준다. openCV 버전따라 다른 것도 해결 해서. 
cnts = imutils.grab_contours(cnts)
# cv2.drawContours(image, cnts, -1, (0,0,255), 3)
sd = ShapeDetector()

# loop over the contours
for c in cnts:
	# compute the center of the contour, then detect the name of the
	# shape using only the contour

	# moments()함수는 contour의 여러가지 기하하적인 수치 데이터를 제공해 준다. 
	# 상세한 내용은 만만치 않은 수학을 배경으로 하므로 생략 
	M = cv2.moments(c) 
	# moments() 함수의 출력값은 딕셔너리 변수형태이다. 그래서 { 키값: 데이터, ...} 이런 형태이다. 
	# 키값이 "m10"과 "m01"을 "m00"값으로 나누면 contour의 중심점 (x, y)값을 얻는다. 
	cX = int((M["m10"] / M["m00"]) * ratio)
	cY = int((M["m01"] / M["m00"]) * ratio)
	# contour가 어떤 모양인지 얄려준다. 상세한 네용은 shapedetector class에 기록한다. 
	shape = sd.detect(c)

	# multiply the contour (x, y)-coordinates by the resize ratio,
	# then draw the contours and the name of the shape on the image
	c = c.astype("float")
	c *= ratio
	c = c.astype("int")
	cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
	cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
		0.5, (255, 255, 255), 2)

	# show the output image
	cv2.imshow("Image", image)
	cv2.waitKey(0)