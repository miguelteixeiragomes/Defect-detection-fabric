import numpy as np
print 'Image Rotation:'
try:
    from imageRotationCL import rotateCL as rotateTmp
    print "\tKicking it up openCL style!"
except:
    from imageRotationPY import rotatePY as rotateTmp
    import random
    print "\tInstall the damned openCL you %s!" % (random.choice(['fool', 'oaf', 'knave', 'varlet']),)


def rotate(I, angle):
    return rotateTmp( I if I.dtype == np.float32 else np.float32(I) , angle  )


if __name__ == '__main__':
    import pylab as pl
    from scipy.ndimage import imread
    I = imread('dados.png')
    I = np.average(I, axis = 2)
    
    from time import clock
    angle = 45.
    pl.subplot(121)
    pl.imshow(I, cmap = 'Greys_r')
    pl.axis('off')
    
    pl.subplot(122)
    Ti = clock()
    R = rotate(I, angle)
    print 'time =', round(clock() - Ti, 6), 's'
    pl.imshow(R, cmap = 'Greys_r')
    pl.axis('off')
    
    pl.show()