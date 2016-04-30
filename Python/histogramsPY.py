import numpy as np


def histogramsPY(I, win_size, scan_rate, BINS = 256):    
    Is = np.arange(0, I.shape[0] - win_size[0] - 1, scan_rate[0])
    Js = np.arange(0, I.shape[1] - win_size[1] - 1, scan_rate[1])
    
    hists = np.zeros((len(Is), len(Js), BINS), np.uint32)
    #print 'hists:', hists.shape
    
    x = 0
    for i in Is:
        #print round(100*i/float(Is[-1]), 1), '%'
        y = 0
        for j in Js:
            hists[x, y] = np.histogram( I[ i:i+win_size[0]  ,  j:j+win_size[1] ].ravel() , bins = BINS)[0]
            y += 1
        x += 1
    
    return hists
    
    avg_hist = np.mean(hists, axis = (0, 1))
    res = np.zeros((len(Is), len(Js)))
    
    for i in range(res.shape[0]):
        for j in range(res.shape[1]):
            res[i, j] = np.sum(np.abs(hists[i, j] - avg_hist)**2)
            #res[i, j] = np.sum(  std_hist < np.abs(hists[i, j] - avg_hist)  )
            #res[i, j] = np.sum( (hists[i, j] - avg_hist)**2 / (hists[i, j] + avg_hist) )
    return res


if __name__ == '__main__':
    from time import clock
    import pylab as pl
    from scipy.ndimage import imread
    from gaussianSubSampling import gaussianSubSampling
    from localBinaryPattern import localBinaryPattern
    
    I = np.uint8( np.average( imread('linhas.png') , axis = 2 ) )
    I = gaussianSubSampling(I, 12)
    L = localBinaryPattern(I)
    Ti = clock()
    H = histogramsPY( L , (25,25) , (1,1) )
    print 'hist time:', clock() - Ti
    
    pl.subplot(131)
    pl.imshow(I, cmap = 'Greys_r')

    pl.subplot(132)
    pl.imshow(L, cmap = 'Greys_r')
    
    pl.subplot(133)
    pl.imshow(H, cmap = 'Greys_r')
    
    pl.show()