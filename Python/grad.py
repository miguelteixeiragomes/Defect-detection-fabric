import numpy as np
import pylab as pl
from scipy.ndimage.filters import gaussian_filter
from scipy.ndimage import imread
from scipy.integrate import dblquad
from scipy.signal import convolve2d
import matplotlib.cm as cm
from scipy.optimize import curve_fit

def generateGaussianKernel1D(n):
    N = float(n)
    ker = np.zeros(n)
    for i in range(n):
        ker[i] = np.exp(-((5*i + 2.5)/N - 2.5)**2)
    return ker / np.sum(ker)

def generateGaussianKernel2D(n):
    N = float(n)
    ker = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            ker[i, j] = np.exp(-((5*i + 2.5)/N - 2.5)**2) * np.exp(-((5*j + 2.5)/N - 2.5)**2)
    return ker / np.sum(ker)

def maxes(x):
    return [x[i] for i in range(1, len(x) - 1) if x[i] > max(x[i - 1], x[i + 1])]

def grad(I):
    #X = I[2:, 1:-1] - I[:-2, 1:-1]
    #Y = I[1:-1, 2:] - I[1:-1, :-2]
    return I[:, 2:] - 2.*I[:, 1:-1]  + I[:, :-2]
    #return Y
    #return X*X + Y*Y

def lorentzian(x, x0, gamma):
    gamma *= .5
    return (gamma**2 / ((x - x0)**2 + gamma**2)) / (np.pi*gamma)

def test(lst_maxes, threshold = 5.):
    lst_maxes.sort()
    if lst_maxes[-1] > threshold*lst_maxes[-2]:
        return True
    return False
    

sig = 10
I = imread('sem.png')
I = np.average(I, axis = 2)
#B = gaussian_filter(I, sigma = sig, mode = 'reflect')
B = convolve2d(I, generateGaussianKernel2D(50), mode = 'valid')
G = grad(B)

pl.subplot(151)
pl.imshow(I, cmap = cm.Greys_r)
pl.axis('off')

pl.subplot(152)
F = np.log10( np.abs(np.fft.fft2(I)) )
pl.imshow(F, cmap = cm.Greys_r)
pl.axis('off')

pl.subplot(153)
pl.imshow(B, cmap = cm.Greys_r)
pl.axis('off')

pl.subplot(154)
F = np.log10( np.abs(np.fft.fft2(B)) )
pl.imshow(F, cmap = cm.Greys_r)
pl.axis('off')

pl.subplot(155)
pl.imshow(G**2, cmap = cm.Greys_r)
pl.axis('off')


g = np.average(G, axis = 0)**2
g = np.convolve(g, generateGaussianKernel1D(50))
#g = gaussian_filter(g, sigma = 3*sig, mode = 'wrap')


pl.figure(2)
pl.plot(g)


print test(maxes(g), 2.)

pl.show()