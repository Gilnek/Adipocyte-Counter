#!/usr/bin/env python3
import cv2
import numpy as np
import math
from imutils import paths
import argparse

#le a imagem
image = cv2.imread("chromosome.png")
original = image.copy()

#transforma pra escala de cinza
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imwrite("gray.png", gray)

#binariza a imagem
thresh =  cv2.threshold(gray, 0, 255,
    cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
cv2.imwrite("thresh.png", thresh)

#engrossa? a imagem
kernel = np.ones((2,2),np.uint8)
dilation = cv2.dilate(thresh,kernel,iterations = 1)
cv2.imwrite("Dilationog.png", dilation)

#afina a imagem
erosion = cv2.erode(dilation,kernel,iterations = 2)
cv2.imwrite("Erosion.png", erosion)

#engorssa? novamente
dilation = cv2.dilate(erosion,kernel,iterations = 2)
cv2.imwrite("Dilation.png", dilation)

#afina dnv
erosion = cv2.erode(dilation,kernel,iterations = 1)
cv2.imwrite("Erosionf.png", erosion)

mask = erosion
cv2.imwrite("mask.png", mask)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
close = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=2)


cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

num = 0
idx = 0
for c in cnts:
    x,y,w,h = cv2.boundingRect(c)
    idx+=1
    new_img=image[y:y+h,x:x+w]
    cv2.imwrite(str(num) + "_" + str(idx) + '.png', new_img)

area_min = 60  #60
area_med = 550 #550
area_conexao = 1000 #500
cromossomos = 0

#faz os contornos
for c in cnts:
    area = cv2.contourArea(c)
    if area > area_min:
        cv2.drawContours(original, [c], -1, (36,255,12), 2)
        if area > area_conexao:
            cromossomos += math.ceil(area / area_med)
        else:
            cromossomos += 1
print('Cromossomos: {}'.format(cromossomos))

cv2.imwrite("close.png", close)
cv2.imwrite("original.png", original)
cv2.imwrite("filename.png", close)

#cv2.waitKey()