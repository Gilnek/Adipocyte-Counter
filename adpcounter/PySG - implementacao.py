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

class ImageProcessing:

   def get_measure(self):

      copy = None
      resize = None
      copy = self.img.img.copy()
      height, width = copy.shape[:2]

      if height > 673 and width > 507:
         resize = cv2.resize(copy, (0,0), fx=0.33, fy=0.33)
      else:
         resize = copy

      hsv = cv2.cvtColor(resize, cv2.COLOR_BGR2HSV)
      thresh=cv2.inRange(hsv, np.array([0, 0, 0]), np.array([180, 255, 50])) #preto
      edges = cv2.Canny(thresh, 50, 150, apertureSize=3)
      base = cv2.HoughLinesP(edges, 1, np.pi / 180, 80, minLineLength=1, maxLineGap=6)
      pixel_array = []
      pixel_length = 0
      
      if base is not None:
         for line in base:
            x1, y1, x2, y2 = line[0]
            cv2.line(resize, (x1, y1), (x2, y2), (0, 0, 255), 2)
            pixel_length = np.abs(x2 - x1)
            pixel_array.append(pixel_length)
         cv2.imshow("Medida", resize)

      def getMeasure():
         self.img.measure_pix = np.mean(pixel_array)
         self.img.measure_know = float(e.get())
         self.img.scale = self.img.measure_pix / self.img.measure_know
         self.img.medUnit = e2.get()

         print("Medida: %0.4f %0.4f %0.4f" %(self.img.measure_pix, self.img.measure_know, self.img.scale))
         print(self.img.medUnit)

         root.destroy()
         cv2.destroyAllWindows()

      root = tk.Tk()
      root.title("Medição")
      tk.Label(root, text="Medida \nConhecida").grid(row=0, column=0, padx=3, pady=3)
      e = tk.Entry(root)
      e.grid(row=0, column=1, padx=6, pady=3, columnspan=3)
      
      tk.Label(root, text="Unidade de \nMedida").grid(row=1, column=0, padx=3, pady=3)
      e2 = tk.Entry(root)
      e2.grid(row=1, column=1, padx=6, pady=2, columnspan=3)

      button = tk.Button(root, text='Salvar', command = getMeasure)
      button.grid(row=2, column=1, padx=3, pady=5)

      root.mainloop()

   def GraphSegment(self):

      def superpixels_info(img):                            # SLIC0
         slic = cv2.ximgproc.createSuperpixelSLIC(img, algorithm = 101, region_size=10, ruler = 20.0) 
         slic.iterate(10)
         slic.enforceLabelConnectivity(50)
         segments = slic.getLabels()    
         segments_ids = np.unique(segments)

         centers = np.array([np.mean(np.nonzero(segments==i), axis=1) for i in segments_ids])

         hsv = cv2.cvtColor(img.astype('float32'), cv2.COLOR_BGR2HSV)
         bins = [20, 20] # H = S = 20 quantidade de intervalos
         ranges = [0, 360, 0, 1] # H: [0, 360], S: [0, 1]
         colors_hists = np.float32([cv2.calcHist([hsv],[0, 1], np.uint8(segments==i), bins, ranges).flatten() for i in segments_ids]) # histograma de cor para cada superpixel

         # Triangulação de Delaunay - vizinhos
         tri = Delaunay(centers)

         return (centers, colors_hists, segments, tri.vertex_neighbor_vertices, slic.getLabelContourMask())

      # Retorna IDs de superpixels que forem FG e BG a partir das marcações
      def find_superpixels_under_marking(marking, superpixels):
         fg_segments = np.unique(superpixels[marking[:,:,0]!=255]) #superpixels que tiverem marcados com o vermelho
         bg_segments = np.unique(superpixels[marking[:,:,2]!=255]) #superpixels que tiverem marcados com o azul
         return (fg_segments, bg_segments)

      # Soma os histogramas para os superpixeis de dados IDs, normaliza
      def cumulative_histogram_for_superpixels(ids, histograms):
         h = np.sum(histograms[ids], axis=0)
         return h / h.sum()

      # Retorna mascara boolena de pixeis dos superixeis de dados IDs
      def pixels_for_segment_selection(superpixels_labels, selection):
         pixels_mask = np.where(np.isin(superpixels_labels, selection), True, False)
         return pixels_mask

      def normalize_histograms(histograms):
         return np.float32([h / h.sum() for h in histograms])

      def do_graph_cut(fgbg_hists, fgbg_superpixels, norm_hists, neighbors):
         num_nodes = norm_hists.shape[0]
         g = maxflow.Graph[float](num_nodes, num_nodes * 5)
         nodes = g.add_nodes(num_nodes)

         hist_comp_alg = cv2.HISTCMP_KL_DIV

         indptr, indices = neighbors
         for i in range(len(indptr)-1):
            N = indices[indptr[i]:indptr[i+1]] # lista de vizinhos dos superpixels
            hi = norm_hists[i]                 # histograma para centro
            for n in N:
               if (n < 0) or (n > num_nodes):
                  continue
               # Cria duas arestas (forwards e backwards) com a capacidade baseada na
               # combinação do histograma
               hn = norm_hists[n]             # histograma para vizinho
               g.add_edge(nodes[i], nodes[n], 20-cv2.compareHist(hi, hn, hist_comp_alg),
                                                20-cv2.compareHist(hn, hi, hist_comp_alg))

         # custo para FG/BG
         for i,h in enumerate(norm_hists):
            if i in fgbg_superpixels[0]:
                  g.add_tedge(nodes[i], 0, 1000) # FG - seta alto custo para BG
            elif i in fgbg_superpixels[1]:
                  g.add_tedge(nodes[i], 1000, 0) # BG - seta alto custo para FG
            else:
                  g.add_tedge(nodes[i], cv2.compareHist(fgbg_hists[0], h, hist_comp_alg),
                                       cv2.compareHist(fgbg_hists[1], h, hist_comp_alg))

         g.maxflow()

         return g.get_grid_segments(nodes)

      #Functionality for finding out the normalized graph cut segmented image.
      def Segmentation(img_marking, superpixels, color_hists, neighbors):

         fg_segments, bg_segments = find_superpixels_under_marking(img_marking, superpixels)

         fg_cumulative_hist = cumulative_histogram_for_superpixels(fg_segments, color_hists)
         bg_cumulative_hist = cumulative_histogram_for_superpixels(bg_segments, color_hists)

         fgbg_hists = [fg_cumulative_hist, bg_cumulative_hist]
         fgbg_superpixels = [fg_segments, bg_segments]
         
         norm_hists = normalize_histograms(color_hists)

         graph_cut = do_graph_cut(fgbg_hists, fgbg_superpixels, norm_hists, neighbors)

         segment_mask = pixels_for_segment_selection(superpixels, np.nonzero(graph_cut))

         mask = np.uint8(segment_mask * 255)

         self.auxMask = mask

         novo = resize.copy() # copia da imagem reajustada

         cv2.imshow('Máscara aplicada', cv2.bitwise_not(novo, novo, mask = mask))

      def interactive_drawing(event, x, y, flags, param):
         global current_former_x, current_former_y, drawing, left_button, counterL, counterR

         if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            current_former_x, current_former_y = x, y
            left_button = True
            counterL = 1

         elif event == cv2.EVENT_RBUTTONDOWN:
            drawing = True
            current_former_x, current_former_y = x, y
            left_button = False
            counterR = 1

         elif event == cv2.EVENT_MOUSEMOVE:
            if drawing == True:
               if left_button == True:
                  cv2.line(img_marking, (current_former_x, current_former_y), (x, y), (0, 0, 255), 5)
                  cv2.line(img_slic, (current_former_x, current_former_y), (x, y), (0, 0, 255), 5) # tela que vista pelo usuario
                  current_former_x, current_former_y = x, y

               if left_button == False:
                  cv2.line(img_marking, (current_former_x, current_former_y), (x, y), (255, 0, 0), 5)
                  cv2.line(img_slic, (current_former_x, current_former_y), (x, y), (255, 0, 0), 5)
                  current_former_x, current_former_y = x, y

         elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            counterL = 1
            if (counterL + counterR == 2):
               Segmentation(img_marking, superpixels, color_hists, neighbors)

         elif event == cv2.EVENT_RBUTTONUP:
            drawing = False
            counterR = 1
            if (counterL + counterR == 2):
               Segmentation(img_marking, superpixels, color_hists, neighbors)

         return x, y

      img = None
      copy = None
      resize = None
      global current_former_x, current_former_y, drawing, left_button, counterL, counterR

      img = self.img
      copy = img.img.copy()

      height, width = copy.shape[:2]

      if height > 673 and width > 507:
         resize = cv2.resize(copy, (0,0), fx=0.33, fy=0.33)
      else:
         resize = copy

      centers, color_hists, superpixels, neighbors, contours = superpixels_info(resize)

      mask_inv_slic = cv2.bitwise_not(contours) # contorno dos superpixels
      img_slic = cv2.bitwise_and(resize, resize, mask = mask_inv_slic) # imagem com os superpixels por cima

      img_marking = np.zeros(resize.shape, np.uint8) # inicializa array com o tamanho da imagem
      img_marking[:] = (255, 255, 255) # imagem em branco

      cv2.namedWindow('Markings')
      cv2.setMouseCallback('Markings', interactive_drawing)

      while(1):
         cv2.imshow('Markings', img_slic)
         k = cv2.waitKey(1) & 0xFF

         if cv2.getWindowProperty('Markings',cv2.WND_PROP_VISIBLE) < 1:    
            counterL = 0
            counterR = 0    
            ImageProcessing.saveMask(self)
            break 

      cv2.destroyAllWindows()

   def Contours(self, mask):
      copy = None
      resize = None

      copy = self.img.img.copy()

      height, width = copy.shape[:2]

      if height > 673 and width > 507:
         resize = cv2.resize(copy, (0,0), fx=0.33, fy=0.33)
      else:
         resize = copy

      r,g,b = mask.cor[0]

      contours, hierarchy = cv2.findContours(mask.mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
      cv2.drawContours(resize,contours, -1, (b,g,r), 3)

      mask.area = 0
      mask.perimetro = 0

      for i in range(len(contours)):
         mask.area += cv2.contourArea(contours[i])
         mask.perimetro += cv2.arcLength(contours[i], True)

      return resize, contours

   def saveMask(self):

      cv2.destroyAllWindows()

      copy = None
      resize = None

      copy = self.img.img.copy()

      height, width = copy.shape[:2]

      if height > 673 and width > 507:
         resize = cv2.resize(copy, (0,0), fx=0.33, fy=0.33)
      else:
         resize = copy

      mask = Mask()

      def getMeasure():

         if len(self.auxMask):
            mask.tipo = e.get()     
            mask.mask = self.auxMask    
            self.img.mask.append(mask)
            self.img.mask[-1].cor = colorchooser.askcolor(title ="Cor da Mascara")

            ImageProcessing.Contours(self, self.img.mask[-1])

            root.destroy()

            cv2.waitKey()
            cv2.destroyAllWindows()

      root = tk.Tk()
      root.title("Mascara")
      tk.Label(root, text="Nome da mascara").grid(row=0, column=0, padx=3, pady=3)
      e = tk.Entry(root)
      e.grid(row=0, column=1, padx=3, pady=3)
      button = tk.Button(root, text='Salvar', padx=3, pady=3, command = getMeasure)
      button.grid(row=0, column=2)

      root.mainloop()

   def showMask(self):

      copy = None
      resize = None

      copy = self.img.img.copy()
      height, width = copy.shape[:2]

      if height > 673 and width > 507:
         resize = cv2.resize(copy, (0,0), fx=0.33, fy=0.33)
      else:
         resize = copy

      for i in range(len(self.img.mask)):
         r,g,b = self.img.mask[i].cor[0]
         _, contours = ImageProcessing.Contours(self, self.img.mask[i])
         cv2.drawContours(resize, contours, -1, (b,g,r), 3)

      self.img.finalMask = resize

      cv2.imshow('Máscaras', resize)

      root = tk.Tk()
      root.title("Máscaras")
      root.geometry("350x400")
      my_listbox = tk.Listbox(root, width=20)
      my_listbox.pack(pady = 5)
      my_listbox.configure(justify=tk.CENTER)

      for i in range(len(self.img.mask)):
         my_listbox.insert("end", self.img.mask[i].tipo)
         my_listbox.itemconfig(i, background = self.img.mask[i].cor[1])

      my_text = tk.Text(root, height = 10, width = 45)
      my_text.pack()

      def select():
         my_text.delete(1.0, tk.END)  

         for i in range(len(self.img.mask)):
            if self.img.mask[i].tipo == my_listbox.get(tk.ANCHOR): 

               ImageProcessing.Contours(self, self.img.mask[i]) 

               my_text.insert("end", str(self.img.mask[i].tipo)+ "\n")

               areatot = self.img.mask[i].area/self.img.scale

               my_text.insert("end", "Área Total = %0.4f %s2\n" %(areatot, self.img.medUnit))
               size = self.img.mask[i].mask.shape[0]*self.img.mask[i].mask.shape[1]
               
               porceArea = cv2.countNonZero(self.img.mask[i].mask)/size*100
               
               my_text.insert("end", "Porcentagem da Área Total = %0.4f %%\n" %(porceArea))

               periTot = self.img.mask[i].perimetro/self.img.scale

               my_text.insert("end", "Perímetro Total = %0.4f %s\n" %(periTot,  self.img.medUnit))               

               self.img.dados.append([areatot, porceArea, periTot])

               break

      button = tk.Button(root, text='Dados', command = select)
      button.pack(pady = 3, padx = 3)

      self.buttons[1]["state"] = tk.ACTIVE
      self.img.imgSaved = False

      root.mainloop()

class Mask:
   tipo = None
   mask = None
   cor = None
   area = 0
   perimetro = 0

   def __del__(self):
      print(str(self.cor) + " Destruindo mascaras")

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

      button_measure = tk.Button(frame, text='Automatic Measure', padx=3, pady=3, state="disable", command = lambda: ImageProcessing.get_measure(self))
      self.buttons.append(button_measure)

      button_seg = tk.Button(frame, text='Segmentation', padx=3, pady=3, state="disable", command = lambda: ImageProcessing.GraphSegment(self))
      self.buttons.append(button_seg)

      button_showMask = tk.Button(frame, text='Show Mask', padx=3, pady=3, state="disable", command = lambda: ImageProcessing.showMask(self))
      self.buttons.append(button_showMask)

      button_help = tk.Button(frame, text='Help', padx=3, pady=3, state="active", command = lambda: self.help())
      self.buttons.append(button_help) 

      button_file.grid(row=0, column=0)
      button_save.grid(row=0, column=1)
      button_measure.grid(row=0, column=2)
      button_seg.grid(row=0, column=3)
      button_showMask.grid(row=0, column=4)
      button_help.grid(row=0, column=5)

      def close():
         if self.img and len(self.img.mask) and self.img.imgSaved == False: 
            self.salvar()
         exit()

      self.window.protocol("WM_DELETE_WINDOW", close)

      self.window.mainloop()

if __name__ == '__main__':

   drawing=False
   current_former_x = 0
   current_former_y = 0

   left_button = True
   counterL = 0
   counterR = 0

   gui = GUI().img_frame() # inicializa a janela inicial

   cv2.destroyAllWindows()