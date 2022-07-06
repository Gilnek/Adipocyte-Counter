#!/usr/bin/env python3
import cv2 as cv
import numpy as np

def remove_small_noise(invert):
# Filter using contour area and remove small noise
    #invert = cv.imread("invert.jpg")

    cnts = cv.findContours(invert, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        area = cv.contourArea(c)
        if area < 5500:
            cv.drawContours(invert, [c], -1, (0,0,0), -1)

    # Morph close and invert image
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (5,5))
    close = 255 - cv.morphologyEx(invert, cv.MORPH_CLOSE, kernel, iterations=2)

    cv.imwrite('limpoinvert.jpg', invert)
    cv.imwrite('limpoclose.jpg', close)

    return invert,close