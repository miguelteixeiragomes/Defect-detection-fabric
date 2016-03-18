# -*- coding: utf-8 -*-
"""
Created on Mon Feb 29 22:57:31 2016

@author: Miguel Gomes
"""

import numpy as np
import pylab as pl
from scipy.ndimage import imread


def bilinear_interpolation_image(Image, x, y):
    if 0 <= x <= Image.shape[0] - 1 and 0 <= y <= Image.shape[1] - 1 :
        x1 = int(x)
        x2 = x1 + 1
        y1 = int(y)
        y2 = y1 + 1
        
        if x == Image.shape[0] - 1:
            x2 = int(x)
            x1 = x2 - 1
        
        if y == Image.shape[1] - 1:
            y2 = int(x)
            y1 = y2 - 1
        
        f11 = Image[x1, y1]
        f21 = Image[x2, y1]
        f12 = Image[x1, y2]
        f22 = Image[x2, y2]
        
        print f11, f12, f21, f22
        
        return f11*(x2 - x)*(y2 - y)  +  f21*(x - x1)*(y2 - y)  +  f12*(x2 - x)*(y - y1)  +  f22*(x - x1)*(y - y1)
    raise IndexError('You can not spline points such as (' + str(x) + ', ' + str(y) + ') out of the domain of given points.')



if __name__ == '__main__':
    I = imread('rodada.png').astype(np.float64)
    I = np.average(I, axis = 2)
    
    print bilinear_interpolation_image(I, 2447., 0.)