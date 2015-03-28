#Shrinidhi Thirumalai and Zarin Bhuiyan
#Gets picture from user input, then outputs a csv file of text on image

#Imports:
import numpy as np
import cv2
from PIL import Image
import pytesseract
import csv


def get_image():
    """Getting Image Capture from the user, and saving it as image.jpg"""
    cap = cv2.VideoCapture(0)
    running = True
    while running:
        # Capture frame-by-frame
        ret, frame = cap.read()
        # Display the resulting frame
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            s, img = cap.read()
            if s:
                cv2.imwrite('image.jpg', img)#save image
            running = False #close video
    #When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

def extract_text(img):
    """Takes an image location as an input, then filters and returns text in it"""
    extractedtext = pytesseract.image_to_string(Image.open(img))
    return extractedtext

def write_text(text):
    """Takes text as input, and writes it to a CSV"""
    with open('output.csv', 'wb') as csvfile:
        output = csv.writer(csvfile, delimiter= ' ', quotechar = '|', quoting = csv.QUOTE_MINIMAL)
        output.writerow([text])

if __name__ == "__main__":
    get_image()
    extractedtext = extract_text('image.jpg')
    write_text(extractedtext)
