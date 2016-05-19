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
        from scipy.ndimage import imread
        import pylab as pl
        I = np.uint8(np.around(np.average( imread('com.png') , axis = 2 )))
        
        points = GLCM( I , (20,20) , (5,5) , (0,1) )
        
        pl.subplot(121)
        pl.imshow(I, cmap = 'Greys_r')
        #pl.axis('off')
        pl.subplot(122)
        pl.scatter(points[:, 3], points[:, -2], alpha = .1)
        pl.show()