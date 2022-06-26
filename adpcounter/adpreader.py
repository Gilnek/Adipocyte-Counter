#!/usr/bin env python3

import cv2 as cv
import numpy as np
import math 
from imutils import paths
import argparse
import os
from pathlib import Path

from adpcount import adp_count


#leitura da imagem

parser = argparse.ArgumentParser()
parser.add_argument('dir',nargs='?',help='Caminho para o diretorio com imagens .jpg',type=str,default='.')
args = parser.parse_args()


dir_path = args.dir

dir_imgs = [x for x in os.listdir(dir_path) if '.jpg' in x]
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

#print('Insira o nome da imagem desejada: ')
#input(image_name)
#image_name = args.img


image_path = "teste.jpg"
#image = cv.imread(str(image_path.resolve()))
#original = image.copy()  #cria uma cópia da original para comparação e se torna a original

resultado = adp_count(image_path)
print(resultado[0])

cv.imwrite("resultado.png",resultado[1])


#print('Insira o nome da imagem desejada: ')
#input(image_name)
#image_name = args.img


image_path = "teste.jpg"
#image = cv.imread(str(image_path.resolve()))
#original = image.copy()  #cria uma cópia da original para comparação e se torna a original

resultado = adp_count(image_path)
print(resultado[0])

cv.imwrite("resultado.png",resultado[1])
