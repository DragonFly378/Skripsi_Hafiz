import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from skimage.io import imread


# DataFrame -> luka_hitam, luka_kuning, luka_merah
df = pd.read_csv('luka_merah.csv')
datapath = "luka_merah/ready/"

# parameter plot
num_of_sample = 200
my_dpi = 96 # https://www.infobyip.com/detectmonitordpi.php

for index,row in df.iterrows():
    
    filename = str(row["filename"])

    img = imread(datapath + filename + "." + row["extension"])
    
    # snake init
    s = np.linspace(0, 2*np.pi, num_of_sample)
    r = row["center_r"] + row["radius"]*np.sin(s)
    c = row["center_c"] + row["radius"]*np.cos(s)
    init = np.array([r, c]).T

    # plot snake_init
    fig= plt.figure(frameon=False, figsize=(img.shape[1]/my_dpi, img.shape[0]/my_dpi), dpi=my_dpi)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.imshow(img, cmap=plt.cm.gray)
    ax.plot(init[:, 1], init[:, 0], '--r', lw=3)
    ax.set_xticks([]), ax.set_yticks([]) # hide axes
    ax.axis('off')
    
    outname = datapath + filename + "_init" + "." + row["extension"]

    plt.savefig(outname, dpi=my_dpi)
    print(outname + " has been saved")
    plt.close(fig)
