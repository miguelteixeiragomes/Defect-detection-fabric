import numpy as np
from scipy.interpolate import RectBivariateSpline


def getGrid(s, l, theta):
    x = 0.5*s
    if s > l*np.sin(2.0*theta):
        x = np.sin(theta) * (l*np.cos(theta) - s*np.sin(theta))/(np.cos(2.0*theta))
    
    a = x/np.sin(theta)
    b = (s - x)/np.cos(theta)
    
    X = np.arange(0.0, a, 1.0)#.astype(np.float32)
    Y = np.arange(0.0, b, 1.0)#.astype(np.float32)
    X, Y = np.meshgrid(X, Y)
    
    R = np.sqrt(X*X + Y*Y)
    O = np.arctan2(Y, X)
    
    O -= theta
    
    X = R*np.cos(O)
    Y = R*np.sin(O)
    
    Y += x
    
    X += .5*(l - X.max())
    
    return X, Y


def rotateUpTo90_horizontal(I, theta, spline = 3):
    if not (0. < theta < .5*np.pi):
        raise ValueError('The angle must be given in radians between 0 and pi/2.')
    if I.shape[0] > I.shape[1]:
        raise ValueError('The image must either be square or an horizontal rectangle.')
        
    inter = RectBivariateSpline(np.arange(I.shape[0]), np.arange(I.shape[1]), I, kx = spline, ky = spline)
    x, y  = getGrid( I.shape[1] - 1  ,  I.shape[0] - 1  ,  theta )
    R = inter.__call__(x, y, grid = False)
    return R.T


def rotate(I, angle): # theta given in degrees
    theta = angle % 360.
    if theta == 0.:
        R = np.zeros( I.shape , I.dtype )
        R[:, :] = I[:, :]
        return R
    
    if theta >= 90.:
        return rotate( I.T[::-1, :] , theta - 90. )
    
    theta *= np.pi/180.
    
    
    return rotateUpTo90_horizontal()
    

if __name__ == '__main__':
    import pylab as pl
    from scipy.ndimage import imread
    I = imread('dados.png')
    I = np.average(I, axis = 2)
    test = ['1', '2', '3'][1]
    
    if test == '1': # Oh yeah!!
        x, y = getGrid(300., 400., 33.75 * np.pi/180.)
        a, b = np.meshgrid(np.arange(401.), np.arange(301.) )
        pl.contourf( a, b , np.zeros(a.shape)+1. )
        pl.contourf( x , y , np.zeros(x.shape)+1. , cmap = 'Greys_r')
        pl.axes().set_aspect('equal', 'datalim')
        pl.show()
    
    if test == '2':
        from time import clock
        angle = 33.75  *  np.pi/180.
        pl.subplot(121)
        pl.imshow(I, cmap = 'Greys_r')
        X, Y = getGrid(I.shape[0]-1, I.shape[1]-1, angle)
        pl.contourf(X, Y, np.zeros(X.shape)+1, alpha = .3)
        
        pl.subplot(122)
        Ti = clock()
        R = rotateUpTo90_horizontal(I, angle, 3)
        print clock() - Ti
        pl.imshow(R, cmap = 'Greys_r')
        
        pl.show()
    
    if test == '3':
        angle = 0.
        pl.subplot(121)
        pl.imshow(I, cmap = 'Greys_r')
        
        pl.subplot(122)
        R = rotate(I, angle)
        pl.imshow(R, cmap = 'Greys_r')
        
        pl.show()