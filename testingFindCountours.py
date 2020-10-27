import numpy as numpy
import cv2 as cv

im = cv.imread('pieces/1-1mask.png')
imgray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
ret, thresh = cv.threshold(imgray, 127, 255, 0)
contours, hiearchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

print((contours))
(cv.drawContours(im, contours, -1, (0,255,0), 3))