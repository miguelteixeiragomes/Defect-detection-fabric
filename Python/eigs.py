import numpy as np
import pylab as pl
from scipy.ndimage.filters import gaussian_filter
from scipy.ndimage import imread
from scipy.integrate import dblquad
from scipy.signal import convolve2d
import matplotlib.cm as cm
from scipy.optimize import curve_fit

I = imread('com.png')
I = np.average(I, axis = 2)


u, s, v = np.linalg.svd(I)
pl.figure(2)
pl.plot(s)
pl.yscale('log')
s[1:] = 0.
S = np.dot(u, np.dot(np.diag(s), v))

pl.figure(1)
pl.subplot(121)
pl.imshow(I, cmap = cm.Greys_r)
pl.axis('off')

pl.subplot(122)
pl.imshow(S, cmap = cm.Greys_r)
pl.axis('off')

pl.show()