import sys
import numpy as np
import cv2 as cv
from GMM import GaussianMixture



DRAW_BG = {'val': 0}
DRAW_FG = {'val': 1}
DRAW_PR_BG = {'val': 2}
DRAW_PR_FG = {'val': 3}

img = np.array(
[
    [[1,2,3], [4,5,6], [7,8,9], [10,11,12], [13,14,15] ],
    [[16,17,18], [12,29,21], [21,23,24], [12,44,17], [32,23,22] ],
    [[11,89,14], [23,41,11], [23,75,12], [13,47,27], [24,81,21] ],
    [[21,79,24], [24,42,41], [23,65,92], [14,45,37], [44,83,12] ],
    [[31,69,34], [12,43,31], [27,25,12], [51,55,57], [34,85,45] ],
    [[41,19,44], [23,24,51], [28,55,32], [16,54,67], [64,30,33] ],
    [[51,29,54], [33,25,61], [29,35,52], [31,31,77], [39,20,62] ],
    [[61,49,64], [43,26,81], [45,25,62], [19,33,87], [32,80,82] ],
]
)

rows, cols, _= img.shape
comp_idxs = np.zeros((rows,cols), dtype=np.uint32)
mask = np.zeros(img.shape[:2], dtype=np.uint8)  # mask initialized to PR_BG

print(img.shape)
print(mask, '\n')


mask[2:6,1:4] = DRAW_PR_FG['val']
print(mask, '\n')

bgd_indexes = np.where(np.logical_or(
    mask == DRAW_BG['val'], mask == DRAW_PR_BG['val']))

fgd_indexes = np.where(np.logical_or(
    mask == DRAW_FG['val'], mask == DRAW_PR_FG['val']))


print('(pr_)bgd count: ', bgd_indexes, '\n \n(pr_)fgd count: ', fgd_indexes)
print('(pr_)bgd count: ', bgd_indexes[0].size, '(pr_)fgd count:', fgd_indexes[0].size, '\n')

# print("ini bgd_indexes : ", img[bgd_indexes])
# print("ini fgd_indexes : ", img[fgd_indexes], '\n')

'''Init GMM'''

bgd_gmm = GaussianMixture(img[bgd_indexes])
print('\n \n \n')
fgd_gmm = GaussianMixture(img[fgd_indexes])



"""Step 1: Assign GMM"""
print("comp idxs awal: ", bgd_indexes)
print("comp idxs awal: ", fgd_indexes)

print('comp idxs untuk bgd')
# comp_idxs[bgd_indexes] = bgd_gmm.which_component(img[bgd_indexes])
# print('\n comp idxs untuk fgd')
# comp_idxs[fgd_indexes] = fgd_gmm.which_component(img[fgd_indexes])


