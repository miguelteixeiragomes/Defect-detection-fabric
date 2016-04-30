import numpy as np


def localBinaryPattern(I):
    R  = np.zeros( np.array(I.shape) - 2 , np.uint8 )
    R +=   1*(I[1:-1, 1:-1] > I[2:  ,  :-2])
    R +=   2*(I[1:-1, 1:-1] > I[2:  , 1:-1])
    R +=   4*(I[1:-1, 1:-1] > I[2:  , 2:  ])
    R +=   8*(I[1:-1, 1:-1] > I[1:-1, 2:  ])
    R +=  16*(I[1:-1, 1:-1] > I[ :-2, 2:  ])
    R +=  32*(I[1:-1, 1:-1] > I[ :-2, 1:-1])
    R +=  64*(I[1:-1, 1:-1] > I[ :-2,  :-2])
    R += 128*(I[1:-1, 1:-1] > I[1:-1,  :-2])
    return R


def DT(I): # directional transform
    I = localBinaryPattern(I)
    R = np.zeros( I.shape , np.float32 )
    for i in range( 1 , I.shape[0] - 1 ):
        for j in range( 1 , I.shape[1] - 1 ):
            p = I[i, j]
            
            U = 1 * (  (p >> 7) != (p & 1)  )
            for k in range(7):
                U += 1 * (  ((p & 2**k) >> k) != ((p & 2**(k+1)) >> (k+1))  )
            
            s = 0
            for k in range(8):
                s += (p & 2**k) >> k
            s = min(s, 8 - s)
            
            R[i, j] = 1  if  ((U == 2) and (s in [3, 4]))  else  0
            #R[i, j] = s if U<3 else 0
            #sleep(1.)

    return R[ 1:-1 , 1:-1 ]


if __name__ == '__main__':
    from gaussianSubSampling import gaussianSubSampling
    import pylab as pl
    from scipy.ndimage import imread
    test = ['LBP', 'DT'][1]
    
    if test == 'LBP':
        I = np.average( imread('com.png') , axis = 2 )
        I = gaussianSubSampling(I, 12, 1)
        I = localBinaryPattern(I)
        I = gaussianSubSampling(I, 1, 1)
        pl.imshow( I , cmap = 'Greys_r' )
        pl.show()

    if test == 'DT':
        I = np.average( imread('com.png') , axis = 2 )
        I = gaussianSubSampling(I, 12, 2)
        D = DT(I)
        #D = gaussianSubSampling(D, 1, 1)
        pl.subplot(121)
        pl.imshow( I , cmap = 'Greys_r' )
        pl.subplot(122)
        pl.imshow( D , cmap = 'Greys_r' )
        pl.show()