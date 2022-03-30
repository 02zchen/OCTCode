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
def sortAvgHeight(val):
    x = val[0]
    ret = x[1]
    return ret

img1 = cv.imread(r"C:\Users\zacha\Documents\BTL\OCTImages\220324\BSCAN-SGL-20220324-132207.jpg")

img = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)

#median filtering
median = cv.medianBlur(img, 5)
median2 = cv.medianBlur(median, 5)

#blur = cv.bilateralFilter(median2,9,75,75)
#bilateral filter only introduces more irregularities

path = r"C:\Users\zacha\Documents\BTL\ProcessedImgs\DepthTest2"
cv.imwrite(os.path.join(path, 'original.jpg'), img1)
cv.imwrite(os.path.join(path , 'median1.jpg'), median)
cv.imwrite(os.path.join(path , 'median2.jpg'), median2)

#otsu thresholder, introduces angles, deletes the rest of the image
ret,thresh2 = cv.threshold(img,97,255,cv.THRESH_BINARY)




#cv.imwrite(os.path.join(path , 'otsu.jpg'), thresh1)
cv.imwrite(os.path.join(path, 'bw.jpg'), thresh2)

# should be artound dx =2 
sobely = cv.Sobel(src=thresh2, ddepth=-1, dx=0, dy=1, ksize=3)


cdst = cv.cvtColor(sobely, cv.COLOR_GRAY2BGR)
cdstP = np.copy(cdst)
"""    
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
"""

#stores the parameters of all detected lines in an array of (x start, ystart, x end, y end)
linesP = cv.HoughLinesP(sobely, 1, np.pi / 180, 20, None, 50, 50)



linesP = sorted(linesP, key=sortAvgHeight)



lineHeights = []

if linesP is not None:
    for i in range(0, len(linesP)):
        l = linesP[i][0]
        cv.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0,0,255), 1, cv.LINE_AA)
        avgY = (l[3]+l[1])/2
        lineHeights.append(avgY)

distances = []        
if lineHeights is not None:
    lineHeights.sort(reverse = True)
    if (len(lineHeights) == 1):
        distances.append(lineHeights[0])
    else:
        for j in range(0, len(lineHeights)-1):
            distanceY = lineHeights[j] - lineHeights[j+1]
            if (distanceY > 20):
                distances.append(distanceY)
print("distances")     
print(distances)


#find mean value of distances 
mean = 0;
for i in range(0, len(distances)):
    mean += distances[i]

mean = mean / len(distances)

#convert distances to distance (micrometers) /pixel conversion

convert = 2000 / mean 

print("convert")
print(convert)
#note: the code from the line detection onwards is very crusty; i will probably create a line object to store all of these various values moving forwards to a 3d heat map

    
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