import numpy as np
import matplotlib.pyplot as plt

x = np.arange(30).reshape((3, 5, 2))
y = np.pad(x, ((1,1), (1,1), (0,0)), 'constant', constant_values=0)

print(y.shape)