import sys
from image_editing import ImageEditing
# from tkinter import ttk, filedialog, PhotoImage
from tkinter import *
from grabcut import GrabCut
from PIL import Image, ImageTk, ImageMath, ImageDraw
import numpy as np

if __name__ == '__main__':
    root = Tk()
    category = "luka_hitam"
    img_name = "39"
    extension = ".jpg"
    image_path = "dataset_3/"+category+"/bahan/"+img_name+extension
    tools = ImageEditing(root, image_path, img_name, category)
    root.mainloop()