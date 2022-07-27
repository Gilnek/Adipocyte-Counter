#!/usr/bin env python3

import cv2 as cv
from cv2 import imwrite, imread
import numpy as np
from PySide6.QtGui import QAction, QPixmap
from skimage import exposure

def gray_scale_transformation(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    return gray

def contrast_stretching(gray):
    p2, p98 = np.percentile(gray, (2, 98))
    img_rescale = exposure.rescale_intensity(gray, in_range=(p2, p98))

    return img_rescale

def blur(img_rescale):
    blur = cv.GaussianBlur(img_rescale, (11,11), 0)

    return blur

def canny_edge(blur):
    canny = cv.Canny(blur, 0, 50)

    return canny

def gaussian_threshold(canny):
    thresh =  cv.adaptiveThreshold(canny,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv.THRESH_BINARY,11,2)

    return thresh

def erode(thresh):
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3,3))
    erosion = cv.erode(thresh, kernel,iterations = 1)

    return erosion

def remove_small_objects(erosion):
    invert = cv.bitwise_not(erosion)
    # Filter using contour area and remove small noise
    cnts = cv.findContours(invert, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        area = cv.contourArea(c)
        if area < 5500:
            cv.drawContours(invert, [c], -1, (0,0,0), -1)

    return invert

def closing(invert):
    # Morph close and invert image
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (5,5))
    close = 255 - cv.morphologyEx(invert, cv.MORPH_CLOSE, kernel, iterations=2)
    cv.imwrite("tempclose.png", close)

    return close

def flood_fill(close, image):
    pad = cv.copyMakeBorder(close, 1,1,1,1, cv.BORDER_CONSTANT, value=255)
    h, w = pad.shape

    mascara = np.zeros([h + 2, w + 2], np.uint8)

    # floodfill outer white border with black
    img_floodfill = cv.floodFill(pad, mascara, (0,0), 0, (5), (0), flags=8)[1]

    # remove border
    img_floodfill = img_floodfill[1:h-1, 1:w-1]

    # save cropped image
    cv.imwrite('floodfilled.jpg',img_floodfill)

    (cnt, hierarchy) = cv.findContours(
        img_floodfill.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    cv.drawContours(rgb, cnt, -1, (0, 255, 0), 2)

    num_area = 0

    # Get the moments
    mu = [None for i in cnt]
    for i in range(len(cnt)):
        mu[i] = cv.moments(cnt[i])
    # Get the mass centers
    mc = [None for i in cnt]
    for i in range(len(cnt)):
        mc[i] = (mu[i]['m10'] / (mu[i]['m00'] + 1e-5), mu[i]['m01'] / (mu[i]['m00'] + 1e-5))
    # Draw contours
    #drawing = np.zeros((src_thresh.shape[0], src_thresh.shape[1], 3), dtype=np.uint8)
    area = 0
    for i, j in enumerate(cnt):
        #colour = cnt[i]['bgr']
        #cv.drawContours(drawing, contours, i, colour, 2)
        area = area + int(cv.contourArea(cnt[i]))
    
    print('Area: {0} pixels'.format(area)) 
 
    cv.imwrite("contorno_celula.jpg", rgb)

    
    return img_floodfill, rgb

def processed_image():
    close= imread("processed.png")
    close = cv.cvtColor(close, cv.COLOR_BGR2GRAY)
    close = cv.adaptiveThreshold(close,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,\
               cv.THRESH_BINARY,11,2)

    return close

 
def dist_transform_plus_thresh(thresh_proportion: int = 0.110 ,write: bool = False):
    floodfilled = cv.imread("floodfilled.jpg")
    
    ff_gray = cv.cvtColor(floodfilled, cv.COLOR_BGR2GRAY)

    ff_dist = cv.distanceTransform(ff_gray, cv.DIST_L2, 0)
    if write: cv.imwrite("ff_dist.png", ff_dist)

    ret, ff_bin = cv.threshold(ff_dist, thresh_proportion*ff_dist.max(), 255, 0)
    if write: cv.imwrite("ff_bin.png", ff_bin)

    return ff_dist, ff_bin

def count_it(ff_dist, ff_bin, processed_image, contorno: str = "contorno.png", final: str = "final.png"):

    ff_dist, ff_bin = dist_transform_plus_thresh(0.130, False)

    image = cv.imread("floodfilled.jpg")

    (cnt, hierarchy) = cv.findContours(
        ff_bin.copy().astype(np.uint8), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    cv.drawContours(rgb, cnt, -1, (0, 255, 0), 2)
    image_f = processed_image

    c = 1
    #cv.drawContours(rgb, cnt, -1, (0, 255, 0), 2)
    font = cv.FONT_HERSHEY_COMPLEX
    # Going through every contours found in the image.
    for cnts in cnt :
    
        approx = cv.approxPolyDP(cnts, 0.009 * cv.arcLength(cnts, True), True)
  
        # draws boundary of contours.
        cv.drawContours(rgb, cnt, -1, (0, 255, 0), 2) 

        
  
        # Used to flatted the array containing
        # the co-ordinates of the vertices.

    
        n = approx.ravel() 
        i = 0
    
        for j in n :
            if(i % 2 == 0):
                x = n[i]
                y = n[i + 1]
  
                # String containing the co-ordinates.
                string = str(x) + " " + str(y) 
  
                if(i == 0):
                    # text on topmost co-ordinate.
                    cv.putText(image_f, "#{}".format(c), (x, y),
                                    font, 1, (0, 0, 255), 2) 
                    c = c+1
            i = i + 1

        cv.imwrite(contorno, rgb)    
        cv.imwrite(final,image_f)
    return len(cnt)

def cv2pix(image):
    imwrite("temp.png", image)
    converted = QPixmap()
    converted.load("temp.png")
    return converted

def pix2cv(image:QPixmap):
    image.save("temp.png")
    converted = imread("temp.png")
    return converted