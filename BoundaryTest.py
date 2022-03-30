# -*- coding: utf-8 -*-
"""
Created on Tue Feb 15 12:34:03 2022

@author: zacha
"""
import cv2 as cv


img = cv.imread(r"C:\Users\zacha\OneDrive - Duke University\Pictures\Saved Pictures\thumbnail_Image.jpg")

# Display original image
cv.imshow('Original', img)

cv.waitKey(0)

 

# Convert to graycsale

img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# Blur the image for better edge detection

img_blur = cv.GaussianBlur(img_gray, (3,3), 0)

#otsu thresholding
ret, thresh1 = cv.threshold(img_blur, 100, 255, cv.THRESH_BINARY)
cv.imshow('thresh1', thresh1)

cv.waitKey(0)
 

# Sobel Edge Detection

sobelx = cv.Sobel(src=img_blur, ddepth=-1, dx=1, dy=0, ksize=5) # Sobel Edge Detection on the X axis

sobely = cv.Sobel(src=img_blur, ddepth=-1, dx=0, dy=1, ksize=5) # Sobel Edge Detection on the Y axis

sobelxy = cv.Sobel(src=img_blur, ddepth=-1, dx=1, dy=1, ksize=5) # Combined X and Y Sobel Edge Detection


# Display Sobel Edge Detection Images

cv.imshow('Sobel X', sobelx)
cv.imwrite('sobelx.jpg', sobelx)


cv.waitKey(0)

cv.imshow('Sobel Y', sobely)

cv.waitKey(0)

cv.imshow('Sobel X Y using Sobel() function', sobelxy)

cv.waitKey(0)

 

# Canny Edge Detection

edges = cv.Canny(image=img_blur, threshold1=100, threshold2=200) # Canny Edge Detection
cv.imshow('Canny Edge Detection', edges)

cv.waitKey(0)

#contour detection
contours, hierarchy = cv.findContours(image=thresh1, mode=cv.RETR_TREE, method=cv.CHAIN_APPROX_NONE)

image_copy = img.copy()
cv.drawContours(image=image_copy, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv.LINE_AA)
cv.imshow('None approximation', image_copy)
cv.waitKey(0)


# Display Canny Edge Detection Image



 

cv.destroyAllWindows()

