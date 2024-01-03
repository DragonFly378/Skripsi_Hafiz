import os
import numpy as np
import matplotlib.pyplot as plt
from skimage.io import imread

file = "luka_hitam/ready/39_g.jpg"
img_path, img_file = os.path.split(file)
img_name, img_extension = os.path.splitext(img_file)
img = imread(file) # print(img.shape) # h x w
print(img.shape)
outname = img_path + "/" + img_name + "_init" + img_extension

jari_jari = 170

s = np.linspace(0, 2*np.pi, 200)
r = 260 + jari_jari*np.sin(s)
c = 265 + jari_jari*np.cos(s)
init = np.array([r, c]).T

my_dpi = 96 #https://www.infobyip.com/detectmonitordpi.php

fig= plt.figure(frameon=False, figsize=(img.shape[1]/my_dpi, img.shape[0]/my_dpi), dpi=my_dpi)
ax = fig.add_axes([0, 0, 1, 1])
ax.imshow(img, cmap=plt.cm.gray)
ax.plot(init[:, 1], init[:, 0], '--r', lw=3)
ax.set_xticks([]), ax.set_yticks([]) # hide axes
ax.axis('off')


plt.show()
