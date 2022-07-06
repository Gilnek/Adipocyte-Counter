#!/usr/bin env python3

import cv2 as cv
import numpy as np
import math
import matplotlib
import matplotlib.pyplot as plt
from skimage import data, img_as_float
from skimage import exposure
from skimage import morphology

#leitura da imagem
image = cv.imread("test1.jpg") 
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


kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3,3))
dilation = cv.dilate(canny,kernel,iterations = 1)
cv.imwrite("dilationcanny.jpg", dilation)

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

     

#remove = morphology.remove_small_objects(invert, 20)
#cv.imwrite("remove.jpg", remove)

#p2, p98 = np.percentile(denoise, (2, 98))
#img_rescale = exposure.rescale_intensity(denoise, in_range=(p2, p98))

#blur2 = cv.GaussianBlur(img_rescale, (11,11), 0)

#canny2 = cv.Canny(blur2, 0, 50)
#cv.imwrite("canny2.jpg", canny)

#binarização da imagem
#threshdenoise =  cv.adaptiveThreshold(canny2,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,\
#           cv.THRESH_BINARY,11,2)
#cv.imwrite("threshdenoiseteste3.jpg", threshdenoise)



cv.waitKey()
  
cv.destroyAllWindows()
