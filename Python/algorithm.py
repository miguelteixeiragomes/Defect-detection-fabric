import numpy as np
import pylab as pl
from gaussianSubSampling   import gaussianSubSampling
from localBinaryPattern    import directionalLBP
from directionalSum        import directionalSum
from minMax                import maxs
from imageRotation         import rotate
from scipy.ndimage.filters import gaussian_filter as gaussianFilter


def singelImageAnalysis(G, command1, command2, threshold, display = False):
    print '\t', command1
    if display:
        pl.figure('cmd1: %s  ,  %s' % (command1, command2))
        pl.subplot(221)
        pl.title('blurred image')
        pl.imshow(G, cmap = 'Greys_r')
        pl.axis('off')
        
    A  = directionalLBP(G , command1, 20)
    if display:
        pl.subplot(222)
        pl.title('special LBP')
        pl.imshow(A, cmap = 'Greys_r')
        pl.axis('off')
        
    L = A - np.average(A)
    L  = directionalSum(L , command2)
    L -= np.average(L)
    L *= L
    if display:
        pl.subplot(223)
        pl.title('blurred squared summation')
        pl.plot(L, 'r:')
        
    L  = gaussianFilter(L, 5.0)
    if display:
        pl.plot(L)
        
    L  = maxs(L)
    if display:
        pl.subplot(224)
        pl.title('maxes')
        pl.plot(L,)
        pl.show()

    M  = max(L)
    del(L[L.index(M)])
    return M > threshold*max(L)


def eightDirectionAnalysis(G, threshold, display):
    if singelImageAnalysis(G , '0|1' , '|' , threshold, display) and singelImageAnalysis(G , '1|0' , '|' , threshold, display):
        return True
        
    if singelImageAnalysis(G , '0-1' , '-' , threshold, display) and singelImageAnalysis(G , '1-0' , '-' , threshold, display):
        return True
    
    if singelImageAnalysis(G , '0/1' , '/' , threshold, display) and singelImageAnalysis(G , '1/0' , '/' , threshold, display):
        return True

    if singelImageAnalysis(G , '0\\1' , '\\' , threshold, display) and singelImageAnalysis(G , '1\\0' , '\\' , threshold, display):
        return True
    
    return False


def fullAnalysis(I, blurRadius, threshold, display = False):
    G = gaussianSubSampling(I , blurRadius)
    
    print 'angle:', 0.0
    if eightDirectionAnalysis(G, threshold, display):
        return True
    
    R = rotate(G, 22.5)
    print 'angle:', 22.5
    if eightDirectionAnalysis(R, threshold, display):
        return True
        
    R = rotate(G, 11.25)
    print 'angle:', 11.25
    if eightDirectionAnalysis(R, threshold, display):
        return True

    R = rotate(G, 33.75)
    print 'angle:', 33.75
    if eightDirectionAnalysis(R, threshold, display):
        return True
    
    else:
        return False
    

if __name__ == '__main__':
    from scipy.ndimage import imread
    from time import clock
    I = np.average( imread('sem.png') , axis = 2 )
    #I = rotate(I, 0) # metam um angulo aleatorio que o meu super algoritmo nao quer saber!
    
    Ti = clock()
    b = fullAnalysis( I , 12 , 2.0, display = False)
    print 'defect:', b
    print 'detected in:', round(clock() - Ti, 2), 's'