from algorithm import fullAnalysis
from scipy.ndimage import imread
import numpy as np
import pylab as pl
from time import clock
import pickle
from mpl_toolkits.mplot3d import Axes3D
from os import listdir
from os.path import isfile, join
import sys

def parameters_variation_from_array(I, defect = True, blur1 = np.arange(1, 101, 4), blur2 = np.arange(1, 101, 4), threshold = np.arange(1.1, 10.1, 0.5)):
    Ti = clock()
    A = np.zeros((blur1.shape[0], blur2.shape[0], threshold.shape[0]), np.uint8)
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            print i*A.shape[0] + j, '/', A.shape[0]*A.shape[1]
            for k in range(A.shape[2]):
                test = fullAnalysis(I, blur1[i], blur2[j], threshold[k])
                if defect:
                    if test:
                        A[i, j, k] = 1
                    else:
                        A[i, j, k] = 0
                else:
                    if test:
                        A[i, j, k] = 0
                    else:
                        A[i, j, k] = 1
    total_time = int(round(clock() - Ti))
    minutes, seconds = divmod(total_time, 60)
    hours, minutes = divmod(minutes, 60)
    print "Total time = %d:%02d:%02d" % (hours, minutes, seconds)
    return A

#def parameters_variation(I, defect = True, blur1 = np.arange(1, 101, 4), blur2 = np.arange(1, 101, 4), thrsh = np.arange(1.1, 10.1, 0.5)):
#    path = 'analysed_images\\b1_' + str(blur1[0]) + '_' + str(blur1[-1]) + '_' + str(blur1[1] - blur1[0]) + '__' + \
#                            'b2_' + str(blur2[0]) + '_' + str(blur2[-1]) + '_' + str(blur2[1] - blur2[0]) + '__' + \
#                            'tr_' + str(thrsh[0]) + '_' + str(thrsh[-1]) + '_' + str(thrsh[1] - thrsh[0]) + '.npy'
#    try:
#        return np.load(path)
#    except:
#        arr = parameters_variation_from_array(I, defect, blur1, blur2, thrsh)
#        np.save(path, arr)
#        return arr

def updateParamList(parameterList, img, defect):
    i = 0
    while i < len(parameterList):
        if fullAnalysis(img, parameterList[i][0], parameterList[i][1], parameterList[i][2]) != defect:
            del(parameterList[i])
        else:
            i += 1
    return parameterList
            

def testing(images_dir, defect_image, fG, sG, threshold):
    fileName = 'parametersTest_' + 
    try:
        pickle.load(file(fileName))
    
    except:
        images_com = [f for f in listdir(images_dir) if isfile(join(images_dir, f))]
        
        
        paramList = []
        for i in fG:
            for j in sG:
                for k in threshold:
                    paramList.append([i, j, k])    
        
        for image in images_com:        
            I = imread(images_dir + image)
            I = np.average(I, axis = 2)
            paramList = updateParamList(paramList, I, True)
            
        for image in images_sem:        
            I = imread(images_dir + image)
            I = np.average(I, axis = 2)
            paramList = updateParamList(paramList, I, False)
    
        pickle.dump(paramList, file(fileName))
        
    fig = pl.figure(2)
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter([i[0] for i in paramList], [i[1] for i in paramList], [i[2] for i in paramList], c='g', alpha = 0.5)
    ax.set_xlabel('1st Gauss Blur')
    ax.set_ylabel('2nd Gauss Blur')
    ax.set_zlabel('Threshold')
    pl.show()
                
fG = np.arange(1.0, 61.0, 2.0)
sG = np.arange(1.0, 51.0, 2.0)
threshold = np.arange(1.1, 10.1, 0.5)
defect_image = True
non_defect_image = False
directory_defect = 'C:\\Users\\1v7\\Projeto\\Imagens\\Com_Defeito\\'
directory_non_defect = 'C:\\Users\\1v7\\Projeto\\Imagens\\Sem_Defeito\\'

testing(directory_defect, defect_image, fG, sG, threshold)
testing(directory_non_defect, non_defect_image, fG, sG, threshold)