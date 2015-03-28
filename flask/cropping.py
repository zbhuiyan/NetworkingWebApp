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

def fail(msg):
	

def display_text(img, text):
	font = cv2.FONT_HERSHEY_SIMPLEX
	cv2.putText(img,text,(10,500), font, 1,(255,255,255),2)
	return img

def image_to_contours(img):
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	gray = cv2.bilateralFilter(gray, 11, 17, 17)
	edged = cv2.Canny(gray, 30, 200)

	# find contours in the image
	(cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	mask = np.ones(img.shape[:2], dtype="uint8") * 255
	cnts = sorted(cnts, key = (lambda x: cv2.arcLength(x, True)), reverse = True)[:10]
	return cnts

def user_contour_response(contour, img):

	#Highlight outline:
	cv2.drawContours(img, [contour], -1, (0, 255, 0), 3)
	img = display_text(img, 'Is this your business card outline? Enter y for yes, n for no')
	while(1):
	    cv2.imshow('img',img)
	    key = cv2.waitKey(33)
	    if key ==ord('y'):
	        return True
	    elif key ==ord('n'):  # normally -1 returned,so don't print it
	        return False
	cv2.destroyAllWindows()

def get_user_contour(img):
	#Finding edges of image
	cnts = image_to_contours(img)

	#Display original image:
	orig = img.copy()
	orig = display_text(orig, 'Enter key to begin')
	cv2.imshow('orig', orig)
	key = cv2.waitKey(0)
	cv2.destroyAllWindows()
	 
	# loop over the contours
	for screen in cnts:
		peri = cv2.arcLength(screen, True)
		approx = cv2.approxPolyDP(screen, 0.02 * peri, True)
		# if our approximated contour has roughly four points, display it
		if 2 <= len(approx) <= 5:
			if user_contour_response(screen, img):
				return screen
		cv2.destroyAllWindows()
	failwith('Could not find card in image. Please try again')

def crop(img, orig, contour):
	x,y,w,h = cv2.boundingRect(contour)
	print x,y,w,h
	crop_img = orig[y:y+h, x:x+w]
	return crop_img

def get_input_and_crop():
	orig = cv2.imread('examplecard.jpg',1)
	img = orig.copy()
	contour = get_user_contour(img)
	return crop(img, orig, contour)

if __name__ == "__main__":
	img = get_input_and_crop()
	cv2.imshow('img',img)
	key = cv2.waitKey(0)

