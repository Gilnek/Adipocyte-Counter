from datetime import datetime
from pathlib import Path
import numpy as np
import pandas as pd
import cv2
import argparse
import math
import os

#import traceback, sys, code

__LEN_FRONTIER_THRESH = 50

def rotate(cl,cc,state):
		#__state = state % 8 + 1
	if state == 1 or state == 8:
		cl-=1
	elif state == 2 or state == 3:
		cc+=1
	elif state == 4 or state == 5:
		cl+=1
	elif state == 6 or state == 7:
		cc-=1
	state = state % 8 + 1
	return (cl,cc,state)

def fronteira(initial,mask):
	#print('\tdebug: entering fronteira')
	coords = []
	_lin,_col = mask.shape
	_l,_c = borda = initial
	cl = _l
	cc = _c-1
	__state = 1
	__state_breaker = __state
	while (cl < 0 or cc < 0 or cl >= _lin or cc >= _col) or mask[cl][cc] == 255:
		cl,cc,__state = rotate(cl,cc,__state)
		if __state_breaker == __state:
			coords.append(initial)
			return coords
	t = (cl,cc)
	(cl,cc) = borda
	borda = t
	__state = ((__state + 3) % 8) + 1
	cl,cc,__state = rotate(cl,cc,__state)
	while borda != initial:
		coords.append(borda)
		__state_breaker = __state
		while (cl < 0 or cc < 0 or cl >= _lin or cc >= _col) or mask[cl][cc] == 255:
			cl,cc,__state = rotate(cl,cc,__state)
			if __state_breaker == __state:
				break
		t = (cl,cc)
		(cl,cc) = borda
		borda = t
		__state = ((__state + 3) % 8) + 1
		cl,cc,__state = rotate(cl,cc,__state)
		pass
	coords.append(initial)
	return coords

def fronteira2recorte(borda:list):
	#print('\tdebug: entering recorte')
	if len(borda) == 0:
		return []
	
	b = list(borda)
	b.sort(key=lambda linha: linha[0])
	lin, min_c = b[0]
	max_c = min_c
	r = []
	for e in b[1:]:
		__l,__c = e
		if __l == lin:
			if __c > max_c:
				max_c = __c
			elif __c < min_c:
				min_c = __c
			pass
		else:
			r.append((lin,min_c,max_c))
			lin = __l
			min_c = max_c = __c
			pass
		pass
	r.append((lin,min_c,max_c))
	return r

def remove_from_mask(recorte:list,mask):
	#print('\tdebug: entering removing mask')
	for e in recorte:
		lin,minc,maxc = e
		for c in range(minc,maxc+1):
			mask[lin][c] = 255
			pass
		pass
	return mask

def img_from_cut(recorte:list,source_image):
	#print('\tdebug: entering img_from_cut')
	q_max_l = recorte[-1][0]
	q_min_l = recorte[0][0]
	q_max_c = max(recorte,key=lambda col:col[2])[2]
	q_min_c = min(recorte,key=lambda col:col[1])[1]
	#exit('degub')
	blank_size = (q_max_l-q_min_l+3,q_max_c-q_min_c+3)
	blank = np.zeros((blank_size[0],blank_size[1],3),np.uint8)
	blank[:][:] = (255,255,255)

	for e in recorte:
		lin,minc,maxc = e
		for c in range(minc,maxc+1):
			blank[lin-q_min_l+1][c-q_min_c+1] = source_image[lin][c]
			pass
		pass
	return blank

def img_from_frontier(borda:list):
	img_max_l = max(borda,key=lambda lin:lin[0])[0]
	img_min_l = min(borda,key=lambda lin:lin[0])[0]
	img_max_c = max(borda,key=lambda col:col[1])[1]
	img_min_c = min(borda,key=lambda col:col[1])[1]

	blank_size = (img_max_l-img_min_l+3,img_max_c-img_min_c+3)
	blank = np.zeros((blank_size[0],blank_size[1],3),np.uint8)
	blank[:][:] = (255,255,255)

	for point in borda:
		tl = point[0] - img_min_l + 1
		tc = point[1] - img_min_c + 1
		blank[tl][tc] = (0,0,255)

	return blank

