import numpy as np


def co_ocurrence_marix(I, direction, levels = 8):
    if direction[0] < 0:
        return co_ocurrence_marix(I[::-1, :], (-direction[0], direction[1]), levels)
    if direction[1] < 0:
        return co_ocurrence_marix(I[:, ::-1], (direction[0], -direction[1]), levels)
        
    coM = np.zeros([levels]*2, np.uint32)
    for i in range(I.shape[0] - direction[0]):
        for j in range(I.shape[1] - direction[1]):
            coM[ I[i,j] , I[i+direction[0],j+direction[1]] ] += 1
            
    return coM


def dissimilarity(coM):
    i, j = np.meshgrid(np.arange(coM.shape[0]), np.arange(coM.shape[1]), indexing = 'ij')
    return np.sum(coM * np.abs(i - j))

def contrast(coM):
    i, j = np.meshgrid(np.arange(coM.shape[0]), np.arange(coM.shape[1]), indexing = 'ij')
    return np.sum(coM * (i - j)**2)

def asm(coM):
    return np.sum(coM*coM)

def energy(coM):
    return np.sqrt(asm(coM))

def correlation(coM):
    i, j = np.meshgrid(np.arange(coM.shape[0]), np.arange(coM.shape[1]), indexing = 'ij')
    ui = np.average(i, weights = coM)
    uj = np.average(j, weights = coM)
    oi = np.average((i - ui)**2, weights = coM)
    oj = np.average((j - uj)**2, weights = coM)
    return np.sum( coM*(i - ui)*(j - uj)/np.sqrt(oi*oj) )

def homogeneity(coM):
    i, j = np.meshgrid(np.arange(coM.shape[0]), np.arange(coM.shape[1]), indexing = 'ij')
    return np.sum( coM / np.float64(1 + np.abs(i - j)) )


def pointsAnalysis(points, shape, winSize, scanRate):
    avg = np.array([ np.average(points[:, i]) for i in range(points.shape[1]) ])
    std = 3.0*np.array([ np.std(points[:, i]) for i in range(points.shape[1]) ])
    
    r = ((points[:, 0] - avg[0])/std[0])**2
    for i in range(1, points.shape[1]):
        r += ((points[:, i] - avg[i])/std[i])**2
    
    lenX = (shape[0] - winSize[0])//scanRate[0]
    lenY = (shape[1] - winSize[1])//scanRate[1]
    
    a = np.reshape(r, (lenX, lenY))
    x, y = np.where( a > 1 )
    x = .5*winSize[0] + scanRate[0]*x
    y = .5*winSize[0] + scanRate[1]*y
    print x
    print y
    
    return (y, x), points[ tuple(np.where(r > 1)[0]) , : ]


def grid(shape, winSize):
    lenX = (shape[0] - winSize[0])//winSize[0]
    lenY = (shape[1] - winSize[1])//winSize[1]
    r = np.zeros( I.shape , np.int8 )
    s = np.zeros( I.shape , np.int8 )
    i = 0
    while i*winSize[0] < I.shape[0]:
        r[ i*winSize[0]: , : ] ^= 1
        i += 1
    j = 0
    while j*winSize[1] < I.shape[1]:
        s[ : , j*winSize[1]: ] ^= 1
        j += 1
    r = r ^ s
    del(s)
    r = np.float32(r)
    r[np.where(r == 0)] = np.nan
    return r


def GLCM(I, winSize, scanRate, direction, analysis = [dissimilarity, contrast, asm, energy, correlation, homogeneity], levels = 256):
    lenX = (I.shape[0] - winSize[0])//scanRate[0]
    lenY = (I.shape[1] - winSize[1])//scanRate[1]
    points = np.zeros((lenX*lenY, len(analysis)))
    
    for i in range(lenX):
        for j in range(lenY):
            points[i*lenY + j] = [ function( I[ i*scanRate[0]:i*scanRate[0]+winSize[0]  ,  j*scanRate[1]:j*scanRate[1]+winSize[1] ] ) for function in analysis ]
    
    return points


if __name__ == '__main__':
    test = ['co_oc_m', 'GLCM'][1]
    
    if test == 'co_oc_m':
        I = np.array([[0, 0, 0, 0],
                      [0, 0, 0, 2],
                      [0, 0, 0, 0],
                      [0, 0, 2, 0]])
        
        print co_ocurrence_marix(I , (1,1))

    if test == 'GLCM':
        from gaussianSubSampling import gaussianSubSampling
        from scipy.ndimage import imread
        from time import clock
        import pylab as pl
        I = np.average( imread('com.png') , axis = 2 )
        I = gaussianSubSampling(I, 15)
        I = np.uint8(np.around(I))
        
        winSize   = (20, 20)
        scanRate  = (2, 2)
        direction = (1, 1)
        
        Ti = clock()
        points = GLCM( I , winSize , scanRate , direction )[:, (2,-2)]
        imgPnts, scatterPnts = pointsAnalysis(points, I.shape, winSize, scanRate)
        print 'GLCM:', round(clock() - Ti, 3), 's'
        
        pl.subplot(121)
        pl.imshow(I, cmap = 'Greys_r')
        pl.imshow(grid(I.shape, winSize), alpha = .1)
        pl.scatter(*imgPnts, alpha = .5)
        #pl.axis('off')
        pl.subplot(122)
        pl.scatter(points[:, 0], points[:, 1], alpha = .05)
        pl.scatter(scatterPnts[:, 0], scatterPnts[:, 1], c = 'r')
        pl.show()