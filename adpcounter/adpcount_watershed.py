#!/usr/bin env python3


import cv2 as cv
from cv2 import imwrite
import numpy as np
import math
from typing import Any, Tuple
from pathlib import Path

def adp_count_watershed(
        image_path: Path | str,
        return_image = True,
        img_gray: str | None = "gray.png",
        img_thresh: str | None = "threshold.png",
        img_mask: str | None = "mask.png"
        ) -> Tuple[int,Any|None]:
    original = cv.imread(image_path)
    image = original.copy()

    #transformação da imagem para escala de cinza
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    if img_gray is not None:
        cv.imwrite(img_gray, gray)
    #print(type(gray))

    #engrossa a imagem
    kernel = np.ones((2,2),np.uint8)
    dilation = cv.dilate(gray,kernel,iterations = 1)
    cv.imwrite("dilation.jpg", dilation)

    #binarização da imagem
    # #blur = cv.GaussianBlur(gray, (11,11), 0)
    # ret, thresh =  cv.threshold(gray,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
    # thresh = cv.adaptiveThreshold(gray,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,\
    #         cv.THRESH_BINARY,11,2)
    thresh = cv.adaptiveThreshold(
        src=gray,
        maxValue=255,
        adaptiveMethod=cv.ADAPTIVE_THRESH_GAUSSIAN_C,
        thresholdType=cv.THRESH_BINARY,
        blockSize=11,
        C=2,
        # dts=...
    )
    if img_thresh is not None:
        cv.imwrite(img_thresh, thresh)

    #### Watershed starts here
    ## remoção de ruido
    ws_kernel = np.ones((3,3),np.uint8)
    ws_opening = cv.morphologyEx(
        thresh, cv.MORPH_OPEN,
        ws_kernel,
        iterations=1
    )
    cv.imwrite("wsnr.png",ws_opening)
    ## sure bg
    ws_sure = cv.dilate(ws_opening, ws_kernel, iterations=0)
    cv.imwrite("ws_surebg.png", ws_sure)
    ## sure fg
    ws_dist_transform = cv.distanceTransform(ws_opening, cv.DIST_L2, 0)
    cv.imwrite("ws_dist.png", ws_dist_transform)
    # valores tirados do alem, for now
    ret, ws_surebg = cv.threshold(ws_dist_transform, 0.7 * ws_dist_transform.max(), 255, 0)
    cv.imwrite("ret.png", ws_surebg)
    ##

    # and ends here

    #engrossa a imagem
    kernel = np.ones((2,2),np.uint8)
    dilation = cv.dilate(thresh,kernel,iterations = 1)

    #afina a imagem
    erosion = cv.erode(dilation,kernel,iterations = 2)
    opening = cv.morphologyEx(erosion, cv.MORPH_OPEN, kernel)

    mask = opening
    if img_mask is not None:
        cv.imwrite(img_mask, mask)

    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3,3))
    opening = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel, iterations=1)
    close = cv.morphologyEx(opening, cv.MORPH_CLOSE, kernel, iterations=2)

    cnts = cv.findContours(close, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    area_min = 50  #60
    area_med = 75 #550
    area_conexao = 500 #500
    adipocitos = 0

    #faz os contornos
    for c in cnts:
        area = cv.contourArea(c)
        if area > area_min:
            cv.drawContours(image, [c], -1, (36,255,12), 2)
            if area > area_conexao:
                adipocitos += math.ceil(area / area_med)
            else:
                adipocitos += 1

    return adipocitos, image if return_image else None