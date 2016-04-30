import numpy as np


def gaussianKernel(n):
    n = n  if  (type(n) in [tuple, list, np.ndarray])  else  (n, n)
    x = np.arange(n[0])
    y = np.arange(n[1])
    x, y = np.meshgrid(x, y, indexing = 'ij')
    x0, y0 = .5*float(n[0] - 1) , .5*float(n[1] - 1)
    sigX, sigY = float(n[0])/5. , float(n[1])/5.
    ker = np.exp( - .5*(x - x0)**2/sigX**2  -  .5*(y - y0)**2/sigY**2 )
    return np.float32( ker / np.sum(ker) )


def gaussianSubSamplingPY(I, blurRadius, n):
    kernel = gaussianKernel( ( 2*blurRadius[0] + 1 , 2*blurRadius[1] + 1 ) )
    R      = np.zeros( ( (I.shape[0] - 2*blurRadius[0])//n[0] , (I.shape[1] - 2*blurRadius[1])//n[1] ) , np.float32)
    for i in  range(kernel.shape[0]):
        for j in range(kernel.shape[1]):
            R += kernel[i, j] * I[ i:n[0]*R.shape[0]+i:n[0]  ,  j:n[0]*R.shape[1]+j:n[0] ]
    return R


if __name__ == '__main__':
    import pylab as pl
    from scipy.ndimage import imread
    test = ['kernel', 'subSampling'][1]
    
    if test == 'kernel':
        pl.matshow(gaussianKernel((7, 5)))
        pl.colorbar()
        pl.show()
    
    if test == 'subSampling':
        I = np.average( imread('linhas.png') , axis = 2 )
        pl.imshow( gaussianSubSamplingPY(I , (15,1) , (1,1) ), cmap = 'Greys_r' )
        pl.show()