import numpy as np
print "Gaussian Sub Sampling:"
try:
    from gaussianSubSamplingCL import gaussianSubSamplingCL as gaussianSubSamplingTmp
    print "\tKicking it up openCL style!"
except:
    from gaussianSubSamplingPY import gaussianSubSamplingPY as gaussianSubSamplingTmp
    print "\tInstall the damned openCL fool!"


def leiDeTojo(blur):
    if type(blur) in [tuple, list, np.ndarray]:
        if len(blur) == 2:
            return int(min( leiDeTojo(blur[0]) , leiDeTojo(blur[1]) ))
    return int(max( blur // 4  ,  1 ))


def gaussianSubSampling(img, blurRadius, n = -1):
    if n == -1:
        n = leiDeTojo(blurRadius)
    blurRadiusTpl = blurRadius  if  (type(blurRadius) in [tuple, list, np.ndarray])  else  (blurRadius, blurRadius)
    nTpl = n  if  (type(n) in [tuple, list, np.ndarray])  else  (n, n)
    
    return gaussianSubSamplingTmp( np.float32(img) , blurRadiusTpl , nTpl )


if __name__ == '__main__':
    from scipy.ndimage import imread
    import pylab as pl
    I = np.average( imread('Poly_com\\s5.jpg') , axis = 2 )
    pl.imshow( gaussianSubSampling( I , 25 , 1 ) , cmap = 'Greys_r' )
    pl.show()