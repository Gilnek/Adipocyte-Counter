#!/usr/bin env python3

import cv2 as cv
import numpy as np
import math
import matplotlib
import matplotlib.pyplot as plt
from skimage import data, img_as_float
from skimage import exposure

#leitura da imagem
image = cv.imread("teste1.jpg") 
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
img_adapteq = exposure.equalize_adapthist(gray, clip_limit=0.03)

#binarização da imagem
thresh =  cv.adaptiveThreshold(img_adapteq,255,cv.ADAPTIVE_THRESH_MEAN_C,\
            cv.THRESH_BINARY,11,2)
cv.imwrite("threshteste4.jpg", thresh)

img_adapteq = exposure.equalize_adapthist(denoise, clip_limit=0.03)

#binarização da imagem
threshdenoise =  cv.adaptiveThreshold(img_adapteq,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv.THRESH_BINARY,11,2)
cv.imwrite("threshdenoiseteste4.jpg", threshdenoise)

#denoise = cv.fastNlMeansDenoising(thresh,
#    dst=None,
#    h=2,
#    templateWindowSize=7,
#    searchWindowSize=21
#)

kernel = np.ones((5,5),np.uint8)
opening = cv.morphologyEx(thresh, cv.MORPH_OPEN, kernel, iterations=4)
cv.imwrite("opening.jpg", opening)

#cv.imshow("denoise", denoise)
#cv.imwrite("threshteste4.jpg", thresh)
#cv.imshow("gray", gray)
cv.waitKey()
  
cv.destroyAllWindows()