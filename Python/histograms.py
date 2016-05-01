import numpy as np
print "Histograms:"
try:
    from histogramsCL import histogramsCL as histogramsTmp
    print "\tKicking it up openCL style!"
except:
    from histogramsPY import histogramsPY as histogramsTmp
    print "\tInstall the damned openCL fool!"


def histograms(img, win_size, scan_rate = 1):
    win_sizeTpl = win_size  if  (type(win_size) in [tuple, list, np.ndarray])  else  (win_size, win_size)
    scan_rateTpl = scan_rate  if  (type(scan_rate) in [tuple, list, np.ndarray])  else  (scan_rate, scan_rate)
    
    return histogramsTmp( np.uint8(np.around(img)) , win_sizeTpl , scan_rateTpl )


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
    H = histograms( L , 25 )
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