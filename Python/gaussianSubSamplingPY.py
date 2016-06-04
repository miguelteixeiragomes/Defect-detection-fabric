import numpy as np
from gaussianStuff import gaussianKernel2D as gaussianKernel


def gaussianSubSamplingPY(I, blurRadius, n):
    kernel = gaussianKernel( ( 2*blurRadius[0] + 1 , 2*blurRadius[1] + 1 ) )
    R      = np.zeros( ( (I.shape[0] - 2*blurRadius[0])//n[0] , (I.shape[1] - 2*blurRadius[1])//n[1] ) , np.float32)
    for i in  range(kernel.shape[0]):
        for j in range(kernel.shape[1]):
            R += kernel[i, j] * I[ i:n[0]*R.shape[0]+i:n[0]  ,  j:n[1]*R.shape[1]+j:n[1] ]
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
        pl.imshow( gaussianSubSamplingPY(I , (0.5,0.5) , (1,1) ), cmap = 'Greys_r' )
        pl.show()