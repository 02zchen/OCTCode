# -*- coding: utf-8 -*-
import cv2 as cv

img_grayscale = cv.imread('m', 0)


cv.imshow('Result', img_grayscale)

cv.waitKey(0)

cv.destroyAllWindows()