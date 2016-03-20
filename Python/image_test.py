from functions import * 

I = imread('tojo.jpg')
I = np.average(I, axis = 2)

print photo_angle(I)

print defect_detection(I, 8, 20, 20, 2., True, False)
pl.show()
