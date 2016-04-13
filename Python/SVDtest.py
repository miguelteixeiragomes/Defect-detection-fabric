from functions import *


I = imread('cinzenta_com.jpg')
I = np.average(I, axis = 2)
I = compr(I, 8)


I2 = convolve2d(I, generateGaussianKernel2D(40), mode = 'valid')
I3 = svd_decomp(I, 1)


pl.figure('svd')

pl.subplot(131)
pl.imshow(I, cmap = 'Greys_r')
pl.axis('off')

pl.subplot(132)
pl.imshow(I2, cmap = 'Greys_r')
pl.axis('off')

pl.subplot(133)
pl.imshow(I3, cmap = 'Greys_r')
pl.axis('off')

pl.show()