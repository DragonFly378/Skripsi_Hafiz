import numpy as np

res_gc = 8396
res_cv = 0

percent = (res_cv - res_gc) / res_cv * 100
res_accurate = 100 - np.abs(percent) 

if res_accurate < 0:
    res_accurate = 0

print(res_accurate)

