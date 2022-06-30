#!/usr/bin env python3

import cv2 as cv
import numpy as np
import math

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


#binarização da imagem
thresh =  cv.adaptiveThreshold(denoise,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv.THRESH_BINARY,11,2)


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
cv.imwrite("denoise.jpg", denoise)
#cv.imshow("gray", gray)
cv.waitKey()
  
cv.destroyAllWindows()