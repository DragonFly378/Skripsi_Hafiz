import numpy as np
x = np.array([[1,2,0,5,6],[4,2,3,5,5],[1,5,5,5,5]])
print(x)
z = np.where(np.logical_or(x == 0, x == 5))
print(np.logical_or(x == 0, x == 5))
print(z)