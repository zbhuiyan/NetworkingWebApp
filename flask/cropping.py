#Shrinidhi Thirumalai and Zarin Bhuiyan
#Codestellation Hackathon 2015

#Business Card Reader
#Gets picture from user input, then outputs a csv file of the processed text on image

#Imports:
import numpy as np
import cv2
from PIL import Image
import pytesseract
import csv

def display_text(img, text):
	"""Puts given text onto given image"""
	fontsize = 1
	msglist = text.rstrip().split('\n')
	print msglist
	font = cv2.FONT_HERSHEY_SIMPLEX
	y = img.shape[1]/2
	for msg in msglist:
		cv2.putText(img,msg,(10,y), font, fontsize, (255,255,255),2)
		y += fontsize*25
	return img

def show_image_till_key(img, userkey):
	"""Shows given image until given userkey is pressed"""
	cv2.imshow('display',img)
	key = cv2.waitKey(userkey)
	return key

def image_to_contours(img):
	"""returns all contours of image"""
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	gray = cv2.bilateralFilter(gray, 11, 17, 17)
	edged = cv2.Canny(gray, 30, 200)

	# find contours in the image
	(cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	mask = np.ones(img.shape[:2], dtype="uint8") * 255
	cnts = sorted(cnts, key = (lambda x: cv2.arcLength(x, True)), reverse = True)[:10]
	return cnts

def user_response(contour, img):
	"""Gets user input on if contour is correct"""
	#Highlight outline:
	cv2.drawContours(img, [contour], -1, (0, 255, 0), 3)
	img = display_text(img, 'Is this your business card outline? \n Enter y for yes, n for no')
	while(1):
	    key = show_image_till_key(img, 33)
	    if key ==ord('y'):
	        return True
	    elif key ==ord('n'):  # normally -1 returned,so don't print it
	        return False
	cv2.destroyAllWindows()

def if_crop(img):
	print "in if crop"
	starter = img.copy()
	starter = display_text(starter, 'Does your image need to be cropped? \n ie: Is there extra background?')
	while True:
		key = show_image_till_key(starter, 33)
		if key == ord('y'):
			return True
		elif key == ord('n'):
			return False

def show_original_image(img):
	#Display original image:
	orig = img.copy()
	orig = display_text(orig, 'Enter key to begin')
	show_image_till_key(orig, 0)
	cv2.destroyAllWindows()
	print "orignal image done"

def get_user_contour(img):
	"""main sequence for user input to find correct contour"""
	#Finding edges of image
	cnts = image_to_contours(img)

	# loop over the contours
	for screen in cnts:
		peri = cv2.arcLength(screen, True)
		approx = cv2.approxPolyDP(screen, 0.02 * peri, True)
		# if our approximated contour has roughly four points, display it
		if 2 <= len(approx) <= 5:
			if user_response(screen, img):
				return screen
		cv2.destroyAllWindows()
	fail('Could not find card in image. \n Please try again', img)

def crop(img, contour):
	"""Crops original file to given contour"""
	x,y,w,h = cv2.boundingRect(contour)
	print x,y,w,h
	crop_img = img[y:y+h, x:x+w]
	return crop_img

def get_input_and_crop(imgFile, outFile):
	"""Gets user input, crops to given contour, and saves to file"""
	orig = cv2.imread(imgFile,1)
	img = orig.copy()
	#Show original image:
	# show_original_image(img)
	toCrop = if_crop(img)
	print 'tocrop', toCrop
	if toCrop:
		print "to crop"
		contour = get_user_contour(img)
		cropped = crop(orig, contour)
	else:
		print "not in to crop"
		cropped = orig
	show_image_till_key(cropped, 0)
	cv2.imwrite(outFile, cropped)

if __name__ == "__main__":
	img = get_input_and_crop(imgFile, outFile)

