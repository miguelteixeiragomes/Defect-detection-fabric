import numpy as np
from initCL import get_ready_cl
import pyopencl as cl

ctx, queue, mf, device = get_ready_cl()
prg = cl.Program(ctx, open('kernelsCL\\imageRotation90.cl', 'r').read()).build()
##########################################################################################


def rotateUpTo90_horizontal(I_h, theta):
    s = I_h.shape[0] - 1
    l = I_h.shape[1] - 1

    x = 0.5*s
    if s > l*np.sin(2.0*theta):
        x = np.sin(theta) * (l*np.cos(theta) - s*np.sin(theta))/(np.cos(2.0*theta))

    a = x/np.sin(theta)
    b = (s - x)/np.cos(theta)
    
    X, Y = int(a) - 1, int(b) - 1
    R, O = np.sqrt(X**2 + Y**2), np.arctan2(Y, X) - theta
    X, Y = R*np.cos(O), R*np.sin(O) + x
    offsetX = .5*(l - X)
    
    R_h = np.zeros( (int(b), int(a)) , np.float32)
    
    I_d        = cl.Buffer(ctx, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf = I_h)
    R_d        = cl.Buffer(ctx, mf.READ_WRITE , size = 4*R_h.shape[0]*R_h.shape[1])

    prg.rotateUpTo90_horizontal(queue, (R_h.shape[1], R_h.shape[0]), None, I_d, R_d, np.float32(theta), np.float32(x), np.uint16(I_h.shape[1]), np.float32(offsetX)).wait()
    
    cl.enqueue_copy(queue, R_h, R_d)
    return R_h


def rotateUpTo90(I, theta):
    if I.shape[0] <= I.shape[1]:
        return rotateUpTo90_horizontal(I, theta*np.pi/180.)
    R = np.zeros( (I.shape[1], I.shape[0]) , np.float32 )
    R[:, :] = I.T[::-1, :]
    return rotateUpTo90_horizontal(R, theta*np.pi/180.).T[:, ::-1]


def rotateCL_aux(I, angle):
    theta = angle % 360.
    
    if theta == 0.:
        return I
    
    if theta < 90.:
        return rotateUpTo90( I if I.dtype == np.float32 else np.float32(I) , theta )
    
    if theta == 90.:
        return I.T[::-1, :]
    
    if theta < 180.:
        A = np.zeros( (I.shape[1], I.shape[0]) , np.float32 )
        A[:, :] = I.T[::-1, :]
        return rotateUpTo90(A, theta - 90.)
    
    if theta == 180.:
        return I[::-1, ::-1]
    
    if theta < 270.:
        A = np.zeros( I.shape , np.float32 )
        A[:, :] = I[::-1, ::-1]
        return rotateUpTo90(A, theta - 180.)
    
    if theta == 270.:
        return I.T[:, ::-1]

    if theta < 360.:
        A = np.zeros( (I.shape[1], I.shape[0]) , np.float32 )
        A[:, :] = I.T[:, ::-1]
        return rotateUpTo90(A, theta - 270.)


def rotateCL(I, angle):
    A = rotateCL_aux(I, angle)
    B = np.zeros( A.shape , np.float32 )
    B[:, :] = A[:, :]
    return B


if __name__ == '__main__':
    from time import clock
    import pylab as pl
    from scipy.ndimage import imread
    from imageRotationPY import rotatePY
    I = np.float32(np.average( imread('miguel.png') , axis = 2 ))
    print I.shape
    angle = 350.
    Ti = clock()
    PY = rotatePY(I, angle)
    print 'PY:', round(clock() - Ti, 6)
    Ti = clock()
    CL = rotateCL(I, angle)
    print 'CL:', round(clock() - Ti, 6)
    
    pl.subplot(131)
    pl.imshow(I, cmap = 'Greys_r')
    pl.axis('off')
    pl.subplot(132)
    pl.imshow(PY, cmap = 'Greys_r')
    pl.axis('off')
    pl.subplot(133)
    pl.imshow(CL, cmap = 'Greys_r')
    pl.axis('off')
    pl.show()