import numpy as np
from initCL import get_ready_cl
import pyopencl as cl

ctx, queue, mf, device = get_ready_cl()
prg = cl.Program(ctx, open('kernelsCL\\imageRotation90.cl', 'r').read()).build()
##########################################################################################


def rotateUpTo90_horizontalCL(I_h, theta): #
    s = I.shape[1] - 1
    l = I.shape[0] - 1
    x = 0.5*s
    if s > l*np.sin(2.0*theta):

        print 'uououo'
        x = np.sin(theta) * (l*np.cos(theta) - s*np.sin(theta))/(np.cos(2.0*theta))
    
    a = x/np.sin(theta)
    b = (s - x)/np.cos(theta)
    
    R_h = np.zeros( (int(a), int(b)) , np.float32)
    
    I_d        = cl.Buffer(ctx, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf = I_h)
    R_d        = cl.Buffer(ctx, mf.READ_WRITE , size = 4*R_h.shape[0]*R_h.shape[1])

    prg.rotateUpTo90_horizontal(queue, R_h.shape, None, I_d, R_d, np.float32(theta), np.float32(x), np.uint16(I.shape[1])).wait()
    
    cl.enqueue_copy(queue, R_h, R_d)
    return R_h


if __name__ == '__main__':
    import pylab as pl
    from scipy.ndimage import imread
    I = np.float32(np.average( imread('linhas2.png') , axis = 2 ))
    R = rotateUpTo90_horizontalCL(I, 35. * np.pi/180.)
    
    pl.subplot(121)
    pl.imshow(I, cmap = 'Greys_r')
    pl.subplot(122)
    pl.imshow(R, cmap = 'Greys_r')
    pl.show()