import numpy as np


def directionalDerivative( G , command1 ):
    if command1 == '-':
        return (G[2: , 1:-1] -2.*G[1:-1 , 1:-1] + G[:-2 , 1:-1])**2
    
    if command1 == '|':
        return (G[1:-1 , 2:] -2.*G[1:-1 , 1:-1] + G[1:-1 , :-2])**2
    
    if command1 == '/':
        return (G[2: , 2:] -2.*G[1:-1 , 1:-1] + G[:-2 , :-2])**2
    
    if command1 == '\\':
        return (G[2: , :-2] -2.*G[1:-1 , 1:-1] + G[:-2 , 2:])**2


if __name__ == '__main__':
    import pylab as pl
    from scipy.ndimage import imread
    from gaussianSubSampling   import gaussianSubSampling
    
    I = gaussianSubSampling(np.average(imread('com.png'), axis = 2), 12)
    pl.subplot(121)
    pl.imshow(I, cmap = 'Greys_r')
    pl.subplot(122)
    pl.imshow(directionalDerivative(I, '|'), cmap = 'Greys_r')
    pl.show()