from functions import *
from scipy.interpolate import RectBivariateSpline
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
        raise ValueError('The polar coordinates (' + str(r) + ', ' + str(angle) + ') defne a valid line but it does not intersect the image.')
    if angle == 270.:
        raise ValueError('The polar coordinates (' + str(r) + ', ' + str(angle) + ') defne a valid line but it does not intersect the image.')
    
    if angle == 0.:
        if 0 <= r <= xs:
            return np.array([r, 0.]), np.array([r, ys])
        raise ValueError('The polar coordinates (' + str(r) + ', ' + str(angle) + ') defne a valid line but it does not intersect the image.')
    if angle == 180.:
        raise ValueError('The polar coordinates (' + str(r) + ', ' + str(angle) + ') defne a valid line but it does not intersect the image.')
    
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
        raise ValueError('The polar coordinates (' + str(r) + ', ' + str(angle) + ') defne a valid line but it does not intersect the image.')
    raise ValueError('well fuck.')


def line_analysis(I, r, angle, dx = .2):
    p1, p2 = box_intersection_points(I, r, angle)
    lineLenght = np.sqrt(np.sum((p1 - p2)**2))
    numSteps = int( lineLenght // dx )
    x, stepX = np.linspace(p1[0], p2[0], numSteps, retstep = True)
    y, stepY = np.linspace(p1[1], p2[1], numSteps, retstep = True)
    step = np.sqrt(stepX**2 + stepY**2)
    
    spl = RectBivariateSpline(np.arange(I.shape[0]), np.arange(I.shape[1]), I, kx = 3, ky = 3)
    fx  = spl.__call__(x, y, dx = 1, grid = False)
    fy  = spl.__call__(x, y, dy = 1, grid = False)
    fxx = spl.__call__(x, y, dx = 2, grid = False)
    fyy = spl.__call__(x, y, dy = 2, grid = False)

    deriv  = ( fy *np.cos(angle) - fx *np.sin(angle) )**2
    deriv2 = ( fyy*np.cos(angle) - fxx*np.sin(angle) )**2
    
    deriv  = step * np.sum(deriv ) / lineLenght
    deriv2 = step * np.sum(deriv2) / lineLenght
    
    return deriv, deriv2


def hough_mig(I):
    R = np.linspace(0., np.sqrt((I.shape[0] - 1)**2 + (I.shape[1] - 1)**2), 1000)
    O = np.linspace(0., 360., 1000.)
    R, O = np.meshgrid(R, O)
    H1 = np.zeros(R.shape)
    H2 = np.zeros(R.shape)
    for i in range(R.shape[0]):
        print round(100.*i/float(R.shape[0]), 2), '%'
        for j in range(R.shape[1]):
            try:
                H1[i, j], H2[i, j] = line_analysis(I, R[i, j], O[i, j])
            except:
                H1[i, j], H2[i, j] = np.nan, np.nan
    #pl.subplot(131)
    #pl.imshow(I, cmap = 'Greys_r')
    pl.axis('off')
    pl.subplot(221)
    pl.contourf(R, O, H1, levels = np.linspace(0., H1[np.where(H1 > 0)].max(), 100))
    pl.subplot(222)
    pl.contourf(R, O, H2, levels = np.linspace(0., H2[np.where(H2 > 0)].max(), 100))
    
    print H1[np.where(H1 == H1[np.where(H1 > 0)].max())]
    
#    x, y = np.meshgrid(np.arange(I.shape[0]), np.arange(I.shape[1]), indexing = 'ij')
#    pl.subplot(223)
#    pl.contourf(x, y, I, cmap = 'Greys_r')
#    pl.axes().set_aspect('equal', 'datalim')
#    pl.plot([p1[0], p2[0]], [p1[1], p2[1]])
    
    pl.show()


I = imread('cinzenta_com.jpg')
I = np.average(I, axis = 2)
print I.shape
I = compr(I, 32)
print I.shape
#I = convolve2d(I, generateGaussianKernel2D(50), mode = 'valid')
hough_mig(I)


#p1, p2 = box_intersection_points(I, 36.8616, 90.8055)
#
#pl.figure(1)
#x, y = np.meshgrid(np.arange(I.shape[0]), np.arange(I.shape[1]), indexing = 'ij')
#pl.contourf(x, y, I, cmap = 'Greys_r')
#pl.axes().set_aspect('equal', 'datalim')
#pl.plot([p1[0], p2[0]], [p1[1], p2[1]])
#
#pl.show()