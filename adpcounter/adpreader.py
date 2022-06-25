#!/usr/bin env python3

import cv2 as cv
import numpy as np
import math 
from imutils import paths
import argparse
import os
from pathlib import Path


#leitura da imagem

parser = argparse.ArgumentParser()
parser.add_argument('dir',nargs='?',help='Caminho para o diretorio com imagens .png',type=str,default='.')
args = parser.parse_args()


dir_path = args.dir

dir_imgs = [x for x in os.listdir(dir_path) if '.png' in x]
dir_imgs.sort()

base_path = Path(dir_path)

print(f'Diretorio selecionado: {base_path.resolve()}')
if dir_imgs is None or len(dir_imgs) == 0:
	print('Este diretório não possui imagens.')
	exit(0)
print('Imagens do Diretório:')
for i in dir_imgs:
	print(i)
input('Pressione ENTER para continuar.')

image_name = args.img


image_path = base_path/image_name
image = cv.imread(str(image_path.resolve()))
original = image.copy()  #cria uma cópia da original para comparação e se torna a original

#transformação da imagem para escala de cinza
gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
cv.imshow(gray)

#binarização da imagem
thresh =  cv.threshold(gray, 0, 255,
    cv.THRESH_BINARY_INV | cv.THRESH_OTSU)[1]

#engrossa a imagem
kernel = np.ones((2,2),np.uint8)
dilation = cv.dilate(thresh,kernel,iterations = 1)
#cv.imwrite("Dilation.png", dilation)

#afina a imagem
erosion = cv.erode(dilation,kernel,iterations = 2)
#cv.imwrite("Erosion.png", erosion)


mask = erosion
cv.imwrite("mask.png", mask)

kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3,3))
opening = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel, iterations=1)
close = cv.morphologyEx(opening, cv.MORPH_CLOSE, kernel, iterations=2)


cnts = cv.findContours(close, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

num = 0
idx = 0
for c in cnts:
    x,y,w,h = cv.boundingRect(c)
    idx+=1
    new_img=image[y:y+h,x:x+w]
    cv.imwrite(str(num) + "_" + str(idx) + '.png', new_img)

area_min = 60  #60
area_med = 550 #550
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

cv.imwrite("close.png", close)
cv.imwrite("original.png", original)
cv.imwrite("filename.png", close)