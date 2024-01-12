import tkinter as tk
from PIL import Image, ImageTk, ImageOps
import os

def convert_to_negative(image_path, save_folder, save_to_tulisan, mask_negative_filename):
    # Open the image using Pillow
    original_image = Image.open(image_path)

    # Convert the image to grayscale
    gray_image = ImageOps.grayscale(original_image)

    # Invert the grayscale image to create a negative
    negative_image = ImageOps.invert(gray_image)
    
    os.makedirs(save_folder, exist_ok=True)
    os.makedirs(save_to_tulisan, exist_ok=True)

    negative_image.save(os.path.join(save_folder, mask_negative_filename))
    negative_image.save(os.path.join(save_to_tulisan, mask_negative_filename))

# Replace "path/to/your/image.jpg" with the actual path to your image
image_name = "37"
arr_img = [2,4,5,6,7,8,14,15,17,18,19,20,22,26,27,28,29,33,37]
save_folder = f"results/luka_hitam"
save_to_tulisan = f"../docs/latex/gambar/hasil_segmentasi/luka_hitam"


for img_name in arr_img:
    image_path = f"results/luka_hitam/mask_{img_name}.jpg"
    mask_r_filename = f"mask_r_{img_name}.jpg"
    convert_to_negative(image_path, save_folder, save_to_tulisan, mask_r_filename)