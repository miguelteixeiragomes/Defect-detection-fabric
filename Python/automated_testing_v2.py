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

images_dir_com = 'com' + breaker
images_dir_sem = 'sem' + breaker
images_com = [images_dir_com + f for f in listdir(images_dir_com) if isfile(join(images_dir_com, f)) and ('.png' in f  or  '.jpg' in f)]
images_sem = [images_dir_sem + f for f in listdir(images_dir_sem) if isfile(join(images_dir_sem, f)) and ('.png' in f  or  '.jpg' in f)]
#images_com = [np.uint8(np.around(np.average(np.float32(imread(paths)), axis = 2))) for paths in images_com]
#images_sem = [np.uint8(np.around(np.average(np.float32(imread(paths)), axis = 2))) for paths in images_sem]


def Q_function(x):
    s = 0
    for i in range(len(images_com)):
        #print '\t', i, '/', len(images_com)
        img = np.average(np.float32(imread(images_com[i])), axis = 2)
        #img = np.float32(images_com[i])
        if fullAnalysis(img, x[0], x[1], x[2]) == True:
            s += 1
#        else:
#            imsave('fails\\' + images_com[i][3:], img)

    for i in range(len(images_sem)):
        img = np.average(np.float32(imread(images_sem[i])), axis = 2)
        #img = np.float32(images_sem[i])
        if fullAnalysis(img, x[0], x[1], x[2]) == False:
            s += 1
            #imsave('fails\\' + images_sem[i][3:], img)

    return float(s)


if __name__ == '__main__':
    from time import clock
    test = ['function', 'parameterFinder'][0]

    if test == 'function':
        Ti = clock()
        print Q_function([20. , 20.  ,  1.5]) # options: [20.,20.,1.5] ->   ou  20. , 10. , 2.0
        print 'exec time:', clock() - Ti

    if test == 'parameterFinder':
        print conjGradMax(Q_function, [20. , 20. , 1.5])