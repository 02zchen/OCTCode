# -*- coding: utf-8 -*-
"""
Created on Sun Feb 20 20:08:58 2022

@author: zacha
"""


import cv2 as cv
import numpy as np
import os
import math

"""
currently more calibrated towards horizontral scans. Need to find someway to decrease noise of scan images
"""

def sortX(val):
    x = val[0]
    ret = x[0]
    return ret

class lineSorter:
    def __init__(self, xcoord, line):
        self.xcoord = xcoord
        self.line = line

img1 = cv.imread(r"C:/Users/zacha/Documents/BTL/OCTImages/220220/B-width-SGL-20220218-142926 (6).jpg")
img = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
path = r"C:\Users\zacha\Documents\BTL\ProcessedImgs\WidthTest1"


cv.imwrite(os.path.join(path, 'original.jpg'), img1)

#median filtering
median = cv.medianBlur(img, 5)
median2 = cv.medianBlur(median, 5)


cv.imshow('img', img1)
cv.waitKey(0)
#blur = cv.bilateralFilter(median2,9,75,75)
#bilateral filter only introduces more irregularities

cv.imwrite(os.path.join(path , 'median1.jpg'), median)
cv.imwrite(os.path.join(path , 'median2.jpg'), median2)

#otsu thresholder, introduces angles, deletes the rest of the image
#ret, thresh1 = cv.threshold(median2, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
ret,thresh2 = cv.threshold(median2,98,255,cv.THRESH_BINARY)

cv.imwrite(os.path.join(path, 'bw.jpg'), thresh2)

# should be artound dx =1, ksize =3
sobely = cv.Sobel(src=thresh2, ddepth=-1, dx=0, dy=1, ksize=3)
#cv.imshow('result', sobely)
cv.imwrite(os.path.join(path , 'Widthsobely.jpg'), sobely)
#cv.waitKey(0)

#------------------ hugh transform for clean lines
#converts sobely image from gray back to rgb, creates two copies for both hugh transforms
cdst = cv.cvtColor(sobely, cv.COLOR_GRAY2BGR)
cdstP = np.copy(cdst)

#standard hough transform
#if 
#lines = cv.HoughLines(sobely, 1, np.pi / 180, 150, None, 0, 0)
#results in a vector of (theta, radius) pairs
'''
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
'''
#stores the parameters of all detected lines in an array of (x start, ystart, x end, y end)
linesP = cv.HoughLinesP(sobely, 1, np.pi / 180, 20, None, 50, 5)
# input, resolution of r in pixels, resolution of theta in radians, minimum number of intersections to detect a line, min line lenght, max line gap
# adjust for as clean lines as possible

#sort lines by x
linesP = sorted(linesP, key=sortX)


lineSeps = []
lineWidth = []

if linesP is not None:
    for i in range(0, len(linesP)):
        l = linesP[i][0]
        cv.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0,0,255), 1, cv.LINE_AA)
        #img, pt1, pt2, color, thickness, linetype 
        

        #store line widths if the line detected isn't basically the same line as the previous one
        
        width = math.sqrt((l[2] -l[0])**2 + (l[3]-l[1])**2)
        lineWidth.append(width)

        
        if (i < len(linesP) -1):
            lNext = linesP[i+1][0]
            #find the distance between the first point in the next line and the last point in the current line 
            sep = math.sqrt((lNext[0] -l[2])**2 + (lNext[1]-l[3])**2)
            cv.line(cdstP, (l[2], l[3]), (lNext[0], lNext[1]), (0, 255, 0), 1, cv.LINE_AA)
            lineSeps.append(sep)
        #store line
        
#-------------------------Error mapping section---------------------------------

relError = []
reference = 0
if(len(lineWidth) % 2 == 0):
    reference = (lineWidth[len(lineWidth)-1] +lineWidth[len(lineWidth)])/2
else:
    reference = lineWidth[math.floor(len(lineWidth)/2)]
    
for i in range(0, len(lineWidth)):
    relError.append(lineWidth[i] / reference)
    



print("lineWidth")
print(lineWidth)
print("lineSeps")
print(lineSeps)
print("line Errors")
print(relError)
        
cv.imwrite(os.path.join(path, "DetectedLines.jpg"), cdstP)
cv.imshow("Detected Lines (in red) - Probabilistic Line Transform", cdstP)

cv.waitKey(0)




cv.destroyAllWindows