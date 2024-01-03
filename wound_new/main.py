import sys
from image_editing import ImageEditing
# from tkinter import ttk, filedialog, PhotoImage
from tkinter import *
from grabcut import GrabCut
from PIL import Image, ImageTk, ImageMath, ImageDraw
import numpy as np

if __name__ == '__main__':
    root = Tk()
    kategori = "luka_hitam"
    img_name = "2.jpg"
    image_path = "dataset_3/"+kategori+"/ready/"+img_name
    tools = ImageEditing(root, image_path)
    root.mainloop()