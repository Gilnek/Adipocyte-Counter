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
p2, p98 = np.percentile(gray, (2, 98))
img_rescale = exposure.rescale_intensity(gray, in_range=(p2, p98))

#binarização da imagem
thresh =  cv.adaptiveThreshold(img_rescale,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv.THRESH_BINARY,11,2)
cv.imwrite("threshteste3.jpg", thresh)

p2, p98 = np.percentile(denoise, (2, 98))
img_rescale = exposure.rescale_intensity(denoise, in_range=(p2, p98))

#binarização da imagem
threshdenoise =  cv.adaptiveThreshold(img_rescale,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv.THRESH_BINARY,11,2)
cv.imwrite("threshdenoiseteste3.jpg", threshdenoise)

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
#cv.imwrite("threshteste3.jpg", thresh)
#cv.imshow("gray", gray)
cv.waitKey()
  
cv.destroyAllWindows()