def main():
	parser = argparse.ArgumentParser()
	#parser.add_argument('-t','--thresh',help='threshold value for image binarization',type=int,default=240)
	parser.add_argument('dir',nargs='?',help='Caminho para o diretorio com imagens .png',type=str,default='.')
	#parser.add_argument()
	args = parser.parse_args()

	props = []
	white = [255,255,255]
	thresh = 240
	# try:
	# 	thresh = args.thresh
	# except:
	# 	pass

	dir_path = args.dir

	dir_imgs = [x for x in os.listdir(dir_path) if '.png' in x]
	dir_imgs.sort()

	base_path = Path(dir_path)

	print(f'Diretorio selecionado: {base_path.resolve()}')
	if dir_imgs is None or len(dir_imgs) == 0:
		print('Não foram encontradas imagens .png nesse diretorio.')
		exit(0)
	print('Imagens presentes:')
	for i in dir_imgs:
		print(i)
	input('Pressione ENTER para continuar.')

	#subdir = datetime.now().strftime('%H_%M_%S')
	#(base_path/subdir).mkdir()

	for image_name in dir_imgs:# para cada imagem
		print(f'\nAnalizando {image_name}')
		image_path = base_path/image_name
		source_image = cv2.imread( str(image_path.resolve()) )
		if source_image is None:
			exit(f"Erro ao abrir imagem {image_name}.")

		
		gray = cv2.cvtColor(source_image,cv2.COLOR_BGR2GRAY)
		thresh, mask = cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY)
		blur = cv2.blur(mask,(7,7))
		thresh, mask = cv2.threshold(blur, thresh, 255, cv2.THRESH_BINARY)
		
		# run through mask and find objects
		found_valid = 0
		found_noise = 0
		found_obj = 0
		valid_objects = []
		peri = []

		rows,cols = mask.shape
		for row in range(0,rows):
			for col in range(0,cols):
				if mask[row][col] == 0:#objeto encontrado
					# salva ponto encontrado como initialPoint
					initialPoint = (row,col)
					#print(f'\tEncontrado objeto {found_obj:4d} em {initialPoint}')
					# pegamos a borda/fronteira do objeto
					frontier = fronteira(initial=initialPoint,mask=mask)
					# a partir da borda criamos uma lista contendo os intervalos que a imagem ocupa em cada linha (linha,inicial,final)
					r = fronteira2recorte(borda=frontier)
					# verificamos se a borda tem um tamanho minimo, para descartar ruidos
					if len(frontier) > __LEN_FRONTIER_THRESH:
						print(f'\tEncontrado objeto {found_valid:4d} em {initialPoint}')
						# encontramos um objeto valido na imagem
						#print(f'\tvalid object {found_valid:3d}')
						# copiamos o objeto para uma imagem
						out_image = img_from_cut(recorte=r,source_image=source_image)
						valid_objects.append(out_image)
						# criamos uma imagem com a borda do objeto desenhado
						per_image = img_from_frontier(frontier)
						peri.append(per_image)
						####
						p_rows,p_cols,_ = out_image.shape
						p_white_pixels =  np.count_nonzero(np.all(out_image==white,axis=2))
						p_area = (p_rows * p_cols) - p_white_pixels
						p_perimetro = len(frontier)
						p_perimetro2= p_perimetro**2
						p_C = p_perimetro2 / p_area
						p_R = 4 * math.pi * p_area / p_perimetro2
						p_De = 2 * math.sqrt(p_area/math.pi)
						data = [image_name,found_valid,p_perimetro,p_area,f'{p_C:.5f}',f'{p_R:.5f}',f'{p_De:.5f}']
						props.append(data)
						####
						#cv2.imwrite(f'out_{found_valid}.png', out_image)
						cv2.imwrite( str((base_path/f'{image_name.split(".")[0]}_{found_valid}.png').resolve()) , out_image)
						#cv2.imwrite(f'{found_valid}_P.png',per_image)
						cv2.imwrite( str((base_path/f'{image_name.split(".")[0]}_{found_valid}_P.png').resolve()) ,per_image)
						
						found_valid += 1
					else:
						#print(f'\tnoise object {found_noise:3d}')
						found_noise += 1
					found_obj += 1
					mask = remove_from_mask(recorte=r,mask=mask)
					pass# if
				pass# for col
			pass# for row
		print(f'Encontrado um total de {found_valid} objetos na imagem {image_name}.')
		pass# for image
	df_props = pd.DataFrame(props,columns=['Imagem','SubImagem', 'Perimetro', 'Area', 'Compacidade', 'Circularidade', 'Diametro Efetivo'])
	df_props.to_csv( str((base_path/'propriedades.csv').resolve()) )
	pass# main

if __name__ == "__main__":
	try:
		main()
		#print(f'erros na fronteira{shithappened:5d}')

	except Exception as err:# inicia uma shell IDLE dentro do frame onde o codigo foi a merda
		print(err)
		# type, value, tb = sys.exc_info()
		# traceback.print_exc()
		# last_frame = lambda tb=tb: last_frame(tb.tb_next) if tb.tb_next else tb
		# frame = last_frame().tb_frame
		# ns = dict(frame.f_globals)
		# ns.update(frame.f_locals)
		# code.interact(local=ns)
		pass
	pass
