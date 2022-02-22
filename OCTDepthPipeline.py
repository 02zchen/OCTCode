# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 21:51:05 2022

@author: zacha
"""

import cv2 as cv
import numpy as np
import os
import math 
"""
currently more calibrated towards horizontral scans. Need to find someway to decrease noise of scan images
"""

img1 = cv.imread(r"C:/Users/zacha/Documents/BTL/OCTImages/220220/B-depth-SGL-20220218-142518 (3).jpg")
img = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)

#median filtering
median = cv.medianBlur(img, 5)
median2 = cv.medianBlur(median, 5)

cv.imshow('medan', median2)
cv.waitKey(0)

#blur = cv.bilateralFilter(median2,9,75,75)
#bilateral filter only introduces more irregularities


"""
compare = np.concatenate((median, median2), axis=1) #side by side comparison
compare2 = np.concatenate((img, median), axis =1)
"""


path = r"C:\Users\zacha\Documents\BTL\ProcessedImgs\DepthTest2"
cv.imwrite(os.path.join(path, 'original.jpg'), img1)
cv.imwrite(os.path.join(path , 'median1.jpg'), median)
cv.imwrite(os.path.join(path , 'median2.jpg'), median2)

#otsu thresholder, introduces angles, deletes the rest of the image
ret, thresh1 = cv.threshold(median2, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
ret,thresh2 = cv.threshold(img,97,255,cv.THRESH_BINARY)


#cv.imshow('otsu', thresh1)
#cv.waitKey(0)

cv.imshow('bw', thresh2)
cv.waitKey(0)

#cv.imwrite(os.path.join(path , 'otsu.jpg'), thresh1)
cv.imwrite(os.path.join(path, 'bw.jpg'), thresh2)


# should be artound dx =2 

sobely = cv.Sobel(src=thresh2, ddepth=-1, dx=0, dy=1, ksize=3)
cv.imshow('result', sobely)
cv.imwrite(os.path.join(path , 'sobely.jpg'), sobely)
cv.waitKey(0)


cdst = cv.cvtColor(sobely, cv.COLOR_GRAY2BGR)
cdstP = np.copy(cdst)
    
lines = cv.HoughLines(sobely, 1, np.pi / 180, 150, None, 0, 50)
    
if lines is not None:
    for i in range(0, len(lines)):
        rho = lines[i][0][0]
        theta = lines[i][0][1]
        a = math.cos(theta)
        b = math.sin(theta)
        x0 = a * rho
        y0 = b * rho
        pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
        pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
        cv.line(cdst, pt1, pt2, (0,0,255), 3, cv.LINE_AA)


linesP = cv.HoughLinesP(sobely, 1, np.pi / 180, 20, None, 50, 50)

if linesP is not None:
    for i in range(0, len(linesP)):
        l = linesP[i][0]
        cv.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0,0,255), 3, cv.LINE_AA)

cv.imshow("Source", img1)
cv.imshow("Detected Lines (in red) - Standard Hough Line Transform", cdst)
cv.imwrite(os.path.join(path, "DetectedLines.jpg"), cdstP)
cv.imshow("Detected Lines (in red) - Probabilistic Line Transform", cdstP)

cv.waitKey(0)




cv.destroyAllWindows


 


"""
cv2.imshow('img', compare)
cv2.waitKey(0)
cv2.imshow('img', compare2)
cv2.waitKey(0)
cv2.destroyAllWindows
"""