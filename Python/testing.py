from functions import defect_detection
from scipy.ndimage import imread
import numpy as np
import pylab as pl
from time import clock
import pickle
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

compr = 3
blur1 = np.arange(1, 101, 8)
blur2 = np.arange(1, 101, 8)
thres = np.arange(1.5, 10.5, .5)

lst = []
for i in range(len(blur1)):
    for j in range(len(blur2)):
        for k in range(len(thres)):
            lst.append( (blur1[i], blur2[j], thres[k]) )

A = imread('img_to_analyse\\IMG_20160316_163331.jpg')
A = np.average(A, axis = 2)
B = imread('img_to_analyse\\IMG_20160316_163350.jpg')
B = np.average(B, axis = 2)

i = 0
while i < len(lst):
    print i, len(lst)
    if not defect_detection(A, compr, blur1[lst[i][0]], blur1[lst[i][1]], blur1[lst[i][2]]):
        del(lst[i])
    else:
        i += 1

i = 0
while i < len(lst):
    print i, len(lst)
    if not defect_detection(B, compr, blur1[lst[i][0]], blur1[lst[i][1]], blur1[lst[i][2]]):
        del(lst[i])
    else:
        i += 1

pickle.dump(lst, 'listOfGoodPoints.mig')



fig = plt.figure()
ax = fig.add_subplot(111, projection = '3d')
for i in lst:
    ax.scatter([i[0]], [i[1]], [i[2]])
ax.set_xlabel('blur1')
ax.set_ylabel('blur2')
ax.set_zlabel('thres')
plt.show()