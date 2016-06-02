import numpy as np


def gaussianKernel(n):
    x = np.arange(n)
    x0 = .5*float(n - 1)
    sigX = float(n)/5.
    ker = np.exp( - .5*(x - x0)**2/sigX**2 )
    return np.float32( ker / np.sum(ker) )
    

def gaussianFilter(signal, n):
    ker = gaussianKernel(n)
    return np.convolve(signal, ker, mode = 'valid')