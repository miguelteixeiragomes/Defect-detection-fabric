from algorithm import fullAnalysis
from scipy.ndimage import imread
import numpy as np
import pylab as pl
from mpl_toolkits.mplot3d import Axes3D
from os import listdir
from os.path import isfile, join
import pickle
from time import localtime

def updateParamList(parameterList, img, defect):
    i = 0
    L = len(parameterList)
    while i < len(parameterList):
        print '\t', round((L - len(parameterList) + i) *100. / float(L), 1), '%'
        if fullAnalysis(img, parameterList[i][0], parameterList[i][1], parameterList[i][2]) != defect:
            del(parameterList[i])
        else:
            i += 1
    return parameterList
            

def testing_siml(images_dir_com, images_dir_sem, fG, sG, threshold):
    
    images_com = [f for f in listdir(images_dir_com) if isfile(join(images_dir_com, f))]
    images_sem = [f for f in listdir(images_dir_sem) if isfile(join(images_dir_sem, f))]
            
    paramList = []
    
    for i in fG:
        for j in sG:
            for k in threshold:
                paramList.append( (i, j, k) ) 
    
    for image in images_com:
        print image
        I = np.float32(imread(images_dir_com + image))
        I = np.average(I, axis = 2)
        paramList = updateParamList(paramList, I, True)
        
    for image in images_sem:
        print image
        I = imread(images_dir_sem + image)
        I = np.average(I, axis = 2)
        paramList = updateParamList(paramList, I, False)
        
    return paramList


def testing(images_dir_com, images_dir_sem, fG, sG, threshold):    
    fileName_params = 'simls\\ParamsList_' + str(fG.min()) + '_' + str(fG.max()) + '_' + str(fG[1] - fG[0]) + '_' + \
                                             str(sG.min()) + '_' + str(sG.max()) + '_' + str(sG[1] - sG[0]) + '_' + \
                                             str(threshold.min()) + '_' + str(threshold.max()) + '_' + str(threshold[1] - threshold[0]) + '_' + '.p'
    
    try:
        paramList = pickle.load( open( fileName_params, "rb" ) )
    except:
        paramList = testing_siml(images_dir_com, images_dir_sem, fG, sG, threshold)
        pickle.dump( paramList , open( fileName_params, "wb" ) )

    fig = pl.figure(2)
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(np.array([i[0] for i in paramList]), np.array([i[1] for i in paramList]), np.array([i[2] for i in paramList]), c = 'g', alpha = 0.5)
    ax.set_xlabel('1st Gauss Blur')
    ax.set_ylabel('2nd Gauss Blur')
    ax.set_zlabel('Threshold')
    pl.show()
    
fG = np.arange(1, 25, 1)
sG = np.arange(0.0, 20.0, 1.0)
threshold = np.arange(1.1, 5.1, 0.1)
directory_defect = 'com_defeito\\'
directory_non_defect = 'sem_defeito\\'

testing(directory_defect, directory_non_defect, fG, sG, threshold)