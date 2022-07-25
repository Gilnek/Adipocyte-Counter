#!/usr/bin env python3
# -*- coding: utf-8 -*-
import os
import csv
import cv2 
import maxflow
import numpy as np
import tkinter as tk
import tkinter.messagebox

from PIL import Image
from tkinter import filedialog
from tkinter import colorchooser
from scipy.spatial import Delaunay


class Imagem:
   img = None
   path = None
   mask = []
   dados = []
   finalMask = None
   imgSaved = False

   measure_know = None
   measure_pix = None
   scale = None
   medUnit = None

   def __init__(self, path, image):
      self.path = path
      self.img = image
   
   def __del__(self):
      # print(len(self.mask))
      # for i in enumerate(self.mask):
      #    del self.mask[i]
      print("Destruindo imagem")


class GUI:
   window = None
   buttons = []
   img = None
   auxMask = None

   def __init__(self):
      self.window = tk.Tk()
      self.window.call('encoding', 'system', 'utf-8')
      self.window.resizable(False,False)

   def salvar(self):
      img = None

      resp = tkinter.messagebox.askquestion("Aviso",  "Deseja salvar o resultado atual?", icon = 'warning')
      
      if resp == 'yes':

         img = self.img

         path = os.path.normpath(img.path)
         list = path.split(os.sep)
         imageName = list[-1]
         name = list[-1].split(".")[0]
         folder = img.path.split(".")[0]

         if not os.path.exists(folder):
            os.mkdir(folder)

         for i in range(len(img.mask)):
            resize, _ = ImageProcessing.Contours(self, img.mask[i])
            file = img.mask[i].tipo + " " + imageName  
            image = cv2.cvtColor(resize, cv2.COLOR_BGR2RGB)
            im_pil = Image.fromarray(image)
            im_pil.save(folder + "/" + file)

         image = cv2.cvtColor(img.finalMask, cv2.COLOR_BGR2RGB)
         im_pil = Image.fromarray(image)
         im_pil.save(folder + "/final mask of " + imageName)

         nome = self.img.path.split("/")

         dados = []
         dados.append(["Area Total", "Porcentagem da Area Total", "Perimetro Total", nome[-1]])

         with open(folder + '/' + name + '.csv', 'a', encoding = 'utf-8') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(dados)
            for i in range(len(self.img.dados)):
               writer.writerow(self.img.dados[i])

         self.buttons[1]['state'] = tk.DISABLED
         self.img.imgSaved = True
      
   def select_image(self):

      file_path = filedialog.askopenfilename() # abre para selecionar arquivo

      if file_path: # se existir

         # No caso de ja ter uma imagem, mas modificações não foram salvas
         if self.img and len(self.img.mask) and self.img.imgSaved == False: 
            self.salvar()

         if self.img and len(self.img.mask):
            self.img.dados.clear()
            self.img.mask.clear()

         readImg = Image.open(file_path) # abre imagem
         numpyarray = np.array(readImg) # transforma em numpy
         img = cv2.cvtColor(numpyarray, cv2.COLOR_RGB2BGR) # converte de rgb para bgr(opencv)
         self.img = Imagem(file_path, img) # cria objeto de imagem
         self.imgAtual = file_path

         for i in range(len(self.buttons)):
            if i == 1:
               self.buttons[i]['state'] = tk.DISABLED
            else:
               self.buttons[i]['state'] = tk.ACTIVE  

   def help(self):
      tkinter.messagebox.showinfo("Instruções", 
      "Automatic Measure: \n" + 
      "Reconhece a escala automaticamente da imagem\n" +
      "O usuário precisa apenas digitar a distância conhecida\n\n"+
      "Segmentation: \n" + 
      "Opção de segmentação\n" +
      "Botão direito do mouse para riscar o que for plano de fundo (cor azul)\n" +
      "Botão esquerdo do mouse para riscar o que deseja segmentar (cor vermelho)\n")

   def img_frame(self):
      frame = tk.Frame(self.window)
      frame.pack(expand=True, fill="both")

      button_file = tk.Button(frame, text='File', padx=10, pady=3, command = lambda: self.select_image())
      self.buttons.append(button_file)

      button_save = tk.Button(frame, text='Save Images', padx=3, pady=3, state="disable", command = lambda: self.salvar())
      self.buttons.append(button_save)

      #button_measure = tk.Button(frame, text='Automatic Measure', padx=3, pady=3, state="disable", command = lambda: ImageProcessing.get_measure(self))
      #self.buttons.append(button_measure)

      #button_seg = tk.Button(frame, text='Segmentation', padx=3, pady=3, state="disable", command = lambda: ImageProcessing.GraphSegment(self))
      #self.buttons.append(button_seg)

      #button_showMask = tk.Button(frame, text='Show Mask', padx=3, pady=3, state="disable", command = lambda: ImageProcessing.showMask(self))
      #self.buttons.append(button_showMask)

      button_help = tk.Button(frame, text='Help', padx=3, pady=3, state="active", command = lambda: self.help())
      self.buttons.append(button_help) 

      button_file.grid(row=0, column=0)
      button_save.grid(row=0, column=1)
      #button_measure.grid(row=0, column=2)
      #button_seg.grid(row=0, column=3)
      #button_showMask.grid(row=0, column=4)
      button_help.grid(row=0, column=3)

      def close():
         if self.img and len(self.img.mask) and self.img.imgSaved == False: 
            self.salvar()
         exit()

      self.window.protocol("WM_DELETE_WINDOW", close)

      self.window.mainloop()