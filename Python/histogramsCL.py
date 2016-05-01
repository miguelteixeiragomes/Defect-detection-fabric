from initCL import get_ready_cl
import numpy as np
import pyopencl as cl
####################################################################################
ctx, queue, mf, device = get_ready_cl(0,0)
prg = cl.Program(ctx, open('kernelsCL\\histogramsKernel.cl', 'r').read()).build()
####################################################################################


def histogramsCL(I_h, win_size, scan_rate, BINS = 256): # janelas tem de conter no minimo 256 elemntos
    hists_h    = np.zeros( ( (I_h.shape[0] - win_size[0])//scan_rate[0] , (I_h.shape[1] - win_size[1])//scan_rate[1] , BINS ) , np.int32 )
    sum_hist_h = np.zeros( 256 , np.int32 )
    R_h        = np.zeros( np.array(hists_h.shape)[:2] , np.float32 )
    
    I_d        = cl.Buffer(ctx, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf = I_h        )
    hists_d    = cl.Buffer(ctx, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf = hists_h    )
    sum_hist_d = cl.Buffer(ctx, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf = sum_hist_h )
    R_d        = cl.Buffer(ctx, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf = R_h        )

    prg.histograms(queue, np.array(hists_h.shape)[:2]*np.array(win_size), None, I_d, hists_d, sum_hist_d, np.int32(hists_h.shape[1]), np.int32(I_h.shape[1]), np.int32(win_size[0]), np.int32(win_size[1]), np.int32(scan_rate[0]), np.int32(scan_rate[1])).wait()
    prg.histogramSubtraction(queue, np.array([256,1])*np.array(hists_h.shape)[:2], (256,1), R_d, hists_d, sum_hist_d, np.int32(hists_h.shape[0]), np.int32(hists_h.shape[1]), np.int32(I_h.shape[1])).wait()
    cl.enqueue_copy(queue, R_h, R_d)
    return R_h


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