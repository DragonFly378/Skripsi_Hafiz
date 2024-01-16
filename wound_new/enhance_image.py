import sys
import os
from tkinter import *
from PIL import Image, ImageTk, ImageOps, ImageDraw
import numpy as np

class EnhanceImage:
    def __init__(self, root, image_path, image_name, category):
        self.root = root
        self.root.title("Image Enhance") 
        self.image_path = image_path
        self.image_name = image_name
        self.category = category


        self.gambar_gc = Image.open(self.image_path)
        self.run()
        self.display_image()
        self.save_result_image()
    
    def run(self):
        self.mask = self.gambar_gc.convert("L")
        self.mask = np.array(self.mask)
        # print(self.gambar_gc[100:180,100:147])


        # Change pixel values
        self.mask[self.mask == 0 ] = 255
        self.mask[(self.mask > 100) | (self.mask <= 20)] = 255
        self.mask[self.mask != 255 ] = 0

        self.mask_image = Image.fromarray(self.mask)
        self.mask_negative = ImageOps.invert(self.mask_image)
        self.result_image = Image.composite(self.gambar_gc, Image.new("RGB", self.gambar_gc.size, "black"), self.mask_negative)


    def display_image(self):
        # Convert the NumPy array back to ImageTk format
        gambar_mask = ImageTk.PhotoImage(Image.fromarray(self.mask))
        gambar_ori = ImageTk.PhotoImage(self.gambar_gc)
        gambar_mask_negative = ImageTk.PhotoImage(self.mask_negative)
        gambar_final = ImageTk.PhotoImage(self.result_image)

        # Create a Label widget to display the updated image
        label_mask_enhance = Label(self.root, image=gambar_mask)
        label_mask_enhance.image = gambar_mask  # Keep a reference to the image to prevent it from being garbage collected

        label_image_gc = Label(self.root, image=gambar_ori)
        label_image_gc.image = gambar_ori  # Keep a reference to the image to prevent it from being garbage collected
        
        label_mask_negative = Label(self.root, image=gambar_mask_negative)
        label_mask_negative.image = gambar_mask_negative  # Keep a reference to the image to prevent it from being garbage collected
    
        label_img_final = Label(self.root, image=gambar_final)
        label_img_final.image = gambar_final  # Keep a reference to the image to prevent it from being garbage collected
    

        label_image_gc.pack()
        label_mask_enhance.pack()
        # label_mask_negative.pack()
        label_img_final.pack()


    def save_result_image(self):
        save_to_tulisan = f"../docs/latex/gambar/hasil_segmentasi/{self.category}"
        save_folder = f"results/{self.category}"

        # Create the folder if it doesn't exist
        os.makedirs(save_folder, exist_ok=True)
        os.makedirs(save_to_tulisan, exist_ok=True)

        result_filename = f"result_enhance_{self.image_name}.jpg"
        mask_filename = f"mask_r_enhance_{self.image_name}.jpg"

        self.mask_image.save(os.path.join(save_to_tulisan, mask_filename))
        self.result_image.save(os.path.join(save_to_tulisan, result_filename))
        
        self.mask_image.save(os.path.join(save_folder, mask_filename))
        self.result_image.save(os.path.join(save_folder, result_filename))

        print("Result image saved successfully:")




if __name__ == '__main__':
    root = Tk()
    category = "luka_hitam"
    img_name = "result_4"
    extension = ".jpg"
    image_path = "results/"+category+"/"+img_name+extension
    ehance_image = EnhanceImage(root, image_path, img_name, category)
    root.mainloop()
