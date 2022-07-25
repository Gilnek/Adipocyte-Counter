#!/usr/bin/env python3

import cv2 as cv
import numpy as np

def dist_transform_plus_thresh(thresh_proportion: int = 0.130 ,write: bool = False):
    floodfilled = cv.imread("floodfilled.jpg")

    ff_gray = cv.cvtColor(floodfilled, cv.COLOR_BGR2GRAY)

    ff_dist = cv.distanceTransform(ff_gray, cv.DIST_L2, 0)
    if write: cv.imwrite("ff_dist.png", ff_dist)

    ret, ff_bin = cv.threshold(ff_dist, thresh_proportion*ff_dist.max(), 255, 0)
    if write: cv.imwrite("ff_bin.png", ff_bin)

    return ff_dist, ff_bin

ff_dist, ff_bin = dist_transform_plus_thresh(0.130, False)

image = cv.imread("floodfilled.jpg")


k = ff_bin.copy().astype(np.uint8)
(cnt, hierarchy) = cv.findContours(
    k, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)


rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)

image_f = cv.imread("contorno_celula.jpg")

c = 1
#cv.drawContours(rgb, cnt, -1, (0, 255, 0), 2)
font = cv.FONT_HERSHEY_COMPLEX
# Going through every contours found in the image.
for cnts in cnt :
    
    approx = cv.approxPolyDP(cnts, 0.009 * cv.arcLength(cnts, True), True)
  
    # draws boundary of contours.
    cv.drawContours(rgb, cnt, -1, (0, 255, 0), 2) 
  
    # Used to flatted the array containing
    # the co-ordinates of the vertices.

    
    n = approx.ravel() 
    i = 0
    
    for j in n :
        if(i % 2 == 0):
            x = n[i]
            y = n[i + 1]
  
            # String containing the co-ordinates.
            string = str(x) + " " + str(y) 
  
            if(i == 0):
                # text on topmost co-ordinate.
                cv.putText(image_f, "#{}".format(c), (x, y),
                                font, 1, (0, 0, 255), 2) 
                c = c+1
        i = i + 1


#for c in range(len(cnt)):
#    cv.putText(rgb, "#{}".format(c), (200, 200),
#        cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)



#usar o rgb para a contagem

#print(type(rgb)) o rgb contém <class 'numpy.ndarray'>
#print(type(cnt)) é uma tupla
#print(type(len(cnt))) é um int. Numero de adipócitos
#print(type(hierarchy)) outro ndarray
#print(type(k))
#print(type(teste))
#print((x, y))



print("coins in the image : ", len(cnt))
cv.imwrite("contorno.jpg", rgb)
cv.imwrite("final.jpg",image_f)