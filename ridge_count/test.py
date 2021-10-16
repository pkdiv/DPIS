import math
import os
import scipy
import imutils
from ridge_count.FingerprintImageEnhancer import FingerprintImageEnhancer

'''
For more info please visit https://www.peterkovesi.com/
'''

import cv2
import numpy as np
from ridge_count.walking import walking, walkonce, checkstable, mergeneighbors



def count_ridge_ind(x1,y1,x2,y2,img):
	o_x1 = x1
	o_y1 = y1
	o_x2 = x2
	o_y2 = y2
	np.set_printoptions(threshold=np.inf)

	#Crop tht image to ROI

	if y1<y2: #y1 is lesser than y2, but checking incase of excepetions
		if x1<x2:
			roi = img[y1:y2, x1:x2]
		else:
			roi = img[y1:y2, x2:x1]
	else:
		if x1<x2:
			roi = img[y2:y1, x1:x2]
		else:
			roi = img[y2:y1, x2:x1]

	roi = cv2.resize(roi, (0,0), fx=5, fy=5) #Magnify image to increase accuracy

	#check cropped image
	cv2.imshow('abc',roi)
	cv2.imwrite('results/abc.bmp', roi)

	roi = roi[:,::-1]
	img = roi

	x1 = 0
	y1 = 0
	y2 = len(roi)
	x2 = len(roi[0])

	dx = x2 - x1
	dy = -(y2 - y1)

	alpha = math.degrees(math.atan2(dy, dx))
	rotation = 180 - alpha

	#Rotate based on position of delta wrt core
	if o_x1 > o_x2:
		pass
	else:
		rotation = -rotation


	img_3 = imutils.rotate_bound(img, -rotation)
	#print(img_3[len(img_3) // 2][5:-5])
	mid = img_3[len(img_3) // 2]
	#ind1 = 0
	#ind2 = len(mid)

	#exclude delta and core

	x = scipy.signal.find_peaks(mid[5:-5]) #Count Peaks in array, 5:-5 to try and remove core and delta lines

	return len(x[0])-1 #-1 because the delta gets counted into the peak


def count_ridge(imgpath):

	ridge_count = 0
	im = cv2.imread(imgpath,0) #make changes here

	#Enhancer

	image_enhancer = FingerprintImageEnhancer()         # Create object called image_enhancer

	if(len(im.shape)>2):                               # convert image into gray if necessary
		im = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)

	kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
	im = cv2.filter2D(im, -1, kernel)

	out = image_enhancer.enhance(im)     # run image enhancer
	image_enhancer.save_enhanced_image('temp.png') #make temporary file for enhanced image
	im = cv2.imread('temp.png',0)
	img = np.copy(im)
	cv2.imwrite('temp.png', np.zeros((100, 100, 3), np.uint8)) #purge image data incase of delete failure
	os.unlink('temp.png')

	#Core and Delta Detection

	stacked_img = np.stack((im,)*3, axis=-1)
	detect_SP = walking(im)

	if min(detect_SP['core'].shape) !=0:
		for i in range(0, detect_SP['core'].shape[0]):
			centre = (int(detect_SP['core'][i,0]), int(detect_SP['core'][i,1]))
			stacked_img = cv2.circle(stacked_img, centre, 10, (0,0,255), 2)

	if min(detect_SP['delta'].shape) !=0:
		for j in range(0, detect_SP['delta'].shape[0]):
			x = int(detect_SP['delta'][j,0])
			y = int(detect_SP['delta'][j,1])
			pts = np.array([[x,y-10], [x-9,y+5], [x+9,y+5]])
			stacked_img = cv2.polylines(stacked_img, [pts], True, (0,255,0), 2)
	cv2.imwrite('aa.png',stacked_img)

	#Ridge Counting

	x1 = int(detect_SP['core'][0][0])
	y1 = int(detect_SP['core'][0][1])

	if len(detect_SP['core'])>1: #pick tip of the core
		if y1>int(detect_SP['core'][1][1]):
			x1 = int(detect_SP['core'][1][0])
			y1 = int(detect_SP['core'][1][1])

	for i in range(len(detect_SP['delta'])): #count ridges from core to each delta
		x2 = int(detect_SP['delta'][i][0])
		y2 = int(detect_SP['delta'][i][1])
		ridge_count += count_ridge_ind(x1, y1, x2, y2, img)

	return ridge_count



# count_ridge('test_images/test_left.png')
