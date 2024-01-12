# import numpy as np

# res_gc = 8396
# res_cv = 0

# percent = (res_cv - res_gc) / res_cv * 100
# res_accurate = 100 - np.abs(percent) 

# if res_accurate < 0:
#     res_accurate = 0

# print(res_accurate)

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
    
    gambar1 = np.array(image_result)
    gambar2 = np.array(image_referensi)


    if gambar1.shape != gambar2.shape:
        gambar2 = np.array(image_referensi.resize(image_result.size).convert('L'))
        
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
    # print(total_piksel_diff)

    # Calculate accuracy as a percentage
    accuracy = 100 - ((total_piksel_diff / total_pixels) * 100)
    accuracy2 = ((total_pixels - total_piksel_diff) / total_pixels) * 100

    # print(accuracy2)
    return round(accuracy, 2), total_piksel_diff, total_pixels


# # Ganti nama file gambar yang ingin Anda bandingkan
# image_result_path = "results/luka_hitam/mask_r_2.jpg"
# image_referensi_path = "results/luka_hitam/2_r.jpg"
# # Panggil fungsi untuk mendapatkan akurasi
# calculate_accuracy(image_result_path, image_referensi_path)


filesname_hitam = ["2", "4", "5", "6", "7", "8", "14", 
           "15", "17", "18", "19", "20", "22", "26", 
           "27", "28", "29", "33", "37", "40", "41", 
           "16", "31", "39"]

akurasi = np.zeros(len(filesname_hitam))
total_diff = np.zeros(len(filesname_hitam))
total_piksel = np.zeros(len(filesname_hitam))

for i in range(len(filesname_hitam)):
    image_result_path = f"results/luka_hitam/mask_r_{filesname_hitam[i]}.jpg"
    image_referensi_path = f"results/luka_hitam/{filesname_hitam[i]}_r.jpg"
    accuracy, total_piksel_diff, total_pixels = calculate_accuracy(image_result_path, image_referensi_path)

    akurasi[i] = accuracy
    total_diff[i] = total_piksel_diff
    total_piksel[i] = total_pixels

print(akurasi)
print(total_diff)
print(total_piksel)
