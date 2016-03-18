from functions import * 

I = imread('com.png')
I = np.average(I, axis = 2)


print defect_detection(I, 2, 10, 10, 2., True, True)
pl.show()
