#!/usr/bin/env python
# coding: utf-8

# In[10]:


import numpy as np
import cv2
import imutils
import sys
import pytesseract
import pandas as pd
import time
import pickle

# Add this line to assert the pat h. Else TesseractNotFoundError will be raised.

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    #Read the original image.

img = cv2.imread("Cars0.png")

img = imutils.resize(img, width=500)


cv2.imshow("Original Image", img)  
    #Convert from colored to Grayscale.

gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

cv2.imshow("Preprocess 1 - Grayscale Conversion", gray_img)        #Show modification.

    #Applying Bilateral Filter on the grayscale image.

    #It will remove noise while preserving the edges. So, the number plate remains distinct.

gray_img = cv2.bilateralFilter(gray_img, 11, 17, 17)

cv2.imshow("Preprocess 2 - Bilateral Filter", gray_img) 

    #Finding edges of the grayscale image.

c_edge = cv2.Canny(gray_img, 170, 200)
cv2.imshow("Preprocess 3 - Canny Edges", c_edge)    
contours, heirarchy = cv2.findContours(c_edge, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key = cv2.contourArea, reverse = True)[:30]
NumberPlateCount = None
im2 = img.copy()
cv2.drawContours(im2, contours, -1, (0,255,0), 3)
cv2.imshow("Top 30 Contours", im2)          #Show the top 30 contours.
count = 0
for c in contours:
    perimeter = cv2.arcLength(c, True)      #Getting perimeter of each contour
    approx = cv2.approxPolyDP(c, 0.02 * perimeter, True)
    if len(approx) == 4:            #Selecting the contour with 4 corners/sides.
        NumberPlateCount = approx
        break
masked = np.zeros(gray_img.shape,np.uint8)
new_image = cv2.drawContours(masked,[NumberPlateCount],0,255,-1)
new_image = cv2.bitwise_and(img,img,mask=masked)
cv2.imshow("4 - Final_Image",new_image)     #The final image showing only the number plate.
cv2.waitKey(0)


    #Configuration for tesseract

configr = ('-l eng --oem 1 --psm 3')


    #Running Tesseract-OCR on final image.

text_no = pytesseract.image_to_string(new_image, config=configr)


    #The extracted data is stored in a data file.

data = {'Date': [time.asctime(time.localtime(time.time()))],

        'Vehicle_number': [text_no]}

print(text_no)

cv2.waitKey(0)
#from tensorflow.keras.models import load_model
#text_no.save('ocr.h5')

