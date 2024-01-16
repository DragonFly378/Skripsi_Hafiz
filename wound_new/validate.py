import sys
import os
from tkinter import *
from PIL import Image
import numpy as np

import numpy as np
from PIL import Image

def calculate_accuracy(image_result_path, image_referensi_path):

    # Load images
    image_result = Image.open(image_result_path).convert("L")
    image_referensi = Image.open(image_referensi_path).convert("L")

    # print(image_referensi.size)
    # print(image_result.size)

    setSizeImg(image_referensi)
    image_referensi = image_referensi.resize((new_width, new_height)) # <-- untuk resize ukuran


    gambar1 = np.array(image_result)
    gambar2 = np.array(image_referensi)


    if gambar1.shape != gambar2.shape:
        gambar1 = np.array(image_result.resize(image_referensi.size).convert('L'))
        
    # print(gambar1.shape)
    # print(gambar2.shape)

    idx_black = np.where(gambar1 == 0)
    idx_white = np.where(gambar1 == 255)

    # print(len(gambar1[idx_zero]))


    difference = np.abs(gambar1 - gambar2)

    diff_image = Image.fromarray(difference)
    diff_image.save('diff.jpg')

    # print(gambar1)
    # print('\n')
    # print(gambar2)
    # Count the number of non-zero differences
    total_piksel_diff = np.count_nonzero(difference)

    # Calculate total number of pixels
    total_pixels = np.prod(gambar1.shape)
    # print(np.prod(gambar1.shape))
    # print(np.prod(gambar2.shape))



    # Calculate accuracy as a percentage
    accuracy = 100 - ((total_piksel_diff / total_pixels) * 100)
    # accuracy2 = ((total_pixels - total_piksel_diff) / total_pixels) * 100

    # print(accuracy)
    return round(accuracy, 2), total_piksel_diff, total_pixels


def setSizeImg(img):
    global new_width, aspect_ratio, new_height
    # set ukuran gambar
    # new_width = 480  # Atur ukuran hanya 480 px
    new_width = 320  # Atur ukuran hanya 320 px
    aspect_ratio = img.width / img.height
    new_height = int(new_width / aspect_ratio)


if __name__ == '__main__':
    # # Ini untuk menguji gambar satuan
    image_result_path = "results/luka_kuning/mask_r_25.jpg"
    image_referensi_path = "results/luka_kuning/25_r.jpg"
    # Panggil fungsi untuk mendapatkan akurasi
    akurasi, total_diff, total_piksel = calculate_accuracy(image_result_path, image_referensi_path)



    # # Ini untuk menguji banyak gambar sekaligus 
    # filesname_hitam = ["2", "4", "5", "6", "7", "8", "14", 
    #            "15", "17", "18", "19", "20", "22", "26", 
    #            "27", "28", "29", "33", "37", "40", "41", 
    #            "16", "31", "39"]

    # filesname_kuning = ["13", "17", "18", "19", "21", "23", "25", 
    #         "34", "35", "38", "42", "3", "12", "10", "16"]

    # filesname_merah = ["16", "17", "22", "24", "25", "30", "32", 
    #            "33", "37", "39", "42", "44", "2", "3", 
    #            "4", "6", "7", "8", "9", "10", "11", "12", "14", 
    #            "18", "19", "20", "23", "26", "29", "31", "35", "36", "38"]

    # akurasi = np.zeros(len(filesname_merah))
    # total_diff = np.zeros(len(filesname_merah))
    # total_piksel = np.zeros(len(filesname_merah))

    # for i in range(len(filesname_merah)):
    #     image_result_path = f"results/luka_merah/mask_r_{filesname_merah[i]}.jpg"
    #     image_referensi_path = f"results/luka_merah/{filesname_merah[i]}_r.jpg"
    #     accuracy, total_piksel_diff, total_pixels = calculate_accuracy(image_result_path, image_referensi_path)

    #     akurasi[i] = accuracy
    #     total_diff[i] = total_piksel_diff
    #     total_piksel[i] = total_pixels

    print(akurasi, '\n')
    print(total_diff, '\n')
    print(total_piksel, '\n')
