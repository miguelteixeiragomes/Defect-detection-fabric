from functions import * 

I = imread('rodada.png')
I = np.average(I, axis = 2)

print photo_angle(I)

print defect_detection(I, 2, 1, 10, 2., True, True)
pl.show()