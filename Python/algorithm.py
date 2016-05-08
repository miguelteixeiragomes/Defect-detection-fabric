import numpy as np
import pylab as pl
from gaussianSubSampling import gaussianSubSampling
from localBinaryPattern  import directionalLBP
from directionalSum      import directionalSum
from minMax              import maxs
from imageRotation       import rotate
from scipy.ndimage.filters import gaussian_filter as gaussianFilter


def singelImageAnalysis(G, command1, command2, threshold):
    print command1 , command2
    pl.imshow(G, cmap = 'Greys_r');pl.show()
    L  = directionalLBP(G , command1, 20)
    pl.imshow(L, cmap = 'Greys_r');pl.show()
    L -= np.average(L)
    L  = directionalSum(L , command2)
    L -= np.average(L)
    L *= L
    L  = gaussianFilter(L, 5.0)
    pl.plot(L);pl.show()
    L  = maxs(L)
    pl.plot(L);pl.show()
    M  = max(L)
    #print 'L1', L
    del(L[L.index(M)])
    pl.plot(L);pl.show()
    #print 'L2', L
    #print M
    return M > threshold*max(L)


def eightDirectionAnalysis(G, threshold):
    if singelImageAnalysis(G , '0|1' , '|' , threshold) and singelImageAnalysis(G , '1|0' , '|' , threshold):
        print 'if1'
        return True
        
    if singelImageAnalysis(G , '0-1' , '-' , threshold) and singelImageAnalysis(G , '1-0' , '-' , threshold):
        return True
    
    if singelImageAnalysis(G , '0/1' , '/' , threshold) and singelImageAnalysis(G , '1/0' , '/' , threshold):
        print 'if3'
        return True

    if singelImageAnalysis(G , '0\\1' , '\\' , threshold) and singelImageAnalysis(G , '1\\0' , '\\' , threshold):
        return True
    
    return False


def fullAnalysis(I, blurRadius, threshold):
    #pl.imshow(I, cmap = 'Greys_r');pl.show()
    G = gaussianSubSampling(I , blurRadius)
    #pl.imshow(G, cmap = 'Greys_r');pl.show()
    if eightDirectionAnalysis(G, threshold):
        print 'full1'
        return True
    
    R = rotate(G, 22.5)
    if eightDirectionAnalysis(R, threshold):
        return True
        
    R = rotate(G, 11.25)
    if eightDirectionAnalysis(R, threshold):
        return True

    R = rotate(G, 22.5 + 11.25)
    if eightDirectionAnalysis(R, threshold):
        return True
    
    else:
        return False
    

if __name__ == '__main__':
    from scipy.ndimage import imread
    I = np.average( imread('com.png') , axis = 2 )
    I = rotate(I, 90)
    print fullAnalysis( I , 15 , 2.0)