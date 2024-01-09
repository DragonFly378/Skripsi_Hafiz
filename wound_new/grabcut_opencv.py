#!/usr/bin/env python
'''
===============================================================================
Interactive Image Segmentation using GrabCut algorithm.

This sample shows interactive image segmentation using grabcut algorithm.

USAGE:
    python grabcut.py <filename>

README FIRST:
    Two windows will show up, one for input and one for output.

    Press 'n' to segment the object (once or a few times)
For any finer touch-ups, you can press any of the keys below and draw lines on
the areas you want. Then again press 'n' for updating the output.

Key 'n' - To update the segmentation
Key 'r' - To reset the setup
Key 's' - To save the results
===============================================================================
'''

# Python 2/3 compatibility
from __future__ import print_function

import numpy as np
import cv2 as cv
import os

BLUE = [255,0,0]        # rectangle color
RED = [0,0,255]         # PR BG
GREEN = [0,255,0]       # PR FG
BLACK = [0,0,0]         # sure BG
WHITE = [255,255,255]   # sure FG

DRAW_BG = {'color' : BLACK, 'val' : 0}
DRAW_FG = {'color' : WHITE, 'val' : 1}
DRAW_PR_BG = {'color' : RED, 'val' : 2}
DRAW_PR_FG = {'color' : GREEN, 'val' : 3}

# setting up flags
rect = (0,0,1,1)
drawing = False         # flag for drawing curves
rectangle = False       # flag for drawing rect
rect_or_mask = 100      # flag for selecting rect or mask mode
value = DRAW_FG         # drawing initialized to FG
thickness = 3           # brush thickness

if __name__ == '__main__':

    # print documentation
    print(__doc__)

    category = "luka_hitam"
    img_name = "33"
    rect =  (98, 53, 133, 98)
    extension = ".jpg"
    image_path = "dataset_3/"+category+"/bahan/"+img_name+extension

    img = cv.imread(image_path)
    img = cv.resize(img, (320, int(img.shape[0] * 320 / img.shape[1])))  # Resize the image to width 480 pixels
    img2 = img.copy()                               # a copy of original image
    mask = np.zeros(img.shape[:2],dtype = np.uint8) # mask initialized to PR_BG
    output = np.zeros(img.shape,np.uint8)           # output image to be shown

    # input and output windows
    cv.namedWindow('output')
    cv.namedWindow('input')
    # cv.setMouseCallback('input',onmouse)
    cv.moveWindow('input',img.shape[1]+10,90)

    print(" Instructions: \n")
    print(" Silahkan tekan tombol n untuk menjalankan segmentasi\n")

    while(1):

        cv.imshow('output',output)
        cv.imshow('input',img)
        k = cv.waitKey(1)

        # key bindings
        if k == 27:         # esc to exit
            break
        elif k == ord('s'): # save image
            bar = np.zeros((img.shape[0],5,3),np.uint8)
            # res = np.hstack((img2,bar,img,bar,output))
            res = np.hstack((bar,output))
            save_to_tulisan = f"../docs/latex/gambar/hasil_segmentasi/{category}"
            save_folder = f"results/{category}"
            
            file_path = os.path.join(save_folder, f"result_{img_name}_cv.jpg")
            file_path_tulisan = os.path.join(save_to_tulisan, f"result_{img_name}_cv.jpg")

            cv.imwrite(file_path,res)
            cv.imwrite(file_path_tulisan,res)
            print(" Result saved as image \n")
        elif k == ord('r'): # reset everything
            print("resetting \n")
            rect = (0,0,1,1)
            drawing = False
            rectangle = False
            rect_or_mask = 100
            value = DRAW_FG
            img = img2.copy()
            mask = np.zeros(img.shape[:2],dtype = np.uint8) # mask initialized to PR_BG
            output = np.zeros(img.shape,np.uint8)           # output image to be shown
        elif k == ord('n'): # segment the image
            print(""" For finer touchups, mark foreground and background after pressing keys 0-3
            and again press 'n' \n""")
            print(rect)
            bgdmodel = np.zeros((1,65),np.float64)
            fgdmodel = np.zeros((1,65),np.float64)
            cv.grabCut(img2,mask,rect,bgdmodel,fgdmodel,1,cv.GC_INIT_WITH_RECT)
            # Extract the probable foreground and probable background from the mask
            probable_foreground = (mask == 1) | (mask == 3)
            probable_background = (mask == 0) | (mask == 2)

            # Get the number of pixels classified as foreground and background
            foreground_len = np.sum(probable_foreground)
            background_len = np.sum(probable_background)
            print("Foreground Pixels: ", foreground_len)
            print("Background Pixels: ", background_len)
            print("Total Pixels: ", img.shape[0] * img.shape[1])
            rect_or_mask = 1
           
        mask2 = np.where((mask==1) + (mask==3),255,0).astype('uint8')
        output = cv.bitwise_and(img2,img2,mask=mask2)

    cv.destroyAllWindows()
