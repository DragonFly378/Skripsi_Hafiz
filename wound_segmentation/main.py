import sys
import os
from image_editing import ImageEditing
from tkinter import Tk, filedialog, Entry, Label, Button
from grabcut import GrabCut
from PIL import Image, ImageTk, ImageMath, ImageDraw
import numpy as np

def load_image():
    file_path = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select Image File", filetypes=(("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*")))
    file_name = os.path.basename(file_path)
    img_name, extension = os.path.splitext(file_name)

    print("Image name:", img_name)
    print("Extension:", extension)    
    return img_name, extension, file_path

def submit_category(entry):
    name = entry.get()
    return name


def getCategrory(root):
    label = Label(root, text="Masukan kategori luka (cth: luka_merah)")
    label.pack()
    entry = Entry(root)
    entry.pack()
    button = Button(root, text="Submit", command=lambda: root.quit())
    button.pack()
    
    root.mainloop()  # Wait for the user to enter the category
    return submit_category(entry)
    

if __name__ == '__main__':
    root = Tk()


    # category_name = "luka_hitam"
    # category_name = "luka_kuning"
    # category_name = "luka_merah"
    # img_name = "2"
    # extension = ".jpg"
    # image_path = "dataset_3/"+category+"/bahan/"+img_name+extension

    category_name = getCategrory(root)
    img_name, extension, image_path = load_image()
    print(category_name, ' ', img_name, ' ', extension)
    tools = ImageEditing(root, image_path, img_name, category_name)
    root.mainloop()

