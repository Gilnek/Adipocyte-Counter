#!/usr/bin/env python3

import cv2 as cv
import numpy as np

def dist_transform_plus_thresh(thresh_proportion: int = 0.125 ,write: bool = False):
    floodfilled = cv.imread("floodfilled.jpg")

    ff_gray = cv.cvtColor(floodfilled, cv.COLOR_BGR2GRAY)

    ff_dist = cv.distanceTransform(ff_gray, cv.DIST_L2, 0)
    if write: cv.imwrite("ff_dist.png", ff_dist)

    ret, ff_bin = cv.threshold(ff_dist, thresh_proportion*ff_dist.max(), 255, 0)
    if write: cv.imwrite("ff_bin.png", ff_bin)

    return ff_dist, ff_bin

ff_dist, ff_bin = dist_transform_plus_thresh(0.130, False)

image = cv.imread("floodfilled.jpg")

(cnt, hierarchy) = cv.findContours(
    ff_bin.copy().astype(np.uint8), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)
cv.drawContours(rgb, cnt, -1, (0, 255, 0), 2)


print("coins in the image : ", len(cnt))
cv.imwrite("contorno.jpg", rgb)