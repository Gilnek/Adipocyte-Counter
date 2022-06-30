#!/usr/bin env python3

import cv2 as cv
import numpy as np
import math

#leitura da imagem
image = cv.imread("teste1.jpg") 
original = image.copy()
#transformação da imagem para escala de cinza
gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
cv.imwrite("gray.jpg", gray)

#geracao do elemento estruturante para aplicacao do filtro
kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5,5))
#aplicacao da erosao antes da binarizacao
erosion = cv.erode(gray, kernel,iterations = 1)
cv.imwrite("erosion1.jpg", gray)

#aplicacao da dilatacao antes da binarizacao
dilation = cv.dilate(gray,kernel,iterations = 1)
cv.imwrite("dilation1.jpg", dilation)

#aqui faz a comparaçao entre elas

resultimage = np.zeros((2040, 1536))
#feita a operacao de uma erosao-dilatacao 
new = (erosion - dilation)*4
#new = cv.normalize(((erosion - dilation)), resultimage, 50, 0, cv.NORM_MINMAX)
#new = cv.normalize(new, resultimage, 50, 125, cv.NORM_MINMAX)
#feita a operacao de uma dilatacao-erosao
new2 = (dilation - erosion)*4
#new2 = cv.normalize(new2, resultimage, 50, 125, cv.NORM_MINMAX)

# new  = erosion-dilation
# new2 = dilation-erosion
# new3 = operacao da transladacao do new2
# new4 = operacao da transladacao do new
# new5 = echo 



cv.imwrite("new.jpg", new)
cv.imwrite("new2.jpg", new2)

# Store height and width of the image
height, width = new.shape[:2]

T = np.float32([[1, 0, 1], [0, 1, 1]])
new_translation = cv.warpAffine(new, T, (width, height))
#cv.imshow("Originalimage", new2)
#cv.imshow('Translation', new2_translation)

new4 = (new_translation + new)
new4 = cv.normalize(new4, resultimage, 75, 150, cv.NORM_MINMAX)
cv.imwrite("new4.jpg", new4)

# Store height and width of the image
height, width = new2.shape[:2]

T = np.float32([[1, 0, 1], [0, 1, 1]])
new2_translation = cv.warpAffine(new2, T, (width, height))
#cv.imshow("Originalimage", new2)
#cv.imshow('Translation', new2_translation)

new3 = (new2_translation + new2)
new3 = cv.normalize(new3, resultimage, 75, 150, cv.NORM_MINMAX)
cv.imwrite("new3.jpg", new3)

ksize = 5,5
dilero = cv.blur(new3, ksize)
cv.imwrite("dileroblur.jpg", dilero)

ksize = 5,5
erodil = cv.blur(new4, ksize)
cv.imwrite("erodilblur.jpg", erodil)

medianerodil = cv.bilateralFilter(new3, 9, 75, 75)
cv.imshow("medianerodil", medianerodil)
medianadilero = cv.bilateralFilter(new4, 9, 75, 75)
cv.imshow("medianadilero", medianadilero)

cv.waitKey()
  
cv.destroyAllWindows()


#laplacianerodil = cv.Laplacian(erodil,cv.CV_64F)
#cv.imshow("laplacianerodil", laplacianerodil)

#laplaciandilero = cv.Laplacian(dilero,cv.CV_64F)
#cv.imshow("laplaciandilero", laplaciandilero)



#binarização da imagem
thresh =  cv.adaptiveThreshold(erodil,255,cv.ADAPTIVE_THRESH_MEAN_C,\
            cv.THRESH_BINARY,11,2)
cv.imwrite("thresh.jpg", thresh)

#engrossa a imagem
kernel = np.ones((2,2),np.uint8)
dilation = cv.dilate(thresh,kernel,iterations = 1)
cv.imwrite("dilation2.jpg", dilation)

#afina a imagem
erosion = cv.erode(dilation,kernel,iterations = 2)
cv.imwrite("erosion2.jpg", erosion)


mask = erosion
cv.imwrite("mask.jpg", mask)

kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (7,7))
opening = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel, iterations=1)
close = cv.morphologyEx(opening, cv.MORPH_CLOSE, kernel, iterations=1)
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
