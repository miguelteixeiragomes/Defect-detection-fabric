import numpy as np
from initCL import get_ready_cl
import pyopencl as cl

ctx, queue, mf, device = get_ready_cl(1,1)
prg = cl.Program(ctx, open('kernelsCL\\lbpTransformKernel.cl', 'r').read()).build()
##########################################################################################

def localBinaryPatternCL(I_h): # melhoramento de ~5x
    R_h = np.zeros( (I.shape[0] - 2, I.shape[1] - 2) , np.uint8)
    
    I_d        = cl.Buffer(ctx, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf = I_h)
    R_d        = cl.Buffer(ctx, mf.READ_WRITE , size = R_h.shape[0]*R_h.shape[1])

    prg.LBP(queue, R_h.shape, None, I_d, R_d).wait()
    
    cl.enqueue_copy(queue, R_h, R_d)
    return R_h


def directionalLBP_CL(I_h, patternList = '0|1' , neighborRange = 0 ):
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
    patternList_h  = np.uint8(np.array(patternList))
    nearMissList_h = np.uint8(np.array(nearMissList))
    
    R_h = np.zeros( (I.shape[0] - 2, I.shape[1] - 2) , np.uint8)
    
    patternList_d  = cl.Buffer(ctx, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf = patternList_h)    
    nearMissList_d = cl.Buffer(ctx, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf = nearMissList_h)   
    I_d            = cl.Buffer(ctx, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf = I_h)
    R_d            = cl.Buffer(ctx, mf.READ_WRITE , size = R_h.shape[0]*R_h.shape[1])
    
    prg.LBP(queue, R_h.shape, None, I_d, R_d).wait()
    prg.directionalPatterns(queue, R_h.shape, None, R_d, patternList_d, np.uint16(len(patternList)), nearMissList_d, np.uint16(len(nearMissList))).wait()
    for i in range(neighborRange):
        prg.neighborCorrection(queue, R_h.shape, None, R_d).wait()
    
    prg.cleanUp(queue, np.array(R_h.shape) - 2, None, R_d).wait()
    
    cl.enqueue_copy(queue, R_h, R_d)
    return R_h[1:-1,1:-1]



if __name__ == '__main__': # 0.00483932963738
    from time import clock
    from localBinaryPatternPY import localBinaryPatternPY, directionalLBP_PY
    from gaussianSubSampling import gaussianSubSampling
    import pylab as pl
    from scipy.ndimage import imread
    test = ['LBP', 'DT'][1]
    
    if test == 'LBP':
        I = np.average( imread('com_2.png') , axis = 2 )
        I = gaussianSubSampling(I, 15, 1)
        Ti = clock()
        PY = localBinaryPatternPY(I)
        print 'LBP_PY time:', clock() - Ti
        Ti = clock()
        CL = localBinaryPatternCL(I)
        print 'LBP_CL time:', clock() - Ti

        pl.subplot(131)
        pl.imshow( PY , cmap = 'Greys_r' )
        pl.subplot(132)
        pl.imshow( CL , cmap = 'Greys_r' )
        pl.subplot(133)
        pl.imshow( np.abs(CL - PY) , cmap = 'Greys_r' )
        pl.show()
    
    if test == 'DT':
        I = np.average( imread('com.png') , axis = 2 )
        I = gaussianSubSampling(I, 15, 1)
        
        Ti = clock()
        PY = directionalLBP_PY(I, '0|1', 1)
        print 'LBP_PY time:', clock() - Ti
        Ti = clock()
        CL = directionalLBP_CL(I, '0|1', 1)
        print 'LBP_CL time:', clock() - Ti
        
        pl.subplot(131)
        pl.imshow( PY , cmap = 'Greys_r' )
        pl.subplot(132)
        pl.imshow( CL , cmap = 'Greys_r' )
        pl.subplot(133)
        pl.imshow( (np.float32(CL) - np.float32(PY)) , cmap = 'Greys_r' )
        pl.colorbar()
        pl.show()