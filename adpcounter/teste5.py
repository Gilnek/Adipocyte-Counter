#!/usr/bin env python3

import cv2 as cv
import numpy as np
import math
import matplotlib
import matplotlib.pyplot as plt
from skimage import data, img_as_float
from skimage import exposure

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


kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5,5))
dilation = cv.dilate(canny,kernel,iterations = 1)
cv.imwrite("dilationcanny.jpg", dilation)

#binarização da imagem
thresh =  cv.adaptiveThreshold(canny,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv.THRESH_BINARY,11,2)
cv.imwrite("threshteste3.jpg", thresh)

kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3,3))

erosion = cv.erode(thresh, kernel,iterations = 1)
cv.imwrite("erosionteste5.jpg", erosion)

p2, p98 = np.percentile(denoise, (2, 98))
img_rescale = exposure.rescale_intensity(denoise, in_range=(p2, p98))

blur2 = cv.GaussianBlur(img_rescale, (11,11), 0)

canny2 = cv.Canny(blur2, 0, 50)
cv.imwrite("canny2.jpg", canny)

#binarização da imagem
threshdenoise =  cv.adaptiveThreshold(canny2,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv.THRESH_BINARY,11,2)
cv.imwrite("threshdenoiseteste3.jpg", threshdenoise)



cv.waitKey()
  
cv.destroyAllWindows()