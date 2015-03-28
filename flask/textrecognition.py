#Shrinidhi Thirumalai and Zarin Bhuiyan
#Codestellation Hackathon 2015

#Business Card Reader
#Gets picture from user input, then outputs a csv file of the processed text on image

#Imports:
import numpy as np
import cv2
from cv2 import cv
from PIL import Image
import pytesseract
import csv
from cropping import *

def fail (msg, img):
    """Graceful Fail with error message"""
    blank = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
    blank = display_text(blank, msg + '\n Press any key to restart.')
    show_image_till_key(blank, 0)
    cv2.destroyAllWindows()
    main()

def get_image(imgFile, outFile):
    """Getting Image Capture from the user, and saves image as image.jpg"""
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
                cv2.imwrite(outFile, img)
                running = False #close video
    #When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

def filter_image(imgFile, outFile):
    """Reads image.jpg and re-writes a clear filtered image.jpg"""
    img = cv2.imread('image.jpg',0)
    #blurring
    img = cv2.medianBlur(img, 3)
    #thresholding
    valid, thresh_img = cv2.threshold(img, 127, 255, cv2.THRESH_OTSU)
    if valid:
        img = thresh_img
    #writing to file
    cv2.imwrite(outFile, img)

def subimage(imgFile, angle):  
    # img = cv2.imread(imgFile,0)
    img = cv.LoadImage(imgFile)
    imgcv2 = cv2.imread('image.jpg',0)
    width = imgcv2.shape[1]
    height = imgcv2.shape[0]
    centre = (width/2, height/2)
    theta = angle #in radians
    width = 100
    height = 200
    
    # cv.SaveImage('image.jpg', patch)

    imgFile = cv.CreateImage((width, height), img.depth, img.nChannels)
    mapping = np.array([[np.cos(theta), -np.sin(theta), centre[0]],
                        [np.sin(theta), np.cos(theta), centre[1]]])
    map_matrix_cv = cv.fromarray(mapping)
    cv.GetQuadrangleSubPix(img, img, map_matrix_cv)
    cv.SaveImage('rotation_test.jpg', img)
    return img


def extract_text(imgFile):
    """Takes an image location as an input, then filters and returns the text in it as a string"""
    extractedtext = pytesseract.image_to_string(Image.open(imgFile))
    return extractedtext

def write_text(text, outFile):
    """Takes text as input, and writes it to a CSV"""
    with open(outFile, 'wb') as csvfile:
        output = csv.writer(csvfile, delimiter= ' ', quotechar = '|', quoting = csv.QUOTE_MINIMAL)
        output.writerow([text])


def csv_write(imgFile, outFile):
    imgFile_list = []
    writing = csv.writer(open(outFile, 'wb'), delimiter= ',')
    writing.writerows(imgFile_list)

def main():
    """Main sequence for gathering image, and outputting text to file"""
    #file names
    imgFile = 'image.jpg'
    cropFile = 'cropped.jpg'
    filtFile = 'filtered.jpg'
    outFile = 'output.csv'

    #main sequence
    get_image(imgFile, imgFile)
    get_input_and_crop(imgFile, cropFile)
    # subimage(imgFile, np.pi/ 6.0)
    filter_image(cropFile, filtFile)
    extractedText = extract_text(filtFile)
    write_text(extractedText, outFile)
    

if __name__ == "__main__":
    main()
