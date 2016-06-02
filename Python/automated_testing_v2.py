from algorithm import fullAnalysis
from scipy.ndimage import imread
import numpy as np
import pylab as pl
from mpl_toolkits.mplot3d import Axes3D
from os import listdir
from os.path import isfile, join
from conjugateGradient import conjGradMax

images_dir_com = 'com_defeito\\'
images_dir_sem = 'sem_defeito\\'
images_com = [images_dir_com + f for f in listdir(images_dir_com) if isfile(join(images_dir_com, f)) and ('.png' in f  or  '.jpg' in f)]
images_sem = [images_dir_sem + f for f in listdir(images_dir_sem) if isfile(join(images_dir_sem, f)) and ('.png' in f  or  '.jpg' in f)]        


def Q_function(x):
    s = 0
    for i in range(len(images_com)):
        #print '\t', i, '/', len(images_com)
        img = np.average(np.float32(imread(images_com[i])), axis = 2)
        if fullAnalysis(img, x[0], x[1], x[2]) == True:
            s += 1

    for i in range(len(images_sem)):
        img = np.average(np.float32(imread(images_sem[i])), axis = 2)
        if fullAnalysis(img, x[0], x[1], x[2]) == False:
            s += 1
    
    return float(s)


if __name__ == '__main__':
    test = ['function', 'parameterFinder'][1]
    
    if test == 'function':
        print Q_function([1.24825119 , 10.01321442 , 1.22132229])
        
    if test == 'parameterFinder':
        print conjGradMax(Q_function, [1.24825119 , 10.01321442 , 1.22132229]) # last value [1.24825119 , 10.01321442 , 1.22132229]