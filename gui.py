#!/usr/bin/env python3
from tkinter import filedialog
import cv2 as cv
from tkinter import *
from PIL import Image, ImageTk, ImageDraw, ImageGrab
import PIL
import numpy as np

app = Tk()
app.title("SCAP") #Software para Contagem de Adipocitos em Python
app.geometry("1240x720")


def get_x_and_y(event):
    global lasx, lasy 
    lasx, lasy = event.x, event.y

def draw_smth(event):
    global lasx, lasy
    canvas.create_line((lasx, lasy, event.x, event.y), fill='black', width= 5)    
    lasx, lasy = event.x, event.y


canvas = Canvas(app, bg='black')
canvas.pack(anchor='nw', fill='both', expand=1)

canvas.bind("<Button-1>", get_x_and_y)
canvas.bind("<B1-Motion>", draw_smth)

image = Image.open("limpoclose.jpg")
image = image.resize((1240,720), Image.Resampling.LANCZOS)
pimage = ImageTk.PhotoImage(image)
canvas.create_image(0,0, image=pimage, anchor='nw')

app.mainloop()

image.save('vadiaputa.png','png')

# from pprint import pprint
# pprint(type(image._PhotoImage__photo))
# pprint(image._PhotoImage__photo.__dir__())

def getter(widget):
    x=app.winfo_rootx()+widget.winfo_x()
    y=app.winfo_rooty()+widget.winfo_y()
    x1=x+widget.winfo_width()
    y1=y+widget.winfo_height()
    ImageGrab.grab().crop((x,y,x1,y1)).save("file path here")


#opencv_image=cv.cvtColor(numpy_image, cv.COLOR_)
#cv.imwrite("final.png", opencv_image)