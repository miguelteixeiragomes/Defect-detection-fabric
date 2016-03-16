from functions import *

I = imread('com.png')
I = np.average(I, axis = 2)


print fullTest(I, 7, 10, 10, 2.)
pl.show()
