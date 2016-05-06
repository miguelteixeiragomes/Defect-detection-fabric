import numpy as np


def localBinaryPattern(I):
    R  = np.zeros( np.array(I.shape) - 2 , np.uint8 )
    R +=   1*(I[1:-1, 1:-1] >= I[2:  ,  :-2])
    R +=   2*(I[1:-1, 1:-1] >= I[2:  , 1:-1])
    R +=   4*(I[1:-1, 1:-1] >= I[2:  , 2:  ])
    R +=   8*(I[1:-1, 1:-1] >= I[1:-1, 2:  ])
    R +=  16*(I[1:-1, 1:-1] >= I[ :-2, 2:  ])
    R +=  32*(I[1:-1, 1:-1] >= I[ :-2, 1:-1])
    R +=  64*(I[1:-1, 1:-1] >= I[ :-2,  :-2])
    R += 128*(I[1:-1, 1:-1] >= I[1:-1,  :-2])
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
            #s = min(s, 8 - s)
            
            R[i, j]  = 2  if  ((U == 2) and (s == 4 or s == 3))  else  0
            R[i, j] += 1  if  ((U == 4) and (s in [4, 5, 6]))  else  0
            #R[i, j] = 1 if U == 4 else 0
            #R[i, j] = s if U<3 else 0
            #sleep(1.)

    return R[ 1:-1 , 1:-1 ]
    

def DT2(I):
    lst = [ 224 , 112 ,  56 ,  28 ,  14 ,   7 , 131 , 193 , 
            240 , 120 ,  60 ,  30 ,  15 , 135 , 195 , 225 , 
            248 , 124 ,  62 ,  31 , 143 , 199 , 227 , 241 ]
    for i in range(24):
        for j in range(8):
            lst.append( lst[j] ^ (2**j) )
    L  = localBinaryPattern(I)
    U  = np.zeros( L.shape , np.uint8 )
    U += 1*( (L >> 7) != (L >> 1) )
    for k in range(7):
        U += 1*(  ((L & 2**k) >> k) != ((L & 2**(k+1)) >> (k+1))  )
    s  = np.zeros( U.shape , np.uint8 )
    for k in range(8):
        s += (L & 2**k) >> k
    
    R  = np.zeros( s.shape , np.uint8 )
    for i in range(len(lst)):
        R += 1*(L == lst[i])
    R[:, :] = 127*(R > 0)    
    R += 255*( (U == 2) * (s > 2) * (s < 5) )
    
    for i in range(1):
        mask = 1*(R[1:-1, 1:-1] == 127) # arranjar maneira de fazer o tresh nos vizinhos
        
        R[1:-1, 1:-1] += 128*(  )
        
    R[np.where(R == 127)] = 0    
    return R


if __name__ == '__main__':
    from gaussianSubSampling import gaussianSubSampling
    import pylab as pl
    from scipy.ndimage import imread
    test = ['LBP', 'DT'][1]
    
    if test == 'LBP':
        I = np.average( imread('com.png') , axis = 2 )
        I = gaussianSubSampling(I, 15, 1)
        I = localBinaryPattern(I)
        I = gaussianSubSampling(I, 1, 1)
        pl.imshow( I , cmap = 'Greys_r' )
        pl.show()

    if test == 'DT':
        I = np.average( imread('com.png') , axis = 2 )
        I = gaussianSubSampling(I, 15, 1)
        D = DT2(I)
        print D.shape
        #D = gaussianSubSampling(D, 5)
        pl.subplot(121)
        pl.imshow( I , cmap = 'Greys_r' )
        pl.subplot(122)
        pl.imshow( D , cmap = 'Greys_r' )
        pl.show()