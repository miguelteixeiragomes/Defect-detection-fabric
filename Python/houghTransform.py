import numpy as np
import pylab as pl
from scipy.interpolate import RectBivariateSpline
from scipy.ndimage import imread

cos = lambda x: np.cos(np.pi/180.*x)
sin = lambda x: np.sin(np.pi/180.*x)
tan = lambda x: np.tan(np.pi/180.*x)


def box_intersection_points(I, r, angle):
    if r < 0:
        raise ValueError('The polar coordinates (' + str(r) + ', ' + str(angle) + ') are not valid.')
    angle -= 360.*(angle//360.)
    xs, ys = I.shape[0] - 1, I.shape[1] - 1
    
    if angle == 90.:
        if 0 <= r <= ys: 
            return np.array([0., r]), np.array([xs, r])
        raise ValueError('The polar coordinates (' + str(r) + ', ' + str(angle) + ') define a valid line but it does not intersect the image.')
    if angle == 270.:
        raise ValueError('The polar coordinates (' + str(r) + ', ' + str(angle) + ') define a valid line but it does not intersect the image.')
    
    if angle == 0.:
        if 0 <= r <= xs:
            return np.array([r, 0.]), np.array([r, ys])
        raise ValueError('The polar coordinates (' + str(r) + ', ' + str(angle) + ') define a valid line but it does not intersect the image.')
    if angle == 180.:
        raise ValueError('The polar coordinates (' + str(r) + ', ' + str(angle) + ') define a valid line but it does not intersect the image.')
    
    A = r / cos(angle)
    B = r / sin(angle)
    C = A - ys*tan(angle)
    D = B - xs/tan(angle)
    
    pnts = []
    if 0 <= A < xs:
        pnts.append( np.array([A, 0.]) )
    if 0 <= D < ys:
        pnts.append( np.array([xs, D]) )
    if xs >= C > 0:
        pnts.append( np.array([C, ys]) )
    if ys >= B > 0:
        pnts.append( np.array([0., B]) )
    if len(pnts) == 2:
        return pnts[0], pnts[1]
    if len(pnts) < 2:
        raise ValueError('The polar coordinates (' + str(r) + ', ' + str(angle) + ') define a valid line but it does not intersect the image.')
    raise ValueError('well fuck.')


def line_analysis(I, r, angle, dx = .2):
    p1, p2 = box_intersection_points(I, r, angle)
    lineLenght = np.sqrt(np.sum((p1 - p2)**2))
    if lineLenght < .2*min(I.shape):
        return 0.
    numSteps = int( lineLenght // dx )
    x, stepX = np.linspace(p1[0], p2[0], numSteps, retstep = True)
    y, stepY = np.linspace(p1[1], p2[1], numSteps, retstep = True)
    step = np.sqrt(stepX**2 + stepY**2)
    
    spl = RectBivariateSpline(np.arange(I.shape[0]), np.arange(I.shape[1]), I, kx = 2, ky = 2)
    fx  = spl.__call__(x, y, dx = 1, grid = False)
    fy  = spl.__call__(x, y, dy = 1, grid = False)

    deriv  = ( fy *np.cos(angle) - fx *np.sin(angle) )**2
    
    deriv  = step * np.sum(deriv ) / lineLenght
    
    return deriv


def houghTransform(I):
    #R = np.linspace(0., np.sqrt((I.shape[0] - 1)**2 + (I.shape[1] - 1)**2), 100)
    R = np.linspace(140., 160., 100)
    O = np.linspace(85., 95., 100)
    R, O = np.meshgrid(R, O)
    H = np.zeros(R.shape)
    for i in range(R.shape[0]):
        print round(100.*i/float(R.shape[0]), 2), '%'
        for j in range(R.shape[1]):
            try:
                H[i, j] = line_analysis(I, R[i, j], O[i, j])
            except:
                H[i, j] = 0.
    
    return R, O, H


if __name__ == '__main__':
    from LBP import LBP, DT
    from gaussianSubSampling import gaussianSubSampling
    I = np.average( imread('com.png') , axis = 2 )
    I = gaussianSubSampling(I, 10, 2)
    I = LBP(I)
    I = gaussianSubSampling(I, 1, 1)
    pl.subplot(121)
    pl.imshow( I , cmap = 'Greys_r' )
    pl.subplot(122)
    pl.contourf( *houghTransform(I) , cmap = 'Greys_r' )
    pl.show()