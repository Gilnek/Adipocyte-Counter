#!/usr/bin/env python3

import cv2 as cv
import numpy as np

def floodfillfunc(image, close):

    #image = cv.imwrite("1.jpg")
    #close = cv.imwrite("close.jpg")

    pad = cv.copyMakeBorder(close, 1,1,1,1, cv.BORDER_CONSTANT, value=255)
    h, w = pad.shape

    mascara = np.zeros([h + 2, w + 2], np.uint8)

    # floodfill outer white border with black
    img_floodfill = cv.floodFill(pad, mascara, (0,0), 0, (5), (0), flags=8)[1]

    # remove border
    img_floodfill = img_floodfill[1:h-1, 1:w-1]

    # save cropped image
    cv.imwrite('floodfilled.jpg',img_floodfill)

    (cnt, hierarchy) = cv.findContours(
        img_floodfill.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    cv.drawContours(rgb, cnt, -1, (0, 255, 0), 2)
 
    #print("coins in the image : ", len(cnt))
    cv.imwrite("contorno.jpg", rgb)

    return rgb