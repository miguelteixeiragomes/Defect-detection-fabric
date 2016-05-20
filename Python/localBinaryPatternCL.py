import numpy as np
from initCL import get_ready_cl
import pyopencl as cl

ctx, queue, mf, device = get_ready_cl()
prg = cl.Program(ctx, open('kernelsCL\\lbpTransformKernel.cl', 'r').read()).build()
##########################################################################################

def localBinaryPatternCL(I_h): # melhoramento de ~5x
    R_h = np.zeros( (I.shape[0] - 2, I.shape[1] - 2) , np.uint8)
    
    I_d        = cl.Buffer(ctx, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf = I_h)
    R_d        = cl.Buffer(ctx, mf.READ_WRITE , size = (I.shape[0] - 2)*(I.shape[1] - 2))

    prg.LBP_transform(queue, R_h.shape, None, I_d, R_d).wait()
    
    cl.enqueue_copy(queue, R_h, R_d)
    return R_h


def directionalLBP_CL(I, patternList = '0|1' , neighbors = 0 ):
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
    from localBinaryPatternPY import localBinaryPatternPY
    from gaussianSubSampling import gaussianSubSampling
    import pylab as pl
    from scipy.ndimage import imread
    test = ['LBP', 'DT'][0]
    
    if test == 'LBP':
        I = np.average( imread('com_2.png') , axis = 2 )
        I = gaussianSubSampling(I, 15, 1)
        Ti = clock()
        PY = localBinaryPatternPY(I)
        print 'LBP_PY time:', clock() - Ti
        Ti = clock()
        CL = localBinaryPatternCL(I)
        print 'LBP_CL time:', clock() - Ti

        pl.subplot(121)
        pl.imshow( PY , cmap = 'Greys_r' )
        pl.subplot(122)
        pl.imshow( CL , cmap = 'Greys_r' )
        pl.show()