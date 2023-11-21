import sys
from tkinter import *
from tkinter import ttk, filedialog
# import tkinter as tk
from grabcut import GrabCut
# from tkinter import PhotoImage
from PIL import Image, ImageTk, ImageMath, ImageDraw
import numpy as np

ix, iy, x, y = 176, 47, 351, 189

# print("titik kotak [ix, iy, x, y]: ",[ix, iy, x, y])


def setSizeImg(img):
    global new_width, aspect_ratio, new_height
    # set ukuran gambar
    new_width = 360  # Atur ukuran hanya 480 px
    aspect_ratio = img.width / img.height
    new_height = int(new_width / aspect_ratio)


if __name__ == '__main__':
    root = Tk()
    root.title("Bahan")
    root.title("Hasil")

    # Import image
    filename = "2.jpg"
    gambar = Image.open(filename)

    gambar = np.array(gambar)
    gambar2 = gambar.copy()
    print(gambar)
    print(gambar.shape)
    mask = np.zeros(gambar.shape[:2], dtype=np.uint8)
    mask2 = mask.copy()

    gc = GrabCut(gambar2, mask2)

    # mask[iy:y, ix:x] = 1
    mask = np.where((mask2 == 1) | (mask2 == 3), 255, 0).astype('uint8')
    gambar = Image.fromarray(gambar)
    setSizeImg(gambar)

    # window image
    gambar = gambar.resize((new_width, new_height))
    gambar_tk = ImageTk.PhotoImage(gambar)
    gambar_label = ttk.Label(root, image=gambar_tk)
    gambar_label.pack()

    # window output
    mask_img = Image.fromarray(mask) 
    mask_img = mask_img.resize((new_width, new_height))
    mask_tk = ImageTk.PhotoImage(mask_img)
    mask_label = ttk.Label(root, image=mask_tk)
    mask_label.pack()

    # Perform the bitwise AND operation with a mask
    result_img = Image.composite(gambar, Image.new("RGB", gambar.size, "black"), mask_img)

    # Save or display the result image
    # result_image.show()
    result_tk = ImageTk.PhotoImage(result_img)
    result_label = ttk.Label(root, image=result_tk)
    result_label.pack()


    root.mainloop()