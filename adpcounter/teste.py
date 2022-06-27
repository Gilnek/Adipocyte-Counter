#!/usr/bin env python3

import cv2 as cv
import numpy as np
import math

image = cv.imread("teste.jpg")
original = image.copy()
#transformação da imagem para escala de cinza
gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
cv.imwrite("gray.jpg", gray)

#binarização da imagem
thresh =  cv.adaptiveThreshold(gray,255,cv.ADAPTIVE_THRESH_MEAN_C,\
            cv.THRESH_BINARY,11,2)
cv.imwrite("thresh.jpg", thresh)

#engrossa a imagem
kernel = np.ones((2,2),np.uint8)
dilation = cv.dilate(thresh,kernel,iterations = 1)
cv.imwrite("dilation.jpg", dilation)

#afina a imagem
erosion = cv.erode(dilation,kernel,iterations = 2)
cv.imwrite("erosion.jpg", erosion)


mask = erosion
cv.imwrite("mask.jpg", mask)

kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3,3))
opening = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel, iterations=2)
close = cv.morphologyEx(opening, cv.MORPH_CLOSE, kernel, iterations=2)
cv.imwrite("close.jpg", close)

cnts = cv.findContours(close, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]



area_min = 1  #60
area_med = 5000 #550
area_conexao = 1000 #500
adipocitos = 0

#faz os contornos
for c in cnts:
    area = cv.contourArea(c)
    if area > area_min:
        cv.drawContours(original, [c], -1, (36,255,12), 2)
        if area > area_conexao:
            adipocitos += math.ceil(area / area_med)
        else:
            adipocitos += 1
print('Numero de Adipócitos: {}'.format(adipocitos))

cv.imwrite("original.png", original)
