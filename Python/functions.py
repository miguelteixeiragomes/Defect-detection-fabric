import numpy as np
import pylab as pl
from scipy.ndimage.filters import gaussian_filter
from scipy.ndimage import imread
from scipy.integrate import dblquad
from scipy.signal import convolve2d
import matplotlib.cm as cm
from scipy.optimize import curve_fit

def compr(I, n):
    a = np.zeros((I.shape[0]//n, I.shape[1]//n))
    I = I[:I.shape[0]//n * n, :I.shape[1]//n * n]
    for i in range(n):
        for j in range(n):
            a += I[i::n, j::n]
    return a

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

def secondDerivSqrd(I):
    #X = I[2:, 1:-1] - I[:-2, 1:-1]
    #Y = I[1:-1, 2:] - I[1:-1, :-2]
    return (I[:, 2:] - 2.*I[:, 1:-1]  + I[:, :-2])**2
    #return Y
    #return X*X + Y*Y

def test(lst_maxes, threshold = 5.):
    lst_maxes.sort()
    if lst_maxes[-1] > threshold*lst_maxes[-2]:
        return True
    return False

def svd_decomp(I, n):
    u, s, v = np.linalg.svd(I, full_matrices = False)
    s[n:] = 0.
    return np.dot(u, np.dot(np.diag(s), v))

def fullTest(I, compression, firstGauss, secondGauss, threshold, represent = True):
    #recebe img em escala de cinzentos
    img = compr(I, compression)
    if represent:
        pl.subplot(221)
        pl.imshow(img, cmap = 'Greys_r')
        pl.axis('off')
    img = convolve2d(img, generateGaussianKernel2D(firstGauss), mode = 'valid')
    if represent:
        pl.subplot(222)
        pl.imshow(img, cmap = 'Greys_r')
        pl.axis('off')
    img = secondDerivSqrd(img)
    if represent:
        pl.subplot(223)
        pl.imshow(img, cmap = 'Greys_r')
        pl.axis('off')
    img = np.average(img, axis = 0)
    if represent:
        pl.subplot(224)
        pl.plot(img, ':')
        #pl.axis('off')
    img = np.convolve(img, generateGaussianKernel1D(secondGauss), mode = 'valid')
    if represent:
        pl.plot([0.]*(secondGauss//2) + list(img))
        #pl.axis('off')
    return test(maxes(img), threshold)