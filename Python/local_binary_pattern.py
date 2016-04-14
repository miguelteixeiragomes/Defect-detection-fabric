# -*- coding: utf-8 -*-
"""
Created on Wed Apr 06 22:39:56 2016

@author: Miguel Gomes
"""

import numpy as np
import pylab as pl
from scipy.ndimage import imread
from functions import gaussianBlur, compr


def LBP(I):
    a  =   1*(I[1:-1, 1:-1] >= I[2:, :-2])
    a +=   2*(I[1:-1, 1:-1] >= I[2:, 1:-1])
    a +=   4*(I[1:-1, 1:-1] >= I[2:, 2:])
    a +=   8*(I[1:-1, 1:-1] >= I[1:-1, 2:])
    a +=  16*(I[1:-1, 1:-1] >= I[:-2, 2:])
    a +=  32*(I[1:-1, 1:-1] >= I[:-2, 1:-1])
    a +=  64*(I[1:-1, 1:-1] >= I[:-2, :-2])
    a += 128*(I[1:-1, 1:-1] >= I[1:-1, :-2])
    return a

def mosaic_LBP_hist(I, x_n, y_n, BINS = 50, blur = 1):    
    lbp = LBP(gaussianBlur(I, blur))
    
    x_len = I.shape[0] // x_n
    y_len = I.shape[1] // y_n
    
    pl.figure('Local Binary Pattern image')
    pl.subplot(121)
    pl.imshow(I, cmap = 'Greys_r')
    pl.axis('off')
    pl.subplot(122)
    pl.imshow(lbp, cmap = 'Greys_r')
    pl.axis('off')
    
    HISTS = np.zeros((x_n, y_n, BINS))
    for i in range(x_n):
        for j in range(y_n):
            hist = np.histogram( I[i*x_len:(i+1)*x_len , j*y_len:(j+1)*y_len].ravel() , bins = BINS, density = True)[0]
            HISTS[i, j] = hist

    avg_hist = np.mean(HISTS, axis = (0, 1))
    hist_diff = np.zeros(HISTS.shape)
    for i in range(x_n):
        for j in range(y_n):
            hist_diff[i, j] = np.abs(avg_hist - HISTS[i, j])
    hist_diff /= hist_diff.max()

    pl.figure('mosaic Local Binary Pattern histograms')  
    for i in range(x_n):
        for j in range(y_n):
            pl.subplot(x_n, y_n, i*y_n + j + 1)
            #pl.bar( np.arange(BINS) , HISTS[i, j] , width = 1. ) # apenas os histogramas
            pl.bar( np.arange(BINS) , hist_diff[i, j] , width = 1. ) ; pl.ylim([0, 1]) # diferença entre o hist e o hist médio
            #pl.imshow( I[i*x_len:(i+1)*x_len , j*y_len:(j+1)*y_len] , cmap = 'Greys_r') # para testar se a imagem está a ser dividida como manda a sapatilha
            pl.axis('off')
    
    pl.show()

def LBP_transform(I, win_size, scan_rate, BINS = 50, blur = 1):
    win_size = [win_size]*2  if type(win_size) in [int, np.int, np.int8, np.int16, np.int32, np.int64, np.uint8, np.uint16, np.uint32, np.uint64]  else  win_size
    scan_rate = [scan_rate]*2  if type(scan_rate) in [int, np.int, np.int8, np.int16, np.int32, np.int64, np.uint8, np.uint16, np.uint32, np.uint64]  else  scan_rate
    
    lbp = LBP(gaussianBlur(I, blur))
    print lbp.shape
    
    Is = np.arange(0, lbp.shape[0] - win_size[0] - 1, scan_rate[0])
    print Is.shape
    Js = np.arange(0, lbp.shape[1] - win_size[1] - 1, scan_rate[1])
    print Js.shape
    
    hists = np.zeros((len(Is), len(Js), BINS), np.float32)
    print hists.shape
    
    x = 0
    for i in Is:
        y = 0
        for j in Js:
            hists[x, y] = np.histogram(lbp[ i:i+win_size[0]  ,  j:j+win_size[1] ].ravel(), bins = BINS, normed = True)[0]
            y += 1
        x += 1
    
    avg_hist = np.mean(hists, axis = (0, 1))
    res = np.zeros((len(Is), len(Js)))
    
    for i in range(res.shape[0]):
        for j in range(res.shape[1]):
            res[i, j] = np.sum(np.abs(hists[i, j] - avg_hist)**2)
            #res[i, j] = np.sum( (hists[i, j] - avg_hist)**2 / (hists[i, j] + avg_hist) )
    
    return res
    


I = imread('mov.png')
I = np.average(I, axis = 2)
I = compr(I, 2)
#mosaic_LBP_hist(I, 8, 8, blur = 5)
img = LBP_transform(I, win_size = 25, scan_rate = 2, BINS = 256, blur = 1)
img = gaussianBlur(img, 1)
pl.imshow(1*(img > .5*(img.max() + img.min())))
pl.show()