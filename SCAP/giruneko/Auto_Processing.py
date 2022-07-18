#!/usr/bin env python3

import cv2 as cv
import numpy as np
from skimage import exposure


#leitura da imagem
image = cv.imread("13 - CON NS F - L1C1 Q1.jpg") 
original = image.copy()
#transformação da imagem para escala de cinza
gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

denoise = cv.fastNlMeansDenoising(gray,
    dst=None,
    h=3,
    templateWindowSize=7,
    searchWindowSize=21
)

#contrast streaching
p2, p98 = np.percentile(gray, (2, 98))
img_rescale = exposure.rescale_intensity(gray, in_range=(p2, p98))

blur = cv.GaussianBlur(img_rescale, (11,11), 0)

canny = cv.Canny(blur, 0, 50)
cv.imwrite("canny.jpg", canny)

#binarização da imagem
thresh =  cv.adaptiveThreshold(canny,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv.THRESH_BINARY,11,2)
cv.imwrite("threshteste3.jpg", thresh)

kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3,3))
erosion = cv.erode(thresh, kernel,iterations = 1)
cv.imwrite("erosionteste5.jpg", erosion)

invert = cv.bitwise_not(erosion)


# Filter using contour area and remove small noise
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
 
 
print("coins in the image : ", len(cnt))
cv.imwrite("contorno.jpg", rgb)

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

(cnt, hierarchy) = cv.findContours(
    ff_bin.copy().astype(np.uint8), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)
cv.drawContours(rgb, cnt, -1, (0, 255, 0), 2)


print("adps in the image : ", len(cnt))
cv.imwrite("contorno.jpg", rgb)
