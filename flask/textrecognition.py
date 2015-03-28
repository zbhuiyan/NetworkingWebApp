#Imports:
import numpy as np
import cv2
from PIL import Image
import pytesseract
import csv


#Getting Image Capture, and saving it as image.jpg:
cap = cv2.VideoCapture(0)
running = True
while running:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
    	s, img = cap.read()
    	if s: #If no error
    		cv2.imwrite('image.jpg', img) #save image
        running = False #close video

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

#Returning Text:
extractedtext = pytesseract.image_to_string(Image.open('image.jpg'))
with open('output.csv', 'wb') as csvfile:
	output = csv.writer(csvfile, delimiter= ' ', quotechar = '|', quoting = csv.QUOTE_MINIMAL)
	output.writerow([extractedtext])
