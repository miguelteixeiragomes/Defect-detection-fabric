from initCL import get_ready_cl
import numpy as np
import pyopencl as cl
from time import clock
import pylab as pl
####################################################################################
ctx, queue, mf = get_ready_cl(0, 0)
prg = cl.Program(ctx, open('kernelsCL\\histogramsKernel.cl', 'r').read()).build()
####################################################################################


def histogramsCL(I_h, win_size, scan_rate, BINS = 256): # janelas tem de conter no minimo 256 elemntos
    if (win_size[0]*win_size[1]) < 256:
        raise ValueError('The window must contain a minimum of 256 pixels this one has %d * %d = %d.' % (win_size[0], win_size[1], win_size[0]*win_size[1]))
    hists_h = np.zeros( ( (I_h.shape[0] - win_size[0])//scan_rate[0] , (I_h.shape[1] - win_size[1])//scan_rate[1] , BINS ) , np.uint32 )
    
    I_d        = cl.Buffer(ctx, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf = I_h       )
    hists_d    = cl.Buffer(ctx, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf = hists_h   )

    Ti = clock()
    prg.histograms1(queue, np.array(hists_h.shape)[:2]*np.array(win_size), win_size, I_d, hists_d, np.uint16(hists_h.shape[1]), np.uint16(I_h.shape[1]), np.uint16(scan_rate[0]), np.uint16(scan_rate[1])).wait()
    #prg.histograms2(queue, np.array(hists_h.shape)[:2]*np.array(win_size), None, I_d, hists_d, np.uint16(hists_h.shape[1]), np.uint16(I_h.shape[1]), np.uint16(win_size[0]), np.uint16(win_size[1]), np.uint16(scan_rate[0]), np.uint16(scan_rate[1])).wait()
    print 'time:', clock() - Ti
    cl.enqueue_copy(queue, hists_h, hists_d)

    
    avg_hist = np.mean(hists_h.astype(np.float32), axis = (0, 1))
    res = np.zeros( np.array(hists_h.shape)[:2] , np.float32 )
    
    for i in range(res.shape[0]):
        for j in range(res.shape[1]):
            res[i, j] = np.sum( (hists_h[i, j] - avg_hist)[0]**2 )
    return res


if __name__ == '__main__':
    from time import clock
    import pylab as pl
    from scipy.ndimage import imread
    from gaussianSubSampling import gaussianSubSampling
    from localBinaryPattern import localBinaryPattern
    #from histogramsPY import histogramsPY
    
    I = np.average( imread('linhas.png') , axis = 2 )
    I = gaussianSubSampling(I, 15)
    L = np.uint8( localBinaryPattern(I) )
    Ti = clock()
    H = histogramsCL( L , (25,25) , (1,1) )
    print 'hist time:', clock() - Ti
    
    #print np.sum( 1*np.abs(H1 - H2) )

    pl.figure('hists')
    
    pl.subplot(131)
    pl.imshow(I, cmap = 'Greys_r')
    pl.axis('off')

    pl.subplot(132)
    pl.imshow(L, cmap = 'Greys_r')
    pl.axis('off')
    
    pl.subplot(133)
    pl.imshow(H, cmap = 'Greys_r')
    pl.axis('off')
    
    pl.show()