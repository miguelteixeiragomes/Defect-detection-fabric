import numpy as np
import pylab as pl
from scipy.ndimage.filters import gaussian_filter
from scipy.ndimage import imread
from scipy.integrate import dblquad
from scipy.signal import convolve2d, correlate2d
import matplotlib.cm as cm


def grad(I):
    return I[:, 2:] - 2.*I[:, 1:-1]  + I[:, :-2]


I = imread('rodada.png')
I = np.average(I, axis = 2)
B = gaussian_filter(I, sigma = 40)
G = grad(B)



corre = np.zeros((100, 100))
corre[40:60, :] = 1.



pl.subplot(121)
pl.imshow(G, cmap = cm.Greys_r)
pl.axis('off')

pl.subplot(122)
pl.imshow(correlate2d(G, corre), cmap = cm.Greys_r)
pl.axis('off')


pl.show()