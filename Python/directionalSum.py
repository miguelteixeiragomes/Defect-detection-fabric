import numpy as np


def diagonalSum(I, diag):
    if diag == '\\':
        R = np.zeros( np.sum(I.shape) - 1 , np.float32 )
        for i in range( -I.shape[1] + 1 , I.shape[0] ):
            R[i + I.shape[1] - 1] = np.trace(I, i)
        return R
    elif diag == '/':
        return diagonalSum(I[:, ::-1] , '\\')
    elif type(diag) != str:
        raise TypeError("The argument 'diag' must be of type 'str' not '%s'." % (str(type(diag)),))
    else:
        raise ValueError("The command '%s' in unrecognized. Use one the following commands ('/','\\') where the direction of the bar indicates the diafgonal." % (diag,))


def directionalSum(I, direction):
    if direction == '|':
        return np.average(I, axis = 0)
    elif direction == '-':
        return np.average(I, axis = 1)
    elif direction == '\\':
        return diagonalSum(I, '\\')
    elif direction == '/':
        return diagonalSum(I, '/')
    elif type(direction) != str:
        raise TypeError("The argument 'direction' must be of type 'str' not '%s'." % (str(type(direction)),))
    else:
        raise ValueError("The command '%s' in unrecognized. Use one the following commands ('|','/','-','\\') where the direction of the bar indicates the summation direction." % (direction,))



if __name__ == '__main__':
    from imageRotation import rotate
    import pylab as pl
    from scipy.ndimage import imread
    from localBinaryPattern import directionalLBP
    from gaussianSubSampling import gaussianSubSampling
    from scipy.ndimage.filters import gaussian_filter as gaussFilter
    
    I = np.average( imread('com.png') , axis = 2 )
    I = gaussianSubSampling(I , 12)
    I = rotate(I, -45)
    
    L = directionalLBP(I , '1/0' , 10)

    pl.figure('lbp')
    pl.subplot(121)
    pl.imshow( I , cmap = 'Greys_r' )
    pl.subplot(122)
    pl.imshow( L , cmap = 'Greys_r' )
    
    pl.figure('2')
    S = L - np.average(L)
    #gr = gaussFilter( np.average(S, axis = 0) , 0.0 )
    gr = gaussFilter( directionalSum(S, '/') , 0.0 )
    gr -= np.average(gr)
    pl.plot(gr)
    pl.show()