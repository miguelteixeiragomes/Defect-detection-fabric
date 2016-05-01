from initCL import get_ready_cl
from gaussianSubSamplingPY import gaussianKernel
import numpy as np
import pyopencl as cl
####################################################################################
ctx, queue, mf, device = get_ready_cl()
prg = cl.Program(ctx, open('kernelsCL\\gaussianSubSamplingKernel.cl', 'r').read()).build()
####################################################################################


def gaussianSubSamplingCL(I_h, blurRadius, n):
    gaussKer_h = gaussianKernel( ( 2*blurRadius[0] + 1 , 2*blurRadius[1] + 1 ) )
    R_h = np.zeros( ( (I_h.shape[0] - 2*blurRadius[0])//n[0] , (I_h.shape[1] - 2*blurRadius[1])//n[1] ), np.float32)
    
    gaussKer_d = cl.Buffer(ctx, mf.READ_ONLY  | mf.COPY_HOST_PTR, hostbuf = gaussKer_h)
    I_d        = cl.Buffer(ctx, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf = I_h)
    R_d        = cl.Buffer(ctx, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf = R_h)

    prg.gaussSS(queue, R_h.shape, None, I_d, R_d, gaussKer_d, np.uint16(I_h.shape[1]), np.uint16(blurRadius[0]), np.uint16(blurRadius[1]), np.uint16(n[0]), np.uint16(n[1])).wait()
    
    cl.enqueue_copy(queue, R_h, R_d)
    
    return R_h


if __name__ == '__main__':
    from scipy.ndimage import imread
    import pylab as pl
    I = np.float32(np.average( imread('linhas.png') , axis = 2 ))
    pl.imshow( gaussianSubSamplingCL(I , (15,1) , (1,1) ) , cmap = 'Greys_r' )
    pl.show()