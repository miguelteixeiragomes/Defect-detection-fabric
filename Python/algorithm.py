import numpy as np
import pylab as pl
from gaussianSubSampling   import gaussianSubSampling
from localBinaryPattern    import directionalLBP
from directionalSum        import directionalSum
from minMax                import maxs
from imageRotation         import rotate
from scipy.ndimage.filters import gaussian_filter as gaussianFilter


def singelImageAnalysis(G, command1, command2, threshold):
    #print '\n', command1 , command2 # comment for fast detection
    #pl.imshow(G, cmap = 'Greys_r');pl.show() # comment for fast detection
    A  = directionalLBP(G , command1, 20)
    #pl.imshow(A, cmap = 'Greys_r');pl.colorbar();pl.show() # comment for fast detection
    #print np.average(A) # comment for fast detection
    L = A - np.average(A)
    #pl.contourf(L, cmap = 'Greys_r');pl.colorbar();pl.show() # comment for fast detection
    L  = directionalSum(L , command2)
    #pl.plot(L);pl.show() # comment for fast detection
    L -= np.average(L)
    L *= L
    #pl.plot(L);pl.show() # comment for fast detection
    L  = gaussianFilter(L, 5.0)
    #pl.plot(L);pl.show() # comment for fast detection
    L  = maxs(L)
    #pl.plot(L);pl.show() # comment for fast detection
    M  = max(L)
    del(L[L.index(M)])
    #pl.plot(L);pl.show() # comment for fast detection
    return M > threshold*max(L)


def eightDirectionAnalysis(G, threshold):
    if singelImageAnalysis(G , '0|1' , '|' , threshold) and singelImageAnalysis(G , '1|0' , '|' , threshold):
        return True
        
    if singelImageAnalysis(G , '0-1' , '-' , threshold) and singelImageAnalysis(G , '1-0' , '-' , threshold):
        return True
    
    if singelImageAnalysis(G , '0/1' , '/' , threshold) and singelImageAnalysis(G , '1/0' , '/' , threshold):
        return True

    if singelImageAnalysis(G , '0\\1' , '\\' , threshold) and singelImageAnalysis(G , '1\\0' , '\\' , threshold):
        return True
    
    return False


def fullAnalysis(I, blurRadius, threshold):
    G = gaussianSubSampling(I , blurRadius)
    
    if eightDirectionAnalysis(G, threshold):
        return True
    
    R = rotate(G, 22.5)
    if eightDirectionAnalysis(R, threshold):
        return True
        
    R = rotate(G, 11.25)
    if eightDirectionAnalysis(R, threshold):
        return True

    R = rotate(G, 33.75)
    if eightDirectionAnalysis(R, threshold):
        return True
    
    else:
        return False
    

if __name__ == '__main__':
    from scipy.ndimage import imread
    from time import clock
    I = np.average( imread('com.png') , axis = 2 )
    I = rotate(I, 56) # metam um angulo aleatorio que o meu super algoritmo nao quer saber!
    
    Ti = clock()
    print 'defect:', fullAnalysis( I , 15 , 2.0)
    print 'detected in:', round(clock() - Ti, 2), 's'