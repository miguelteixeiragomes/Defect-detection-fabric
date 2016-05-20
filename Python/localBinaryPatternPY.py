import numpy as np


def localBinaryPatternPY(I):
    R  = np.zeros( np.array(I.shape) - 2 , np.uint8 )
    R +=   1*( I[1:-1 , 1:-1]  <=  I[ :-2 ,  :-2] )
    R +=   2*( I[1:-1 , 1:-1]  <=  I[ :-2 , 1:-1] )
    R +=   4*( I[1:-1 , 1:-1]  <=  I[ :-2 , 2:  ] )
    R +=   8*( I[1:-1 , 1:-1]  <=  I[1:-1 , 2:  ] )
    R +=  16*( I[1:-1 , 1:-1]  <=  I[2:   , 2:  ] )
    R +=  32*( I[1:-1 , 1:-1]  <=  I[2:   , 1:-1] )
    R +=  64*( I[1:-1 , 1:-1]  <=  I[2:   ,  :-2] )
    R += 128*( I[1:-1 , 1:-1]  <=  I[1:-1 ,  :-2] )
    return R


def directionalLBP(I, patternList = '0|1' , neighbors = 0 ):
    if type(patternList) == str:
        if patternList == '0|1':
            patternList = [0b00011110, 0b00111100]
        elif patternList == '1|0':
            patternList = [0b11100001, 0b11000011]
            
        elif patternList == '0-1':
            patternList = [0b11110000, 0b01111000]
        elif patternList == '1-0':
            patternList = [0b00001111, 0b01111000]

        elif patternList == '0/1':
            patternList = [0b01111000, 0b00111100]
        elif patternList == '1/0':
            patternList = [0b11000011, 0b10000111]

        elif patternList == '0\\1':
            patternList = [0b00001111, 0b00011110]
        elif patternList == '1\\0':
            patternList = [0b11110000, 0b11100001]
        
        elif patternList == '|':
            patternList = [0b00011110, 0b00111100, 0b11100001, 0b11000011]
        elif patternList == '-':
            patternList = [0b11110000, 0b01111000, 0b00001111, 0b01111000]
        elif patternList == '/':
            patternList = [0b01111000, 0b00111100, 0b11000011, 0b10000111]
        elif patternList == '\\':
            patternList = [0b00001111, 0b00011110, 0b11110000, 0b11100001]
        
        else:
            raise ValueError("Invalid text command: '" + str(patternList) + "'.")
            
    nearMissList = []
    for i in range(len(patternList)):
        for j in range(8):
            elem = patternList[i] ^ (2**j)
            if elem not in patternList:
                if elem not in nearMissList:
                    nearMissList.append( elem )
                
    L  = localBinaryPattern(I)
    U  = np.zeros( L.shape , np.uint8 )
    U += 1*( (L >> 7) != (L >> 1) )
    for k in range(7):
        U += 1*(  ((L & 2**k) >> k) != ((L & 2**(k+1)) >> (k+1))  )
    
    s  = np.zeros( U.shape , np.uint8 )
    for k in range(8):
        s += (L & 2**k) >> k
    
    R  = np.zeros( s.shape , np.uint8 )
    for i in range(len(patternList)):
        R += 255*(L == patternList[i])
    
    for i in range(len(nearMissList)):
        R += 127*(L == nearMissList[i])
    
    for i in range(neighbors):
        mask = 1*(R[1:-1, 1:-1] == 127)

        R[1:-1, 1:-1] += 128*mask*( ( (R[2:  , 1:-1] == 255) + 
                                      (R[ :-2, 1:-1] == 255) + 
                                      (R[1:-1, 2:  ] == 255) + 
                                      (R[1:-1,  :-2] == 255) + 
                                      (R[2:  , 2:  ] == 255) + 
                                      (R[ :-2,  :-2] == 255) + 
                                      (R[ :-2, 2:  ] == 255) + 
                                      (R[2:  ,  :-2] == 255) ) > 0 )
    
    R = R[1:-1, 1:-1]
    R[np.where(R == 127)] = 0
    return R


if __name__ == '__main__':
    from time import clock
    from gaussianSubSampling import gaussianSubSampling
    import pylab as pl
    from scipy.ndimage import imread
    test = ['LBP', 'DT'][0]
    
    if test == 'LBP':
        I = np.average( imread('com_3.png') , axis = 2 )
        I = gaussianSubSampling(I, 15, 1)
        Ti = clock()
        I = localBinaryPatternPY(I)
        print 'LBP time:', clock() - Ti
        I = gaussianSubSampling(I, 1, 1)
        pl.imshow( I , cmap = 'Greys_r' )
        pl.show()

    if test == 'DT':
        from scipy.ndimage.filters import gaussian_filter as gauss
        from imageRotation import rotate
        I = np.average( imread('com_2.png') , axis = 2 )#[100:120, 100:120]
        I = rotate(I, 0)
        I = gaussianSubSampling(I, 20, 1)
        D = directionalLBP(I)
        print D.shape
        #D = gaussianSubSampling(D, 5)
        pl.figure('lbp')
        pl.subplot(121)
        pl.imshow( I , cmap = 'Greys_r' )
        pl.subplot(122)
        pl.imshow( D , cmap = 'Greys_r' )
        
        pl.figure('2')
        S = D - np.average(D)
        gr = gauss(np.average(S, axis = 0), 15.0)
        gr -= np.average(gr)
        pl.plot(gr)
        pl.show()