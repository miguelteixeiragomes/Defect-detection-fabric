import numpy as np


def gaussianKernel1D(n):
    x = np.arange(n)
    x0 = .5*float(n - 1)
    sigX = float(n)/5.
    ker = np.exp( - .5*(x - x0)**2/sigX**2 )
    return np.float32( ker / np.sum(ker) )


def gaussianKernel2D(n):
    n = n  if  (type(n) in [tuple, list, np.ndarray])  else  (n, n)
    n_int = int(n[0]) + 1 if n[0] % 1. != 0 else int(n[0]) , int(n[1]) + 1 if n[1] % 1. != 0 else int(n[1])
    x = np.arange(n[0])
    y = np.arange(n[1])
    x, y = np.meshgrid(x, y, indexing = 'ij')
    x0, y0 = .5*float(n[0] - 1) , .5*float(n[1] - 1)
    sigX, sigY = float(n[0])/5. , float(n[1])/5.
    ker = np.exp( - .5*(x - x0)**2/sigX**2  -  .5*(y - y0)**2/sigY**2 )
    return np.float32( ker / np.sum(ker) )


def gaussianKernel3D(n):
    n = n  if  (type(n) in [tuple, list, np.ndarray])  else  (n, n, n)
    n_int = int(n[0]) + 1 if n[0] % 1. != 0 else int(n[0]) , int(n[1]) + 1 if n[1] % 1. != 0 else int(n[1]) , int(n[2]) + 1 if n[2] % 1. != 0 else int(n[2])
    x = np.arange(n[0])
    y = np.arange(n[1])
    z = np.arange(n[2])
    x, y = np.meshgrid(x, y, z, indexing = 'ij')
    x0, y0, z0 = .5*float(n[0] - 1) , .5*float(n[1] - 1) , .5*float(n[2] - 1)
    sigX, sigY, sigZ = float(n[0])/5. , float(n[1])/5. , float(n[2])/5.
    ker = np.exp( - .5*(x - x0)**2/sigX**2  -  .5*(y - y0)**2/sigY**2 - .5*(z - z0)**2/sigZ**2 )
    return np.float32( ker / np.sum(ker) )


def gaussianFilter(signal, n):
    ker = gaussianKernel1D(n)
    return np.convolve(signal, ker, mode = 'valid')