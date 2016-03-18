from functions import defect_detection
from scipy.ndimage import imread
import numpy as np
import pylab as pl
from time import clock
import pickle

def parameters_variation_from_array(I, defect = True, blur1 = np.arange(1, 101, 4), blur2 = np.arange(1, 101, 4), threshold = np.arange(1.1, 10.1, 0.5)):
    Ti = clock()
    A = np.zeros((blur1.shape[0], blur2.shape[0], threshold.shape[0]), np.uint8)
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            print i*A.shape[0] + j, '/', A.shape[0]*A.shape[1]
            for k in range(A.shape[2]):
                test = defect_detection(I, 3, blur1[i], blur2[j], threshold[k], False, True)
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
    

I = imread('tojo.jpg')
I = np.average(I, axis = 2)

parameters_variation(I)