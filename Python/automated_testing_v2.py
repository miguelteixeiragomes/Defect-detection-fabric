from algorithm import fullAnalysis
from scipy.ndimage import imread
from scipy.misc import imsave
import numpy as np
import pylab as pl
from mpl_toolkits.mplot3d import Axes3D
from os import listdir
from os.path import isfile, join
from conjugateGradient import conjGradMax
import platform
breaker = '\\' if platform.system() == 'Windows' else '/'

images_dir_com = 'Poly_com' + breaker
images_dir_sem = 'Poly_sem' + breaker
images_com = [images_dir_com + f for f in listdir(images_dir_com) if isfile(join(images_dir_com, f)) and ('.png' in f  or  '.jpg' in f)]
images_sem = [images_dir_sem + f for f in listdir(images_dir_sem) if isfile(join(images_dir_sem, f)) and ('.png' in f  or  '.jpg' in f)]
images_com = [np.uint8(np.around(np.average(np.float32(imread(paths)), axis = 2))) for paths in images_com]
images_sem = [np.uint8(np.around(np.average(np.float32(imread(paths)), axis = 2))) for paths in images_sem]
print '\nNumber of images with defects:   ', len(images_com)
print 'Number of images without defects:', len(images_sem), '\n'


def Q_function(x):
    defectsDetected = 0
    missedDefects = 0
    falseAlarms = 0

    for i in range(len(images_com)):
        #print '\t', i, '/', len(images_com)
        #img = np.average(np.float32(imread(images_com[i])), axis = 2)
        img = np.float32(images_com[i])
        if fullAnalysis(img, x[0], x[1], x[2]) == True:
            defectsDetected += 1
        else:
            missedDefects += 1
#            pl.imshow(images_sem[i], cmap = 'Greys_r')
#            pl.show()

    for i in range(len(images_sem)):
        #img = np.average(np.float32(imread(images_sem[i])), axis = 2)
        img = np.float32(images_sem[i])
        if fullAnalysis(img, x[0], x[1], x[2]) == True:
            falseAlarms += 1
#            pl.imshow(images_sem[i], cmap = 'Greys_r')
#            pl.show()

    defectsDetected /= float(len(images_com)) / 100.
    missedDefects   /= float(len(images_com)) / 100.
    falseAlarms     /= float(len(images_sem)) / 100.
    print '\tdefects detected:', round(defectsDetected, 1), '%'
    print '\tmissed defects:', round(missedDefects, 1), '%'
    print '\tfalse alarms:', round(falseAlarms, 1), '%'

    return float(defectsDetected - falseAlarms)


if __name__ == '__main__':
    from time import clock
    test = ['function', 'parameterFinder'][0]

    if test == 'function':
        Ti = clock()
        print Q_function([25. , 15. , 30.0]) # best so far: 20. , 30. , 3.0 algodao
        print 'exec time:', clock() - Ti

    if test == 'parameterFinder':
        print conjGradMax(Q_function, [20. , 30. , 3.])