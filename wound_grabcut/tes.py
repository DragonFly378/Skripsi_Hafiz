import sys
import numpy as np
from GMM import GaussianMixtureModels


F_BG = 0
F_FG = 1
F_PR_BG = 2
F_PR_FG = 3

gambar2 = np.array(
[
    [[159, 192, 201], [160, 193, 202], [162, 197, 207], [167, 203, 213], [166, 204, 216], [159, 198, 212], [158, 195, 199]],
    [[159, 192, 201], [156, 192, 200], [159, 194, 204], [163, 201, 213], [162, 201, 215], [152, 193, 208], [135, 177, 190]],
    [[156, 189, 198], [149, 185, 193], [150, 185, 195], [155, 193, 205], [157, 196, 210], [150, 191, 206], [142, 182, 187]],
    [[163, 197, 203], [152, 188, 196], [149, 184, 194], [153, 189, 199], [152, 192, 204], [146, 188, 201], [151, 189, 194]],
    [[150, 187, 191], [158, 195, 199], [160, 196, 202], [151, 189, 194], [145, 182, 190], [143, 182, 191], [145, 184, 198]],
    [[154, 191, 195], [158, 195, 199], [158, 195, 199], [150, 188, 192], [146, 184, 189], [150, 187, 195], [159, 194, 204]],
    [[151, 189, 194], [152, 190, 195], [149, 187, 192], [142, 182, 187], [142, 181, 189], [147, 186, 194], [132, 171, 186]],
    [[150, 187, 195], [146, 185, 193], [143, 182, 190], [141, 180, 188], [143, 182, 190], [147, 186, 195], [144, 185, 194]],
    [[150, 189, 198], [146, 187, 196], [144, 185, 194], [146, 187, 196], [148, 189, 198], [148, 188, 200], [152, 193, 208]],
    [[141, 180, 194], [140, 180, 192], [141, 180, 194], [145, 185, 197], [145, 184, 198], [142, 182, 194], [153, 189, 199]]
]
)

gambar = np.array([
    [[159, 192, 201], [160, 193, 202], [162, 197, 207], [167, 203, 213], [166, 204, 216], [159, 198, 212], [158, 195, 199]],
    [[159, 192, 201], [160, 192, 203], [163, 198, 208], [167, 204, 214], [169, 207, 216], [161, 198, 212], [150, 190, 205]],
    [[157, 190, 200], [152, 186, 196], [150, 185, 195], [157, 195, 207], [160, 200, 213], [153, 194, 208], [140, 182, 197]],
    [[165, 198, 204], [154, 189, 197], [150, 186, 196], [157, 194, 206], [155, 195, 208], [147, 189, 202], [150, 188, 203]],
    [[154, 191, 195], [162, 199, 203], [160, 197, 201], [155, 193, 205], [150, 188, 200], [144, 182, 194], [148, 186, 198]],
    [[150, 187, 195], [157, 194, 202], [158, 195, 203], [150, 188, 200], [146, 184, 196], [152, 189, 201], [161, 198, 210]],
    [[150, 187, 194], [155, 193, 200], [149, 187, 194], [142, 180, 188], [143, 181, 189], [152, 190, 198], [135, 173, 181]],
    [[151, 188, 195], [148, 186, 193], [142, 180, 187], [141, 179, 186], [144, 182, 189], [150, 188, 195], [146, 184, 191]],
    [[150, 189, 196], [146, 187, 194], [144, 185, 192], [146, 187, 194], [148, 189, 196], [148, 189, 196], [152, 193, 200]],
    [[142, 181, 188], [140, 179, 186], [141, 180, 187], [145, 184, 191], [145, 184, 191], [142, 181, 188], [153, 192, 199]]
], dtype=np.uint8)

gambar3 = np.array([
    [[78, 122, 231], [97, 193, 202], [162, 123, 207]],
    [[140, 186, 128], [42, 180, 187], [141, 179, 186]],
    [[129, 89, 186], [141, 156, 125], [145, 108, 191]]
])

beta = 0
gamma = 50
rows, cols, _= gambar.shape
komponen_piksel = np.zeros((rows,cols), dtype=np.uint32)
mask = np.zeros(gambar.shape[:2], dtype=np.uint8)
# gc = GrabCut(gambar, mask)
# ix, iy, x, y = 176, 47, 351, 189
# mask[iy:y, ix:x] = 1

def count_smoothness():
    left_diff_ = gambar3[:, 1:] - gambar3[:, :-1]
    upleft_diff_ = gambar3[1:, 1:] - gambar3[:-1, :-1]
    up_diff_ = gambar3[1:, :] - gambar3[:-1, :]
    upright_diff_ = gambar3[1:, :-1] - gambar3[:-1, 1:]
    # print(gambar3[:, 1:], '\n hadehcls \n', gambar3[:, :-1])
    print('left diff: \n', left_diff_)  
    print('Beta pertama: \n', beta)  

    print("square left: \n", np.square(left_diff_))


print('data gambar: ', gambar.shape)

def inisiasi_piksel():
    s_x, s_y, x, y = 1, 3, 5, 8
    mask[s_y:y, s_x:x] = F_PR_FG
    print(gambar.shape)
    print(mask)

    bg_idx = np.where(np.logical_or(
        mask == F_BG, mask == F_PR_BG
    ))

    fg_idx = np.where(np.logical_or(
        mask == F_FG, mask == F_PR_FG
    ))
    
    print('(pr_)bgd count: \n', bg_idx, '\n(pr_)fgd count: \n', fg_idx)
    print('(pr_)bgd count: ', bg_idx[1].size, '(pr_)fgd count:', fg_idx[1].size)

    print('inisiasi piksel selesai')

    return(bg_idx, fg_idx)



def init_assign_gmm():
    gmm_fg = GaussianMixtureModels(gambar[idx_fg])
    gmm_bg = GaussianMixtureModels(gambar[idx_bg])

    komponen_piksel[idx_fg] = gmm_fg.assign_component(gambar[idx_fg])
    komponen_piksel[idx_bg] = gmm_bg.assign_component(gambar[idx_bg])
    # print('Komponen piksel FG: %d, Komponen piksel BG: %d, Total komponen: %d' % (len(komponen_piksel[idx_fg]), len(komponen_piksel[idx_bg]), len(komponen_piksel)))
    
    print('inisiasi GMM selesai')


if __name__ == '__main__':
    count_smoothness()
    # idx_bg, idx_fg = inisiasi_piksel()
    # print('tes fg_idx: ',fg_idx)
    # init_assign_gmm()


